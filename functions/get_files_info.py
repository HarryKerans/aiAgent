import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        if not os.path.isdir(working_directory):
            return(f'Error: Working directory "{working_directory}" does not exist or is not a directory')
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        dir_info_lines = []
        for x in os.listdir(target_dir):
            filesize = os.path.getsize(os.path.join(target_dir, x))
            is_dir=os.path.isdir(os.path.join(target_dir, x))

            dir_info_lines.append(f"{x}: file_size={filesize} bytes, is_dir={is_dir}")
        return "\n".join(dir_info_lines)
    except Exception as e:
        return(f'Error: Something went wrong: {e}')
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)