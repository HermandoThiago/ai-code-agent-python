import os
import sys

from dotenv import load_dotenv

from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel

from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function


def main():
    load_dotenv()

    console = Console()

    API_KEY = os.environ.get("GEMINI_API_KEY")
    MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")

    if not API_KEY:
        console.print("[bold red]Error: GEMINI KEY not found[/]")
        return

    console.print(Panel("""\n[dark blue]                                                                                                                                                                                                                                                                                                                                                                                                            
      [ P Y T H O N   C O D E   A G E N T ]
      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
      >> STATUS: [ BUILDING_MODULES... ]
    \n"""))

    client = genai.Client(api_key=API_KEY)

    system_prompt = """
        You are a helpful AI coding agent,
        
        When a user asks a question or makes a request, make a function call plan. You can perfom the following operations:
        
        - List files and directories
        - Read the content of a file
        - Write to a file (create or update)
        - Run a Python file with optional arguments
        
        All paths you provide should be relative to the working directory. You do not need to specify the working 
        directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content
        ]
    )

    history = []
    verbose_flag = "--verbose" in sys.argv

    console.print(Panel("[bold green]Agente de IA Pronto! Como posso ajudar no seu código hoje?[/]"))
    
    while True:
        user_input = Prompt.ask("\n[bold blue]Você[/]")

        if user_input.lower() in ["exit", "quit"]:
            break

        # Adiciona a mensagem do usuário ao histórico
        history.append(
            types.Content(
                role="user", 
                parts=[types.Part(text=user_input)]
            )
        )

        while True:  # Loop de iteração do agente (pensar -> agir -> observar)
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=history,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )


            history.append(response.candidates[0].content)


            if response.text:
                console.print(f"\n[bold magenta]Gemini:[/] {response.text}")


            if not response.function_calls:
                break


            for function_call in response.function_calls:
                console.print(f"[yellow]⚙️ Executando: {function_call.name}...[/]")
                
                result = call_function(function_call, verbose_flag)
                
                history.append(types.Content(
                    role="tool", # No SDK novo, pode ser necessário ajustar o papel ou usar part específica
                    parts=[types.Part(function_response=types.FunctionResponse(
                        name=function_call.name,
                        response={"result": result}
                    ))]
                ))
                
                if verbose_flag:
                    console.print(f"[dim]Resultado da função: {result}[/]")



main()
