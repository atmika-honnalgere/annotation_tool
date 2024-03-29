import os
import cv2
import numpy as np
import json
import shutil
from datetime import datetime
from PyQt5.QtGui import QImage

def process_contours_in_image(annotations, image, mask, contours, size, filename, via_style):
	file_key = filename + str(size)

	annotations['_via_img_metadata'][file_key] = {}
	annotations['_via_img_metadata'][file_key]['filename'] = filename

	if via_style:
		annotations['_via_img_metadata'][file_key]['size'] = size

	annotations['_via_img_metadata'][file_key]['height'] = np.int(image.shape[0])
	annotations['_via_img_metadata'][file_key]['width'] = np.int(image.shape[1])

	annotations['_via_img_metadata'][file_key]['file_attributes'] = {} ##Empty
	annotations['_via_img_metadata'][file_key]['regions'] = []

	regions = []
	for contour in contours:
		x, y, w, h = cv2.boundingRect(contour)
		if w * h < image.shape[0] * image.shape[1]:
			cntr = {}
			cntr['shape_attributes'] = {}
			cntr['shape_attributes']['name'] = 'polygon'
			cntr['shape_attributes']['all_points_x'] = []
			cntr['shape_attributes']['all_points_y'] = []

			X = []
			Y = []
			for pt in contour:
				x = pt[0][0]
				y = pt[0][1]
				if x >= 0 and x < image.shape[1] and y >= 0 and y < image.shape[0]:
					X.append(np.int(x))
					Y.append(np.int(y))

			if len(X) > 0: ##or len(Y) > 0, both will be of equal length
				cntr['shape_attributes']['all_points_x'] = X
				cntr['shape_attributes']['all_points_y'] = Y

				cntr['region_attributes'] = {} ##Empty

				regions.append(cntr)

	annotations['_via_img_metadata'][file_key]['regions'] = regions

	return annotations

