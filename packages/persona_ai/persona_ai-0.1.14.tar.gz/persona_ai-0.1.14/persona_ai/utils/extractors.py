import re
from typing import List

from strip_markdown import strip_markdown

from persona_ai.domain.conversations import FileReference


def extract_json(data: str) -> str:
    """Extract JSON delimited from ```json ... ``` from a string."""

    data = data.strip()
    if data.startswith("{") and data.endswith("}"):
        return data

    json = re.search(r"```json(.*?)```", data, re.DOTALL)
    if json:
        return json.group(1)


def extract_json_object(data: str) -> str:
    """Extract JSON object delimited a string."""

    start_index = data.find("{")
    end_index = data.rfind("}") + 1
    return data[start_index:end_index]


def extract_moderation_block(data: str) -> str:
    """Extract moderation block delimited from ```moderation ... ``` from a string."""

    python = re.search(r"```moderation(.*?)```", data, re.DOTALL)
    if python:
        return python.group(1)
    else:
        return data


def extract_python_code(data: str) -> str:
    """Extract Python code delimited from ```python ... ``` from a string."""
    python = re.search(r"```python(.*?)```", data, re.DOTALL)
    if python:
        return python.group(1)


def markdown_to_text(markdown: str) -> str:
    """Convert markdown to text."""
    return strip_markdown(markdown)


def extract_message_block(text: str) -> str:
    """Extract message tag block delimited from <message></message from a string."""
    tag = re.search(r"<message>(.*?)</message>", text, re.DOTALL)
    if tag:
        return tag.group(1).strip()
    else:
        return text.strip()


def extract_files_block(text: str) -> List[FileReference]:
    """
    Extract multiple files references from a block of this type:
    <files>
        <file name="the name of the file" description="the description of the file", mime_type="mime type of the file" />
        <file name="the name of the file 2" description="the description of the file 2", mime_type="mime type of the file 2" />
    </files>
    """

    file_references = []
    files = re.search(r"<files>(.*?)</files>", text, re.DOTALL)
    if files:
        files = files.group(1)
        for file in re.findall(r"<file(.*?)/>", files, re.DOTALL):
            name = re.search(r'path="(.*?)"', file).group(1)
            description = re.search(r'description="(.*?)"', file).group(1)
            mime_type = re.search(r'mime_type="(.*?)"', file).group(1)
            file_references.append(
                FileReference(
                    path=name, description=description, content_type=mime_type
                )
            )

    return file_references
