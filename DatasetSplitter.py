import os
import shutil
import random
import json
import cv2
from datetime import datetime


class DatasetSplitter():
	def __init__(self):
		self.train_files = []
		self.val_files = []
		self.train_directory = ''
		self.val_directory = ''
		self.time_string = datetime.now().strftime("%m-%d-%Y||%H:%M:%S")

	def split_dataset(self, images_directory, annotations_file, split_ratio):
		annotations = json.load(open(annotations_file, 'r'))

		if '_via_img_metadata' not in annotations.keys():
			return 1, None
			
		annotations = list(annotations['_via_img_metadata'].values())

		image_files = []
		for a in annotations:
			filename = a['filename']
			path = os.path.join(images_directory, filename)
			if os.path.isfile(path):
				image = cv2.imread(path)
				if image is not None:
					image_files.append(path)

		print(len(image_files))

		if len(image_files) > 0:
			train_size = int(split_ratio * len(image_files))
			train_samples = random.sample(image_files, k=train_size)

			current_directory = os.path.join(images_directory, self.time_string)
			if not os.path.isdir(current_directory):
				os.mkdir(current_directory)

			self.train_directory = os.path.join(current_directory, 'train')
			self.val_directory = os.path.join(current_directory, 'val')
			if not os.path.isdir(self.train_directory):
				os.mkdir(self.train_directory)
			if not os.path.isdir(self.val_directory):
				os.mkdir(self.val_directory)

			for filepath in train_samples:
				filename = filepath.split(os.sep)[-1]
				shutil.move(filepath, os.path.join(self.train_directory, filename))
				image_files.remove(filepath)
				self.train_files.append(os.path.join(self.train_directory, filename))

			for filepath in image_files:
				filename = filepath.split(os.sep)[-1]
				shutil.move(filepath, os.path.join(self.val_directory, filename))
				self.val_files.append(os.path.join(self.val_directory, filename))

			return 0, current_directory

		else:
			return -1, None

	def generate_annotations(self, annotations_file):
		annotations = json.load(open(annotations_file, 'r'))

		if '_via_img_metadata' not in annotations.keys():
			return False

		annotations = annotations['_via_img_metadata']

		train_annotations = {}
		train_annotations['_via_img_metadata'] = {}
		if os.path.isdir(self.train_directory):
			if len(self.train_files) > 0:
				for filepath in self.train_files:
					size = os.path.getsize(filepath)
					filename = filepath.split(os.path.sep)[-1]
					file_key = filename + str(size)
					train_annotations['_via_img_metadata'][file_key] = annotations[file_key]

					with open(os.path.join(self.train_directory, 'train_annotations.json'), 'w') as outfile:
						json.dump(train_annotations, outfile)

		val_annotations = {}
		val_annotations['_via_img_metadata'] = {}
		if os.path.isdir(self.val_directory):
			if len(self.val_files) > 0:
				for filepath in self.val_files:
					size = os.path.getsize(filepath)
					filename = filepath.split(os.path.sep)[-1]
					file_key = filename + str(size)
					val_annotations['_via_img_metadata'][file_key] = annotations[file_key]

					with open(os.path.join(self.val_directory, 'val_annotations.json'), 'w') as outfile:
						json.dump(val_annotations, outfile)

		return True

	def reset(self):
		self.train_files = []
		self.val_files = []
		self.train_directory = ''
		self.val_directory = ''
		self.time_string = datetime.now().strftime("%m-%d-%Y||%H:%M:%S")