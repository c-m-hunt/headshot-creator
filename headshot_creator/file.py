from os import makedirs, path
from pathlib import Path

import requests
from PIL import Image

from logger import logger


def save_image(image: Image, directory: str, filename: str) -> str:
    """
    Save an image to a specified directory with a given filename.
    :param image: PIL Image object to save.
    :param directory: Directory where the image will be saved.
    :param filename: Name of the file to save the image as.
    :return: Full path to the saved image.
    """
    if not path.exists(directory):
        makedirs(directory)
    savename = path.join(directory, filename)
    image.save(savename)
    return savename


def download_remote_images(input_file: str, base_path: str) -> None:
    """
    Download images from a file containing URLs and save them to a specified base path.
    :param input_file: Path to the file containing image URLs.
    :param base_path: Base path where the images will be saved.
    """
    f = open(input_file, "r")
    logger.debug(f"Found file {input_file}. Reading contents")
    files_data = f.read()
    f.close()
    files = files_data.split("\n")
    Path(base_path).mkdir(parents=True, exist_ok=True)
    for num, file in enumerate(files):
        logger.debug(f"Downloading from {file}")
        img_data = requests.get(file).content
        with open(path.join(base_path, f"{num}.jpg"), 'wb') as handler:
            handler.write(img_data)