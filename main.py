import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = args[0]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    try:
        if args[1] == '--verbose':
            verbose_content(client, messages)
    except IndexError:
        generate_content(client, messages)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents and returns a string of those contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read files from, relative to the working directory. If not provided, read files in the working directory itself.",
            ),
        },
        required=["file_path"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns its stdout,stderr, and exit code if applicable and ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run python files from, relative to the working directory. If not provided, read files in the working directory itself.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to the given path. If the path does not exits it will create the needed directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write files to, relative to the working directory. If not provided, read files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="This is what is being writen to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    calls = response.function_calls
    if calls:
        for call in calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print("Response:")
        print(response.text)

def verbose_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),

    )
    print(f'User prompt: {messages[0].parts[0].text}')
    calls = response.function_calls
    if calls:
        for call in calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print("Response:")
        print(response.text)
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
