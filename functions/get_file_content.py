import os

MAX_CHARACTERS = 10000


def get_file_content(working_directory: str, file_path: str):
    """
    Reads the content of a file within a restricted working directory.

    This function performs a security check to ensure the file path is within
    the specified working directory to prevent path traversal attacks. It also
    limits the output to a predefined maximum number of characters.

    Args:
        working_directory (str): The base directory where the file should be located.
        file_path (str): The relative or absolute path to the file to be read.

    Returns:
        str: The content of the file if successful, or an error message starting
            with 'Error:' or 'Exception reading file:'. If the file exceeds
            MAX_CHARACTERS, the content is truncated with a notice.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    file_content_string = ""

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)

            if len(file_content_string) >= MAX_CHARACTERS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
                )

        return file_content_string
    except Exception as error:
        return f"Exception reading file: {error}"
