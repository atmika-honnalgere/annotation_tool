import cv2
import os
from datetime import datetime
import json
import numpy as np

from segmentation.detector import Detector

class MaskGenerator:
	def __init__(self):
		self.masks_directory = '' 
		self.detector = Detector()
		self.contours_data = {}

	def set_masks_directory(self, images_directory):	
		self.masks_directory = os.path.join(images_directory, 'masks_' + datetime.now().strftime("%m-%d-%Y||%H:%M:%S"))
		if not os.path.isdir(self.masks_directory):
			os.mkdir(self.masks_directory)

		return self.masks_directory

	def load_weights(self, weights_path):
		self.detector.load_model(weights_path)
		self.contours_data = {}

	def generate_mask(self, image, filename):	
		mask = None
		instances, contours, mask = self.detector.get_object_contours_from_image(image)
		contours = [contour.astype(int).tolist() for contour in contours]
		
		if mask is not None:
			cv2.imwrite(os.path.join(self.masks_directory, filename), mask)

			if len(contours) > 0:
				self.contours_data[filename] = contours
				with open(os.path.join(self.masks_directory, 'contours.json'), 'w') as outfile:
					json.dump(self.contours_data, outfile)
				
			return True

		return False

	def reset(self):
		self.masks_directory = '' 
		self.detector = Detector()
		self.contours_data = {}