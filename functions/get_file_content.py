import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        if not os.path.isdir(working_directory):
            return(f'Error: Working directory "{working_directory}" does not exist or is not a directory')
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_file:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        is_file = os.path.isfile(target_file)
        if not is_file:
            return(f'Error: File not found or is not a regular file: "{file_path}"')
        MAX_CHARS = 10000
        content = ""
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            content += file_content_string
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content

    except Exception as e:
        return(f'Error: Something went wrong: {e}')

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory, with a maximum character limit and truncation notice.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
    ),
)