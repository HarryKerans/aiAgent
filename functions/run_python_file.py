import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        if not os.path.isdir(working_directory):
            return(f'Error: Working directory "{file_path}" does not exist or is not a directory')
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path
        if not valid_target_file:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            return(f'Error: "{file_path}" does not exist or is not a regular file')
        if not file_path.endswith(".py"):
            return(f'Error: "{file_path}" is not a Python file')
        
        command = ["python", target_file]
        command.extend(args or [])
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=absolute_path,
            timeout=30
        )
        output = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
        if result.returncode != 0:
            output["message"] = f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            output["message"] = output.get("message", "") + ("\n" if output.get("message") else "") + "No output produced"
        else:
            msg_parts = []
            if result.stdout:
                msg_parts.append(f"STDOUT: {result.stdout.strip()}")
            if result.stderr:
                msg_parts.append(f"STDERR: {result.stderr.strip()}")
            msg = "\n".join(msg_parts)
            if msg:
                if output.get("message"):
                    output["message"] += "\n" + msg
                else:
                    output["message"] = msg
        return output

    except Exception as e:
        return(f"Error: executing Python file: {e}")