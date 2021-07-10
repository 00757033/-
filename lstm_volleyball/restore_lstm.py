import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf  # Version 1.0.0 (some previous versions are used in past commits)
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
#from tensorflow.python.keras.layers import  Input, Embedding, Dot, Reshape, Dense
#from tensorflow.python.keras.models import Model
from sklearn import metrics
import random
from random import randint
import time
import os

saver = tf.train.Saver()

with tf.Session() as sess:
    saver.restore(sess, "model/model.ckpt.index")
    print("Model restored.")
    print("all values %s" % sess.run(tf.global_variables()))
    print("v2 value : %s" % sess.run(v2))
