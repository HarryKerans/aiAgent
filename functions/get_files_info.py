import os

def get_files_info(working_directory, directory="."):
    if not os.path.isdir(working_directory):
        print(f'Error: Working directory "{working_directory}" does not exist or is not a directory')
        return
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, directory))
    print(f"Target directory: {target_dir}")
    # Will be True or False
    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    if not valid_target_dir:
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    for x in os.listdir(target_dir):
        filesize = os.path.getsize(os.path.join(target_dir, x))
        is_dir=os.path.isdir(os.path.join(target_dir, x))
        print(f"{x}: file_size={filesize} bytes, is_dir={is_dir}")

if __name__ == "__main__":
    get_files_info("calculator", ".")