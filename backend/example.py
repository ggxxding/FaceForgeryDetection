import numpy as np
from classifiers import *
from pipeline import *
import sys
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def main(method,path):
  print('!!!!!!!!!!!!!!!!!!!!!!!!',path)
  classifier = Meso4()
  if method == "df":
    classifier.load(sys.path[0]+'/weights/Meso4_DF.h5')

  global graph
  graph = tf.get_default_graph()

  dataGenerator = ImageDataGenerator(rescale=1. / 255)
  generator = dataGenerator.flow_from_directory(
    path,
    target_size=(256, 256),
    batch_size=1,
    class_mode='binary',
    subset='training')

# 3 - Predict
  X, y = generator.next()
  #print(X.shape)
  with graph.as_default():
    pred = classifier.predict(X)
  print('Predicted :', pred, '\nReal class :', y)
  return str(pred[0][0]*100)+'%'


# 4 - Prediction for a video dataset
'''
classifier.load('weights/Meso4_F2F.h5')

predictions = compute_accuracy(classifier, 'test_videos')
for video_name in predictions:
    print('`{}` video class prediction :'.format(video_name), predictions[video_name][0])
'''