from os import path
import subprocess

def run_python_file(working_directory, file_path):
    working_path = path.abspath(working_directory)
    full_file_path = path.abspath(path.join(working_directory, file_path))

    if not full_file_path.startswith(working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not path.isfile(full_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path[-3:] == '.py':
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(['python', full_file_path], timeout=30, capture_output=True, cwd=working_path)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return_string = f'STDOUT: {result.stdout}\n'
    return_string += f'STDERR: {result.stderr}\n'
    if result.returncode != 0:
        return_string += f'Process exited with code {result.returncode}\n'
    if result.stderr == '' and result.stdout == '':
        return_string += 'No output produced.'
    return return_string

    