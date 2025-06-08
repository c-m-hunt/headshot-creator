from typing import Tuple


def add_padding(
    x1: int,
    y1: int,
    height: int,
    width: int,
    padding: Tuple[int, int],
    aspect_ratio: float,
) -> Tuple[int, int, int, int]:
    """
    Add padding to the bounding box coordinates based on the specified aspect ratio and padding values.
    :param x1: The x-coordinate of the top-left corner of the bounding box.
    :param y1: The y-coordinate of the top-left corner of the bounding box.
    :param height: The height of the bounding box.
    :param width: The width of the bounding box.
    :param padding: A tuple containing the padding values for top and bottom (padding_top, padding_bottom).
    :param aspect_ratio: The desired aspect ratio for the bounding box.
    :return: A tuple containing the new coordinates of the bounding box (x1, y1, x2, y2).
    """
    padding_top, padding_bottom = padding
    y1 = y1 - (height * padding_top)
    height = height + (height * sum(padding))
    new_width = aspect_ratio * height
    width_diff = new_width - width
    x1 = x1 - (width_diff / 2)
    width = new_width
    x2, y2 = x1 + width, y1 + height
    return int(x1), int(y1), int(x2), int(y2)
