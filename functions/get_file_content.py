from os import path

def get_file_content(working_directory, file_path):
    working_path = path.abspath(working_directory)
    full_file_path = path.join(working_path, file_path)
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
    

