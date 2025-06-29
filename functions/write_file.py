from os import path, makedirs

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
