from typing import Tuple, List, Dict
from mtcnn import MTCNN
import matplotlib.pyplot as pyplot
from os import path, listdir, makedirs
from PIL import Image
import numpy as np
import logging
import fire

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger("headshot_creator")

base_path = path.join(path.dirname(__file__), "input")

def add_padding(
	x1: int,
	y1: int,
	height: int,
	width: int,
	padding: Tuple[int, int],
	aspect_ratio: float
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

def get_faces(pixels: np.array) -> List[Dict]:
	detector = MTCNN()
	return detector.detect_faces(pixels)

def extract_faces(
	filename: str,
	outname: str,
	required_size: Tuple[int, int],
	padding: Tuple[int, int],
	confidence_threshold: float
):
	logger.info(f"Looking for faces in {filename}")
	pixels = pyplot.imread(filename)
	results = get_faces(pixels)
	logger.info(f"Found {len(results)} faces")
	for i, result in enumerate(results):
		if result["confidence"] > confidence_threshold:
			logger.info(f"Face found with confidence of {result['confidence']}")
			x1, y1, width, height = result['box']
			x1, y1, x2, y2 = add_padding(x1, y1, height, width, padding, required_size[0] / required_size[1])
			face = pixels[y1:y2, x1:x2]
			try:
				image = Image.fromarray(face)
				save_path = path.join(path.dirname(__file__), "output", f"{required_size[0]}x{required_size[1]}")
				filename = f"{outname}_{i}.jpg"
				image = image.resize(required_size)
				saved_file = save_image(image, save_path, filename)
				logger.info(f"Written face to {saved_file}")
			except:
				logger.warning('The calculated image goes beyond the bounds of the image. Try to make the padding smaller or adjust the aspect ratio.')
		else:
			logger.warning(f"Face found below confidence threshold at {result['confidence']}")

def save_image(image: Image, directory: str, filename: str) -> str:
	if not path.exists(directory):
		makedirs(directory)
	savename = path.join(directory, filename)
	image.save(savename)
	return savename

def start(
	padding: Tuple[int, int]=(0.4, 0.6),
	output_size: Tuple[int, int]=(400, 500),
	confidence_threshold: float=0.95
):
	logger.info(f"Running with padding of {padding}")
	logger.info(f"Running with required size of {output_size}")
	logger.info(f"Running with confidence threshold of {confidence_threshold}")
	for file_in in listdir(base_path):
		if file_in.endswith(".jpg") or file_in.endswith(".jpeg"):
			filename = path.join(base_path, file_in)
			extract_faces(filename, file_in.split(".")[0], output_size, padding, confidence_threshold)
		else:
			continue

if __name__ == '__main__':
  fire.Fire(start)