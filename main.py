from os import listdir, path
from typing import Tuple

import fire

from headshot_creator.extractor import extract_faces
from headshot_creator.file import download_remote_images
from logger import logger

base_path = path.join(path.dirname(__file__), "data")


def headshots(
    padding: Tuple[int, int] = (0.4, 0.6),
    output_size: Tuple[int, int] = (400, 500),
    confidence_threshold: float = 0.8,
    output_path: str = "",
    input_file: str = None,
    input_path: str = base_path,
    img_format: str = 'jpg',
    debug: bool = False,
):
    """
    Main function to start the face extraction process.
    :param padding: Padding to apply around the detected face.
    :param output_size: Size of the output image.
    :param confidence_threshold: Minimum confidence level for face detection.
    :param output_path: Path to save the output images.
    :param input_file: Path to a file containing URLs of images to process.
    :param img_format: Format of the output images (jpg, jpeg, png).
    :param debug: Enable debug logging.
    """
    if debug:
        logger.setLevel(logger.DEBUG)
        logger.info("Running in debug mode")

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
        download_remote_images(input_file, input_path)

    for file_in in listdir(input_path):
        if file_in.endswith(".jpg") or file_in.endswith(".jpeg"):
            filename = path.join(input_path, file_in)
            extract_faces(
                filename,
                file_in.split(".")[0],
                output_size,
                padding,
                confidence_threshold,
                base_path,
                output_path,
                img_format,
                debug,
            )
        else:
            continue


if __name__ == "__main__":
    fire.Fire()
