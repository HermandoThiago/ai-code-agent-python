from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

WORKING_DIRECTORY = "./"


def call_function(function_call_part, verbose=False):
    """
    Routes and executes function calls requested by the Gemini model.

    This function acts as a dispatcher that maps a 'FunctionCall' request from
    the Google GenAI SDK to the corresponding local tool implementation. It
    handles argument unpacking, executes the logic within the allowed
    WORKING_DIRECTORY, and wraps the output back into a 'types.Content'
    object suitable for the model's conversation history.

    Args:
        function_call_part (google.genai.types.Part): The part of the model
            response containing the 'function_call' details (name and args).
        verbose (bool, optional): If True, prints detailed information about
            the function name and its arguments to the console. Defaults to False.

    Returns:
        google.genai.types.Content: A tool response object containing either
            the "result" of the successful execution or an "error" message
            if the function name is unrecognized.
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    result = ""

    if function_call_part.name == "get_files_info":
        result = get_files_info(WORKING_DIRECTORY, **function_call_part.args)
    if function_call_part.name == "get_file_content":
        result = get_file_content(WORKING_DIRECTORY, **function_call_part.args)
    if function_call_part.name == "run_python_file":
        result = run_python_file(WORKING_DIRECTORY, **function_call_part.args)
    if function_call_part.name == "write_file":
        result = write_file(WORKING_DIRECTORY, **function_call_part.args)
    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"}
                )
            ]
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result}
            )
        ]
    )
