import tensorflow as tf
import numpy as np
import bbox as bx
from os.path import isfile, join
import os
import dataGen
import matplotlib.pyplot as plt

'''
data inputs format:
data = train, test
features_1, labels_1 = train
features_2, labels_2 = test
'''


def load_data():
	data = tf.keras.datasets.mnist.load_data()
	train,test = data
	f1,l1 = train
	f2,l2 = test
	f1 = f1/np.float32(255)+0.001
	f2 = f2/np.float32(255)+0.001
	l1 = tf.keras.utils.to_categorical(l1, 10)
	l2 = tf.keras.utils.to_categorical(l2, 10)

	train = f1, l1
	test = f2, l2
	data = train, test
	return data


def transform_to_conv(data):
	train, test = data
	f1,l1 = train
	f2,l2 = test
	f1 = np.reshape(f1,(-1, 28, 28, 1))
	f2 = np.reshape(f2,(-1, 28, 28, 1))
	train = f1, l1
	test = f2, l2
	data = train,test
	return data


def transform_to_dense(data):
	train, test = data
	f1,l1 = train
	f2,l2 = test
	f1 = np.reshape(f1,(-1, 784))
	f2 = np.reshape(f2,(-1, 784))
	train = f1, l1
	test = f2, l2
	data = train,test
	return data


def yolo_input_pippeline(
	num_imgs,  
	img_size, 
	cell_size, 
	min_object_size, 
	max_object_size, 
	num_objects,
	num_bboxes,
	channels,
	train=True):
	# CREATE
	imgs, bboxes = bx.create_rect(num_imgs, img_size, min_object_size, max_object_size, num_objects, channels)
	# NORMALIZE IMG
	imgs = bx.normalize_img(imgs)
	# TRANSFORM TO YOLO SHAPE
	num_cells = int(img_size/cell_size)
	# NORMALIZE+TRANSFORM BBOXES
	bboxes, offsets = bx.labels_to_loss(bboxes,num_cells,num_bboxes,img_size,num_imgs)

	if train:
		return (imgs, bboxes)
	else:
		return (imgs, bboxes, offsets)

# зображення та bbox з data_dir -> датасет
def yolo_input_pippeline2 (num_cells, num_objects, num_bboxes, train=True):
	bboxes = bx.bbox_from_file(data_file='./data/code_labels.txt', num_objects=num_objects)
	imgs = bx.img_from_file(data_dir='./data/code')
	imgs = bx.normalize_img(imgs)
	num_imgs, img_size = imgs.shape[0:2]
	bboxes, offsets = bx.labels_to_loss(bboxes, num_cells, num_bboxes, img_size, num_imgs)

	if train:
		return (imgs, bboxes)
	else:
		return (imgs, bboxes, offsets)



if __name__ == '__main__':
	'''
	data_dir = r'E:\programming\python\study\tutorials\keras\img_labeling\BBox-Label-Tool\Images\002'
	save_dir = r'E:\programming\python\study\tutorials\keras\img_labeling\BBox-Label-Tool\Images\004'
	dataGen.DataSetGenerator(data_dir).resize_imgs(save_dir=save_dir, size=(128,128))
	'''
	imgs,bboxes,offsets = yolo_input_pippeline2(num_cells=4, num_objects=1, num_bboxes=2, train=False)
	bboxes_batch, confidences = bx.loss_to_labels(bboxes, offsets, num_cells=4, num_bboxes=2, img_size=128)
	imgs = bx.restore_imgs(imgs)
	imgs = np.reshape(imgs, [-1, 128, 128, 3])
	bx.build_bboxes(imgs, bboxes_batch)