import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        if not os.path.isdir(working_directory):
            return(f'Error: Working directory "{working_directory}" does not exist or is not a directory')
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_file:
            return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')


        if os.path.isdir(target_file):
            return(f'Error: Cannot write to "{file_path}" as it is a directory')
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

    except Exception as e:
        return(f'Error: Something went wrong: {e}')

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory, creating directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)