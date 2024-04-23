import base64
import logging
import os
import tempfile

from persona_ai.code_runners.base import CodeRunner
from persona_ai.code_runners.local import LocalCodeRunner
from persona_ai.conversations.manager import ConversationManager
from persona_ai.domain import roles
from persona_ai.domain.conversations import (
    MessageBody,
    Message,
    CodeRunnerOutput,
    FileReference,
    Blob,
)
from persona_ai.domain.utils import create_id
from persona_ai.initializers.persona_configuration import PersonaAI
from persona_ai.models.base import GenAIModel
from persona_ai.personas.assistant import Assistant
from persona_ai.prompts.base import Prompt
from persona_ai.prompts.jinja import JinjaTemplatePrompt
from persona_ai.transport.messagebus import MessageBus
from persona_ai.utils.extractors import (
    extract_python_code,
)

logger = logging.getLogger(__name__)


class Coder(Assistant):
    """
    Coder is a persona that can generate python code based on the input it receives.
    The generated code is executed by a CodeRunner.
    """

    code_runner: CodeRunner
    """
    Code runner used by the coder to run the code.
    """

    code_generation_instructions: str
    """
    Instructions for code generation.
    """

    def __init__(
        self,
        name: str,
        scope: str,
        role: str = roles.CODER,
        id: str = None,
        code_runner: CodeRunner = None,
        model: GenAIModel = None,
        message_bus: MessageBus = None,
        conversation_manager: ConversationManager = None,
        prompt: Prompt = None,
        code_generation_instructions: str = None,
        allow_broadcasting: bool = False,
        included_in_moderation: bool = True,
        can_reply_multiple_times: bool = False,
    ):
        super().__init__(
            id=id if id else create_id(prefix="coder"),
            name=name,
            role=role,
            scope=scope,
            model=model if model else PersonaAI.coder_model,
            message_bus=message_bus,
            prompt=prompt if prompt else JinjaTemplatePrompt(template="coder"),
            conversation_manager=conversation_manager,
            allow_broadcasting=allow_broadcasting,
            included_in_moderation=included_in_moderation,
            can_reply_multiple_times=can_reply_multiple_times,
        )

        self.code_runner = code_runner if code_runner else LocalCodeRunner()
        self.code_generation_instructions = code_generation_instructions

    def _render_template_prompt(self, history, message):
        return self.prompt.render(
            conversation_history=history,
            request=message,
            code_generation_instructions=self.code_generation_instructions,
        )

    def _generate_reply(self, body: MessageBody, request: Message) -> Message:
        message = super()._generate_reply(body, request)

        if message.body.text is not None:
            code = extract_python_code(message.body.text)
            current_dir = os.getcwd()
            temp_dir = None
            try:
                temp_dir = tempfile.mkdtemp(suffix="_" + message.id, prefix="persona_")

                logging.debug(f"Running code in temp dir: {temp_dir}")

                code = f"""
import os
import json
os.chdir("{temp_dir}")
                    
{code}
    """

                logger.debug(f"Running code: {code}")

                result = self.code_runner.run(code)

                if not result.success:
                    message.body.text = repr(result.error)
                else:
                    if "message" in result.output:
                        message.body.text = result.output["message"]

                    if "files" in result.output:
                        message.body.blobs = [
                            self._to_blob(FileReference.model_validate(f))
                            for f in result.output["files"]
                        ]

                message.body.code_runner_output = CodeRunnerOutput(
                    code=code,
                    success=result.success,
                )

                logger.debug(f"Code runner output: {repr(message.body)}")

                return message
            finally:
                if temp_dir:
                    # Clean up temp dir
                    for file in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, file))
                    os.rmdir(temp_dir)
                    os.chdir(current_dir)

    def _to_blob(self, file_reference: FileReference):
        with open(file_reference.path, "rb") as file:
            base64_data = str(base64.b64encode(file.read()).decode("utf-8"))
            return Blob(
                id=create_id(prefix="blob"),
                description=file_reference.description,
                base64_data=base64_data,
                content_type=file_reference.content_type,
            )
