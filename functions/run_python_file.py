import os
import subprocess

from google.genai import types


def run_python_file(working_directory: str, file_path: str, args: list[str]):
    """
    Executes a Python script as a subprocess within a restricted working directory.

    This function validates that the script is a Python file located within the
    allowed working directory. It executes the script using 'python3', captures
    both standard output and error streams, and enforces a 30-second timeout.

    Args:
        working_directory (str): The base directory where the script execution
            takes place (used for security validation and as the CWD).
        file_path (str): The path to the .py file to be executed, relative
            to the working_directory.
        args (list of str): A list of additional command-line arguments to
            pass to the Python script.

    Returns:
        str: A formatted string containing the script's STDOUT, STDERR, and
            exit code (if non-zero). Returns an error message if validation
            fails or an exception occurs during execution.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}"is not in the working dir'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Pytho file'

    try:
        final_args = ["python3", file_path]
        final_args.extend(args)

        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True
        )

        final_string = f"""
            STDOUT: {output.stdout}
            STDERR: {output.stderr}
            """

        if final_string == "" and output.stderr == "":
            final_string = "No output produced\n"

        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"
    except Exception as error:
        return f'Error: executing Python file: {error}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to run, relative from the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional array of strings to be used as the CLI args fot the Python files."
            )
        }
    )
)