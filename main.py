from typing import Tuple, List, Dict
from mtcnn import MTCNN
from pathlib import Path
import matplotlib.pyplot as pyplot
from os import path, listdir, makedirs
from PIL import Image, ImageDraw
import numpy as np
import wget
from logger import logger
import fire
from helper_methods import add_padding

base_path = path.join(path.dirname(__file__), "input")


def get_faces(pixels: np.array) -> List[Dict]:
    detector = MTCNN()
    return detector.detect_faces(pixels)


def extract_faces(
    filename: str,
    outname: str,
    required_size: Tuple[int, int],
    padding: Tuple[int, int],
    confidence_threshold: float,
    output_path: str,
    output_format: str,
    debug: bool,
):
    logger.debug(f"Looking for faces in {filename}")
    pixels = pyplot.imread(filename)
    image_main = Image.fromarray(pixels)
    draw = ImageDraw.Draw(image_main)
    results = get_faces(pixels)
    logger.info(f"Found {len(results)} faces")
    for i, result in enumerate(results):
        x1, y1, width, height = result["box"]
        if result["confidence"] > confidence_threshold:
            logger.debug(
                f"Face found with confidence of {result['confidence']}")
            x1, y1, width, height = result["box"]
            draw.rectangle([x1, y1, x1 + width, y1 + height],
                           outline="blue", width=3)
            logger.debug(
                f"Face found at {x1} {y1} with width {width} and height {height}"
            )
            x1, y1, x2, y2 = add_padding(
                x1, y1, height, width, padding, required_size[0] /
                required_size[1]
            )
            face = pixels[y1:y2, x1:x2]
            try:
                image = Image.fromarray(face)
                save_path = path.join(
                    path.dirname(__file__),
                    "output",
                    output_path,
                    f"{required_size[0]}x{required_size[1]}",
                )
                filename = f"{outname}_{i}.{output_format}"
                image = image.resize(required_size)
                saved_file = save_image(image, save_path, filename)
                logger.info(f"Written face to {saved_file}")
                draw.rectangle([x1, y1, x2, y2], outline="green", width=3)
            except:
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                logger.warning(
                    "The calculated image goes beyond the bounds of the image. Try to make the padding smaller or adjust the aspect ratio."
                )
        else:
            draw.rectangle([x1, y1, x1 + width, y1 + height],
                           outline="orange", width=3)
            logger.warning(
                f"Face found below confidence threshold at {result['confidence']}"
            )
    if debug:
        save_path = path.join(path.dirname(__file__), "output")
        filename = f"{outname}_debug.jpg"
        saved_debug_file = save_image(image_main, save_path, filename)
        logger.info(f"Saving debug image to {saved_debug_file}")


def save_image(image: Image, directory: str, filename: str) -> str:
    if not path.exists(directory):
        makedirs(directory)
    savename = path.join(directory, filename)
    image.save(savename)
    return savename


def download_remote_images(input_file: str):
    f = open(input_file, "r")
    logger.debug(f"Found file {input_file}. Reading contents")
    files_data = f.read()
    f.close()
    files = files_data.split("\n")
    Path(base_path).mkdir(parents=True, exist_ok=True)
    for num, file in enumerate(files):
        logger.debug(f"Downloading from {file}")
        file_name = file.split("/")[-1]
        wget.download(file, path.join(base_path, f"{num}.jpg"))


def start(
    padding: Tuple[int, int] = (0.4, 0.6),
    output_size: Tuple[int, int] = (400, 500),
    confidence_threshold: float = 0.95,
    output_path: str = "",
    input_file: str = None,
    img_format: str = 'jpg',
    debug: bool = False,
):
    logger.info(f"Running with padding of {padding}")
    logger.info(f"Running with required size of {output_size}")
    logger.info(f"Running with confidence threshold of {confidence_threshold}")
    logger.info(f"Using input file {input_file}")
    logger.info(f"Outputting file in {img_format} format")

    allowed_formats = ['jpg', 'jpeg', 'png']
    if img_format not in allowed_formats:
        formats = ",".join(allowed_formats)
        raise Exception(f"{img_format} is not a valid format. Try one of {formats}") 

    if input_file:
        download_remote_images(input_file)
    if debug:
        logger.setLevel(logger.DEBUG)
        logger.info(f"Running in debug mode")
    for file_in in listdir(base_path):
        if file_in.endswith(".jpg") or file_in.endswith(".jpeg"):
            filename = path.join(base_path, file_in)
            extract_faces(
                filename,
                file_in.split(".")[0],
                output_size,
                padding,
                confidence_threshold,
                output_path,
                img_format,
                debug,
            )
        else:
            continue


if __name__ == "__main__":
    fire.Fire(start)
