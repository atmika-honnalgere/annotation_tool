import cv2
import os
from datetime import datetime

from segmentation.detector import Detector

class MaskGenerator:
	def __init__(self):
		self.masks_directory = '' 
		self.detector = Detector()

	def set_masks_directory(self, images_directory):	
		self.masks_directory = os.path.join(images_directory, 'masks_' + datetime.now().strftime("%m-%d-%Y||%H:%M:%S"))
		if not os.path.isdir(self.masks_directory):
			os.mkdir(self.masks_directory)

		return self.masks_directory

	def load_weights(self, weights_path):
		self.detector.load_model(weights_path)

	def generate_mask(self, image_path):	
		mask = None
		instances, bounding_boxes, mask, splash = self.detector.detect(image_path)
		
		if mask is not None:
			cv2.imwrite(os.path.join(self.masks_directory, filename), mask)
			return True

		return False