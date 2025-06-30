from os import path
from google.genai import types

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

def get_file_content(working_directory, file_path):
    working_path = path.abspath(working_directory)
    full_file_path = path.abspath(path.join(working_directory, file_path))

    if not full_file_path.startswith(working_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not path.isfile(full_file_path):
        f'Error: File not found or is not a regular file: "{file_path}"'
    MAX_CHARS = 10000

    try:
        with open(full_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {e}"
    return file_content_string
    

