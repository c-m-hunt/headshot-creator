from typing import Tuple
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)
logger = logging.getLogger("headshot_creator")


def add_padding(
    x1: int,
    y1: int,
    height: int,
    width: int,
    padding: Tuple[int, int],
    aspect_ratio: float,
) -> Tuple[int, int, int, int]:
    original_aspect_ratio = width / height
    padding_top, padding_bottom = padding
    y1 = y1 - (height * padding_top)
    height = height + (height * sum(padding))
    new_width = aspect_ratio * height
    width_diff = new_width - width
    x1 = x1 - (width_diff / 2)
    width = new_width
    x2, y2 = x1 + width, y1 + height
    return int(x1), int(y1), int(x2), int(y2)
