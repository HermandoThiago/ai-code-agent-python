import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types  # Types package for gemini ai


def main():
    load_dotenv()

    API_KEY = os.environ.get("GEMINI_API_KEY")
    MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME")

    client = genai.Client(api_key=API_KEY)

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)

    verbose_flag = False

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    print(response.text)

    if response is None or response.usage_metadata is None:
        print("response is malformed")
        return

    if verbose_flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
