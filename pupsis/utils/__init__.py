

def get_stream_file(file_path):
    """
    Returns the content of a file as a string.

    Attributes:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def dump_stream_file(output_file_path, content):
    """
    Writes content to a file.

    Attributes:
        file_path (str): The path to the file.
        content (str): The content to write.
    """
    with open(output_file_path, 'w') as file:
        file.write(content)