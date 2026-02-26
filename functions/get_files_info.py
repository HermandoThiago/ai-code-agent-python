import os
from google.genai import types


def get_files_info(working_directory: str, directory="."):
    """
    Lists metadata for all items within a specific directory.

    This function scans the target directory and returns a formatted string
    containing the name, size, and type (file or directory) for each item found.
    It includes a security check to ensure the target directory is contained
    within the specified working directory.

    Args:
        working_directory (str): The base directory used for security validation.
        directory (str, optional): The target directory to scan, relative to the
            working_directory. Defaults to ".".

    Returns:
        str: A bulleted list of files and directories with their sizes and
            directory status, or an error message if the path is outside
            the allowed working directory.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_dir):
        return f'Error: "{directory}" is not in the working dir'

    final_response = ""
    contents = os.listdir(abs_directory)

    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(os.path.join(abs_directory, content))
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"

    return final_response


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, "
                            "lists files in the working directory itself."
            )
        }
    )
)