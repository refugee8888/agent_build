import os
import subprocess
from google.genai import types


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not os.path.basename(target_file).endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)

        s = subprocess.run(
            args=command,
            cwd=working_dir_abs,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
        output = ""
        if s.returncode != 0:
            output += f"Process exited with code {s.returncode}"
        if not s.stderr and not s.stdout:
            output += "No output produced"
        else:
            output += f"STDOUT: {s.stdout}"
            output += f"STDERR: {s.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    return output


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the content of file or files in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file, relative to the working directory (default is the file path itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of CLI flags that might be invoked when running the file(arguments can be None because they are optional).",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path", "args"],
    ),
)
