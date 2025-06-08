from os import path

import matplotlib.pyplot as pyplot
from PIL import Image, ImageDraw

from headshot_creator.utils import add_padding
from logger import logger

from .detector import get_faces
from .file import save_image


def extract_faces(
    filename: str,
    outname: str,
    required_size: tuple[int, int],
    padding: tuple[int, int],
    confidence_threshold: float,
    base_path: str,
    output_path: str,
    output_format: str,
    debug: bool,
):
    """
    Extract faces from an image and save them with specified padding and size.
    :param filename: Path to the input image file.
    :param outname: Base name for the output files.
    :param required_size: Desired size of the output images (width, height).
    :param padding: Padding to apply around the detected face (top, bottom).
    :param confidence_threshold: Minimum confidence level for face detection.
    :param base_path: Base path for saving output images.
    :param output_path: Subdirectory within base_path to save output images.
    :param output_format: Format of the output images (jpg, jpeg, png).
    :param debug: Enable debug logging.
    """

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

            if x1 < 0 or y1 < 0 or x2 > pixels.shape[1] or y2 > pixels.shape[0]:
                logger.warning("Face region is out of bounds")
                continue

            face = pixels[y1:y2, x1:x2]
            try:
                image = Image.fromarray(face)
                save_path = path.join(
                    base_path,
                    "output",
                    output_path,
                    f"{required_size[0]}x{required_size[1]}",
                )
                filename = f"{outname}_{i}.{output_format}"
                image = image.resize(required_size)
                saved_file = save_image(image, save_path, filename)
                logger.info(f"Written face to {saved_file}")
                draw.rectangle([x1, y1, x2, y2], outline="green", width=3)
            except Exception:
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
        save_path = path.join(base_path, "output")
        filename = f"{outname}_debug.jpg"
        saved_debug_file = save_image(image_main, save_path, filename)
        logger.info(f"Saving debug image to {saved_debug_file}")

