import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    lines = []
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

    except Exception as e:
        return f"Error: {e}"
    for entry in os.listdir(target_dir):
        full = os.path.join(target_dir, entry)
        lines.append(
            f"- {entry}: file_size={os.path.getsize(full)} bytes, is_dir={os.path.isdir(full)}"
        )
    return "\n".join(lines)
