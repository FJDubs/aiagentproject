from os import path, listdir

def get_files_info(working_directory, directory=None):
    working_path = path.abspath(working_directory)
    directory_path = path.abspath(path.join(working_directory, directory))
    if not path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'
    if not directory_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    directory_content = listdir(directory_path)
    content_string = ''
    try:
        for content in directory_content:
            full_path = path.join(directory_path, content)
            content_string += f'- {content}: file_size={path.getsize(full_path)}, is_dir={path.isdir(full_path)}\n'
    except Exception as e:
        return f"Error: {str(e)}"
    return content_string
