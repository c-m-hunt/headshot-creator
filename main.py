# check version of keras_vggface
import keras_vggface
from mtcnn import MTCNN
import matplotlib.pyplot as pyplot
from os import path, listdir
from PIL import Image
import numpy as np
import logging

logger = logging.getLogger("headshot_creator")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)

base_path = path.join(path.dirname(__file__), "input")

def add_padding(x1, y1, height, width, padding, aspect_ratio):
	original_aspect_ratio = width / height
	padding_top, padding_bottom = padding
	y1 = y1 - ((height / 100) * padding_top)
	height = height + ((height / 100) * sum(padding))
	new_width = aspect_ratio * height
	width_diff = new_width - width
	x1 = x1 - (width_diff / 2)
	width = new_width
	x2, y2 = x1 + width, y1 + height
	return int(x1), int(y1), int(x2), int(y2)

def get_faces(pixels):
	detector = MTCNN()
	return detector.detect_faces(pixels)

def extract_face(filename, outname, required_size=(500, 500)):
	logger.info(f"Looking for faces in {filename}")
	pixels = pyplot.imread(filename)
	results = get_faces(pixels)
	logger.info(f"Found {len(results)} faces")
	for i, result in enumerate(results):
		x1, y1, width, height = result['box']
		x1, y1, x2, y2 = add_padding(x1, y1, height, width, (40, 80), required_size[0] / required_size[1])
		face = pixels[y1:y2, x1:x2]
		image = Image.fromarray(face)
		savename = path.join(path.dirname(__file__), f"output/{outname}_{i}.jpg")
		image = image.resize(required_size)
		image.save(savename)
		logger.info(f"Written face to {savename}")


for file_in in listdir(base_path):
	if file_in.endswith(".jpg") or file_in.endswith(".jpeg"):
		filename = path.join(base_path, file_in)
		extract_face(filename, file_in.split(".")[0])
	else:
		continue