class JSONGenerator:
	def __init__(self):
		self.images_directory = ''
		self.masks_directory = ''
		self.image_paths = []
		self.mask_paths = []
		self.already_annotated = []
		self.image_contours = None

		self.current_image = None
		self.current_mask = None
		self.current_image_contours = []

		##via_img_metadata
		self.annotations = {}
		self.annotations['_via_img_metadata'] = {}

		self.accepted_annotations = {}
		self.accepted_annotations['_via_img_metadata'] = {}

		self.time_string = datetime.now().strftime("%m-%d-%Y||%H:%M:%S")

	def load_paths(self):
		for filename in os.listdir(self.images_directory):
			if filename not in self.already_annotated:
				path = os.path.join(self.images_directory, filename)
				if os.path.isfile(path) and cv2.imread(path) is not None:
					file_name = filename.split('.')[0]
					for mask_name in os.listdir(self.masks_directory):
						mask_path = ''
						if mask_name.find(file_name) >= 0:
							if self.images_directory == self.masks_directory: 
								if len(mask_name) > len(filename):
									mask_path = os.path.join(self.masks_directory, mask_name)
							else:
								mask_path = os.path.join(self.masks_directory, mask_name)
							if os.path.isfile(mask_path) and cv2.imread(mask_path) is not None:
								self.image_paths.append(path)
								self.mask_paths.append(mask_path)
								break

		return self.image_paths, self.mask_paths

	def set_directories(self, images_directory, masks_directory, annotations_file=None):
		self.images_directory = os.path.join(images_directory, '') ##add trailing seperator
		self.masks_directory = masks_directory

		contours_file = os.path.join(masks_directory, 'contours.json')
		if os.path.isfile(contours_file):
			self.image_contours = json.load(open(contours_file, 'r'))

		if len(annotations_file) > 0:
			old_annotations = json.load(open(annotations_file, 'r'))

			if '_via_img_metadata' not in old_annotations.keys():
				return False

			self.already_annotated = [filedata['filename'] for filedata in old_annotations['_via_img_metadata'].values()]
			
			for key in old_annotations['_via_img_metadata'].keys():
				if 'accepted' in old_annotations['_via_img_metadata'][key].keys():
					if old_annotations['_via_img_metadata'][key]['accepted']:
						self.accepted_annotations['_via_img_metadata'][key] = old_annotations['_via_img_metadata'][key]
					else:
						self.annotations['_via_img_metadata'][key] = old_annotations['_via_img_metadata'][key]

				else:
					self.annotations['_via_img_metadata'][key] = old_annotations['_via_img_metadata'][key]
					
		return True

	def _style_annotations_for_VIA(self):
		if "_via_settings" not in self.annotations.keys():
			##via_settings
			self.annotations["_via_settings"] = {}
			self.annotations["_via_settings"]["ui"] = {}
			self.annotations["_via_settings"]["ui"]["annotation_editor_height"] = 25
			self.annotations["_via_settings"]["ui"]["annotation_editor_fontsize"] = 0.8
			self.annotations["_via_settings"]["ui"]["leftsidebar_width"] = 18

			self.annotations["_via_settings"]["ui"]["image_grid"] = {}
			self.annotations["_via_settings"]["ui"]["image_grid"]["img_height"] = 80
			self.annotations["_via_settings"]["ui"]["image_grid"]["rshape_fill"] = "none"
			self.annotations["_via_settings"]["ui"]["image_grid"]["rshape_fill_opacity"] = 0.3
			self.annotations["_via_settings"]["ui"]["image_grid"]["rshape_stroke"] = "yellow"
			self.annotations["_via_settings"]["ui"]["image_grid"]["rshape_stroke_width"] = 2
			self.annotations["_via_settings"]["ui"]["image_grid"]["show_region_shape"] = True
			self.annotations["_via_settings"]["ui"]["image_grid"]["show_image_policy"] = "all"

			self.annotations["_via_settings"]["ui"]["image_grid"]["image"] = {}
			self.annotations["_via_settings"]["ui"]["image_grid"]["image"]["region_label"] = "__via_region_id__"
			self.annotations["_via_settings"]["ui"]["image_grid"]["image"]["region_color"] = "__via_default_region_color__"
			self.annotations["_via_settings"]["ui"]["image_grid"]["image"]["region_label_font"] = "10px Sans"
			self.annotations["_via_settings"]["ui"]["image_grid"]["image"]["on_image_annotation_editor_placement"] = "NEAR_REGION"

			self.annotations["_via_settings"]["core"] = {}
			self.annotations["_via_settings"]["core"]["buffer_size"] = "18"
			self.annotations["_via_settings"]["core"]["filepath"] = {}
			self.annotations["_via_settings"]["core"]["filepath"][self.images_directory] = 1
			self.annotations["_via_settings"]["core"]["default_filepath"] = self.images_directory

			self.annotations["_via_settings"]["project"] = {}
			self.annotations["_via_settings"]["project"]["name"] = 'Model_Retraining_Annotations_' + self.time_string

		if "_via_attributes" not in self.annotations.keys():
			##via_attributes
			self.annotations["_via_attributes"] = {}
			self.annotations["_via_attributes"]["region"] = {}
			self.annotations["_via_attributes"]["file"] = {}

	def generate_rejected_contour_data(self, image_path, mask_path, via_style):
		if self.current_image is None:
			self.current_image = cv2.imread(image_path)

		if self.current_mask is None:
			self.current_mask = cv2.imread(mask_path)

		filename = image_path.split(os.path.sep)[-1]

		if via_style:
			self._style_annotations_for_VIA()

		if self.current_image is not None and self.current_mask is not None:
			if len(self.current_image_contours) == 0:
				if self.image_contours is not None and filename in self.image_contours.keys():
					self.current_image_contours = self.image_contours[filename]
				else:
					_, _, contour_image = cv2.split(self.current_mask)
					ret, contour_image = cv2.threshold(contour_image, 127, 255, cv2.THRESH_BINARY)
					self.current_image_contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

			if len(self.current_image_contours) > 0:
				self.current_image_contours = [np.array(contour, dtype=np.int64) for contour in self.current_image_contours]

			size = os.path.getsize(image_path)
			self.annotations = process_contours_in_image(self.annotations, self.current_image, self.current_mask, self.current_image_contours, size, filename, via_style)

			if len(self.annotations['_via_img_metadata'].keys()) > 0:
				with open(os.path.join(self.images_directory, 'annotations_rejected_%s.json'%self.time_string), 'w') as outfile:
					json.dump(self.annotations, outfile)

		if len(self.annotations['_via_img_metadata'].keys()) > 0:
			return self.annotations
		else:
			return None

	def generate_accepted_contour_data(self, image_path, mask_path, via_style):
		if self.current_image is None:
			self.current_image = cv2.imread(image_path)

		if self.current_mask is None:
			self.current_mask = cv2.imread(mask_path)

		filename = image_path.split(os.path.sep)[-1]

		if self.current_image is not None and self.current_mask is not None:
			if len(self.current_image_contours) == 0:
				if self.image_contours is not None and filename in self.image_contours.keys():
					self.current_image_contours = self.image_contours[filename]
				else:
					_, _, contour_image = cv2.split(self.current_mask)
					ret, contour_image = cv2.threshold(contour_image, 127, 255, cv2.THRESH_BINARY)
					self.current_image_contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

			if len(self.current_image_contours) > 0:
				self.current_image_contours = [np.array(contour, dtype=np.int64) for contour in self.current_image_contours]

			size = os.path.getsize(image_path)
			self.accepted_annotations = process_contours_in_image(self.accepted_annotations, self.current_image, self.current_mask, self.current_image_contours, size, filename, via_style)

			if len(self.annotations['_via_img_metadata'].keys()) > 0:
				with open(os.path.join(self.images_directory, 'annotations_accepted_%s.json'%self.time_string), 'w') as outfile:
					json.dump(self.accepted_annotations, outfile)

	def generate_JSON(self, via_style):
		if via_style:
			self._style_annotations_for_VIA()

		if len(self.image_paths) > 0 and len(self.mask_paths) > 0:
			for image_path, mask_path in zip(self.image_paths, self.mask_paths):
				self.current_image = None
				self.current_mask = None
				self.current_image_contours = []

				self.generate_rejected_contour_data(image_path, mask_path, via_style)

		with open(os.path.join(self.images_directory, 'annotations_rejected_%s.json'%self.time_string), 'w') as outfile:
			json.dump(self.annotations, outfile)

		if len(self.annotations['_via_img_metadata'].keys()) > 0:			
			return self.annotations
		else:
			return None

	def clear_annotations(self):
		self.images_directory = ''
		self.masks_directory = ''
		self.image_paths = []
		self.mask_paths = []
		self.already_annotated = []
		self.image_contours = None
		
		self.current_image = None
		self.current_mask = None
		self.current_image_contours = []

		##via_img_metadata
		self.annotations = {}
		self.annotations['_via_img_metadata'] = {}

		##via_img_metadata
		self.accepted_annotations = {}
		self.accepted_annotations['_via_img_metadata'] = {}

		self.time_string = datetime.now().strftime("%m-%d-%Y||%H:%M:%S")

	def save_annotations(self, via_style):
		if via_style:
			self._style_annotations_for_VIA()

		for key in self.accepted_annotations['_via_img_metadata'].keys():
			self.accepted_annotations['_via_img_metadata'][key]['accepted'] = True
		
		for key in self.annotations['_via_img_metadata'].keys():
			self.annotations['_via_img_metadata'][key]['accepted'] = False

		for key in self.accepted_annotations['_via_img_metadata'].keys():
			self.annotations['_via_img_metadata'][key] = self.accepted_annotations['_via_img_metadata'][key]

		if len(self.annotations['_via_img_metadata'].keys()) > 0:
			with open(os.path.join(self.images_directory, 'annotations_saved_%s.json'%self.time_string), 'w') as outfile:
				json.dump(self.annotations, outfile)	

			return self.annotations

		else:
			return None

	def generate_display_image(self, image_path, mask_path):
		self.current_image = cv2.imread(image_path)
		self.current_mask = cv2.imread(mask_path)
		self.current_image_contours = []

		if self.current_image is not None and self.current_mask is not None:
			filename = image_path.split(os.path.sep)[-1]
			if len(self.current_image_contours) == 0:
				if self.image_contours is not None and filename in self.image_contours.keys():
					self.current_image_contours = self.image_contours[filename]
				else:
					_, _, contour_image = cv2.split(self.current_mask)
					ret, contour_image = cv2.threshold(contour_image, 127, 255, cv2.THRESH_BINARY)
					self.current_image_contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

			if len(self.current_image_contours) > 0:
				self.current_image_contours = [np.array(contour, dtype=np.int64) for contour in self.current_image_contours]
				display_mask = cv2.drawContours(self.current_mask, self.current_image_contours, -1, (0, 255, 0), 10)
			else:
				display_mask = self.current_mask

			display = np.concatenate([self.current_image, display_mask], axis=1)
			display = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)

			return QImage(display.data, display.shape[1], display.shape[0], display.strides[0], QImage.Format_RGB888)

		return None

	def convert_to_VIA(self, annotations_file, images_directory):
		self.annotations = json.load(open(annotations_file, 'r'))

		if '_via_img_metadata' not in self.annotations.keys():
			return False, None

		self.images_directory = images_directory

		for filekey in self.annotations['_via_img_metadata'].keys():
			filedata = self.annotations['_via_img_metadata'][filekey]
			keys = filedata.keys()

			# if 'size' not in keys:
			# 	size = os.path.getsize(os.path.join(images_directory, filedata['filename']))
			# 	filedata['size'] = size

			if 'height' not in keys or 'width' not in keys:
				image = cv2.imread(os.path.join(images_directory, filedata['filename']))

				if 'height' not in keys:
					filedata['height'] = image.shape[0]

				if 'width' not in keys:
					filedata['width'] = image.shape[1]

			self.annotations['_via_img_metadata'][filekey] = filedata

		self._style_annotations_for_VIA()

		with open(os.path.join(self.images_directory, 'annotations_via_%s.json'%self.time_string), 'w') as outfile:
			json.dump(self.annotations, outfile)

		return True, self.annotations

	def convert_to_training_JSON(self, annotations_file, images_directory):
		self.annotations = json.load(open(annotations_file, 'r'))

		if '_via_img_metadata' not in self.annotations.keys():
			return False, None

		self.images_directory = images_directory

		if "_via_settings" in self.annotations.keys():
			self.annotations.pop("_via_settings")

		if "_via_attributes" in self.annotations.keys():
			self.annotations.pop("_via_attributes")

		for filekey in self.annotations['_via_img_metadata'].keys():
			filedata = self.annotations['_via_img_metadata'][filekey]
			keys = filedata.keys()

			if 'size' in keys:
				filedata.pop('size')

			if 'height' not in keys or 'width' not in keys:
				image = cv2.imread(os.path.join(images_directory, filedata['filename']))

				if 'height' not in keys:
					filedata['height'] = image.shape[0]

				if 'width' not in keys:
					filedata['width'] = image.shape[1]

			self.annotations['_via_img_metadata'][filekey] = filedata

		with open(os.path.join(self.images_directory, 'annotations_training_%s.json'%self.time_string), 'w') as outfile:
			json.dump(self.annotations, outfile)

		return True, self.annotations

	def combine_annotations(self, original_file, additional_file, via_style, images_directory=None, additional_directory=None):
		self.annotations = json.load(open(original_file, 'r'))

		if '_via_img_metadata' not in self.annotations.keys():
			return 1, None

		additional_annotations = json.load(open(additional_file, 'r'))

		if '_via_img_metadata' not in additional_annotations.keys():
			return 2, None

		for filekey in additional_annotations['_via_img_metadata'].keys():
			filedata = additional_annotations['_via_img_metadata'][filekey]
			if additional_directory is not None:
				path = os.path.join(additional_directory, filedata['filename'])
				if os.path.isfile(path):
					self.annotations['_via_img_metadata'][filekey] = filedata
					shutil.copyfile(path, os.path.join(images_directory, filedata['filename']))
			else:
				return 3, None

		if via_style:
			if images_directory is not None:
				self.images_directory = images_directory

				for filekey in self.annotations['_via_img_metadata'].keys():

					filedata = self.annotations['_via_img_metadata'][filekey]
					keys = filedata.keys()

					# if 'size' not in keys:
					# 	size = os.path.getsize(os.path.join(images_directory, filedata['filename']))
					# 	filedata['size'] = size

					if 'height' not in keys or 'width' not in keys:
						image = cv2.imread(os.path.join(images_directory, filedata['filename']))

						if 'height' not in keys:
							filedata['height'] = image.shape[0]

						if 'width' not in keys:
							filedata['width'] = image.shape[1]

					self.annotations['_via_img_metadata'][filekey] = filedata

				self._style_annotations_for_VIA() 

		with open(os.path.join(self.images_directory, 'annotations_combined_%s.json'%self.time_string), 'w') as outfile:
			json.dump(self.annotations, outfile)

		return 0, self.annotations