import uuid


def save_image(image, key):
    """
        Saves an image file to the specified directory.

        :param image: File-like object representing the image to be saved.
        :param key: Unique identifier or category for organizing the saved images.
        :return: File path where the image is saved.
    """
    file_path = f"media/{key}/{uuid.uuid4()}-{image.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(image.file.read())
    return file_path
