import os


def file_exists(directory, filename):
    """
    Check if a file exists in a specific directory.

    :param directory: The directory in which to look for the file.
    :param filename: The name of the file to check for.
    :return: True if the file exists, False otherwise.
    """
    # Construct the full file path
    file_path = os.path.join(directory, filename)

    # Check if the file exists and is a file
    return os.path.isfile(file_path)
