import tensorflow as tf
from custom_loss import yolo_loss
from custom_metrics import metric_iou
from input_data import yolo_input_pippeline
import matplotlib.pyplot as plt
import numpy as np
import bbox


#<==============================_DISABLE_WARNINGS_==============================>
tf.logging.set_verbosity(tf.logging.ERROR)


#<======================_INPUT_DATA_======================>
test = yolo_input_pippeline(
	num_imgs=5,  
	img_size=28, 
	cell_size=7, 
	min_object_size=3, 
	max_object_size=7, 
	num_objects=1,
	num_bboxes=2,
	channels=1,
	train=False)
imgs, bboxes, offsets = test

#<======================_LOAD_CLEAR_MODEL_======================>
with open('./saved_model/modelyolo_4.json', 'rt', encoding='utf-8') as fileobj:
	json_model = fileobj.read()
model = tf.keras.models.model_from_json(json_model)
model.compile(
	optimizer='adam',				
	loss=yolo_loss,
	metrics=[metric_iou])		


#<======================_WEIGHTS_LOAD_======================>
model.load_weights('./weight/model_yolo_4_test1')


#<======================_MODEL_PREDICT_======================>
bboxes = model.predict(imgs)

bboxes = np.reshape(bboxes, [-1, 4, 4, 2, 5])

bboxes_batch, confidences = bbox.loss_to_labels(bboxes, offsets, 4, 2, 28)
imgs = bbox.restore_imgs(imgs)
imgs = np.reshape(imgs, [-1, 28, 28])

print('\nbbox:\n', bboxes_batch)
bbox.build_bboxes(imgs, bboxes_batch)


#print('\nconfidences:\n{}\n\n'.format(confidences))
