from os import path, makedirs
from google.genai import types

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

def write_file(working_directory, file_path, content):
    working_path = path.abspath(working_directory)
    full_file_path = path.join(working_path, file_path)
 
    if not full_file_path.startswith(working_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not path.exists(path.dirname(full_file_path)):
        try:
            makedirs(path.dirname(full_file_path))
        except Exception as e:
            return f'Error: {e}'
    try:
        with open (full_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
