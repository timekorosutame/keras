import tensorflow as tf
from custom_loss import yolo_loss
from custom_metrics import metric_iou
from input_data import yolo_input_pippeline2


#<==============================_DISABLE_WARNINGS_==============================>
tf.logging.set_verbosity(tf.logging.ERROR)


#<======================_INPUT_DATA_======================>
'''
test = yolo_input_pippeline(
	num_imgs=200,  
	img_size=28, 
	cell_size=7, 
	min_object_size=3, 
	max_object_size=7, 
	num_objects=1,
	num_bboxes=2,
	channels=1,
	train=True)
'''
test = yolo_input_pippeline2(
	num_cells=4,
	num_objects=1,
	num_bboxes=2,
	return_offsets=0,
	data_dir='data/test')
imgs, bboxes = test


#<======================_LOAD_CLEAR_MODEL_======================>
with open('./saved_model/modelyolo_card.json', 'rt', encoding='utf-8') as fileobj:
	json_model = fileobj.read()
model = tf.keras.models.model_from_json(json_model)
model.compile(
	optimizer='adam',				
	loss=yolo_loss,
	metrics=[metric_iou,])		


#<======================_WEIGHTS_LOAD_======================>
model.load_weights('./weight/model_yolo_card_test2')


#<======================_EVALUATE_MODEL_======================>
evaluate = model.evaluate(imgs, bboxes, verbose=0)
print('lose: {}\nmy_accuracy: {}'.format(evaluate[0], evaluate[1]))