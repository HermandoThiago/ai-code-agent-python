import os


def write_file(working_directory, file_path, content):
    """
    Writes text content to a file within a restricted working directory.

    This function validates that the destination is within the allowed
    working directory to prevent path traversal. It also automatically
    creates any missing parent directories before attempting to write
    the file.

    Args:
        working_directory (str): The base directory used for security validation.
        file_path (str): The path to the file to be written, relative to
            the working_directory.
        content (str): The string content to write into the file.

    Returns:
        str: A success message including the number of characters written,
            or an error message if the path is invalid, directories
            cannot be created, or writing fails.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'

    parent_dir = os.path.dirname(abs_file_path)

    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as error:
            return f'Could not create parent dirs: {parent_dir} = {error}'

    if not os.path.isfile(abs_file_path):
        pass

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" {len(content)} characters'
    except Exception as error:
        return f'Failed to write to file {file_path}, {error}'
