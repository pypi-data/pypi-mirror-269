from typing import List

from persona_ai.domain import roles
from persona_ai.domain.conversations import Message
from persona_ai.domain.tasks import Task


def render_conversation_history(
    messages: List[Message], include_sender_name=True
) -> str:
    """
    Render the history of a conversation.

    Args:
    - messages: List[Message], the messages.
    - include_sender_name: bool, whether to include the sender name.

    Returns:
    - str, the rendered history.
    """
    history = []
    for message in messages:
        sender = f"{message.sender_name}: " if include_sender_name else ""
        history.append(f"{sender}{message.get_text()}")
    return "\n".join(history)


def render_context(messages: List[Message]) -> str:
    """
    Render the context of a conversation. Context do not include messages from moderator and users

    Args:
    - messages: List[Message], the messages.

    Returns:
    - str, the rendered context.
    """
    context = []
    for message in messages:
        if message.sender_role != roles.PARTY and message.sender_role != roles.USER:
            context.append(message.get_text())
    return "\n".join(context)


def render_iterations(task: Task) -> str:
    """
    Render the iterations of a task.

    Args:
    - task: Task, the task.

    Returns:
    - str, the rendered iterations.
    """
    iterations = []
    for i in task.iterations:
        assistant = i.participant_id
        # if i.output.body.tool_suggestion:
        #    assistant = i.output.body.tool_suggestion.suggested_tool
        iterations.append(
            f"Thought: {i.reason}\nAssistant: {assistant}\nAssistant Question: {i.request}\nObservation: {i.output.get_text()}"
        )

    return "\n".join(iterations)


def get_context(task: Task, conversation_history: List[Message]) -> List[Message]:
    """
    Get the context of a conversation.

    Args:
    - task: Task, the task.
    - conversation_history: List[Message], the conversation history.

    Returns:
    - List[Message], the context.
    """
    context = []
    for message in conversation_history:
        if message.timestamp < task.init_message.timestamp:
            context.append(message)
    return context


def get_task_history(task: Task, conversation_history: List[Message]) -> List[Message]:
    """
    Get the task history.

    Args:
    - task: Task, the task.
    - conversation_history: List[Message], the conversation history.

    Returns:
    - List[Message], the task history.
    """
    task_history = []
    for message in conversation_history:
        if task.init_message.timestamp <= message.timestamp:
            task_history.append(message)
    return task_history
