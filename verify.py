import tensorflow as tf
import numpy as np

DATASET_PATH = "volleyball/toss_round5/"
X_path = DATASET_PATH + "restore.txt"#"test_toss_X_round8.txt"
file = open(X_path, 'r')
X_ = np.array(
    [elem for elem in [
        row.split(',') for row in file
    ]],
    dtype=np.float32
)
file.close()
print(X_)
print(len(X_))
blocks = int(len(X_) / 18)
print( blocks )   
X_ = np.array(np.split(X_,blocks))
with tf.compat.v1.Session() as sess:
    new_saver = tf.compat.v1.train.import_meta_graph('tosslog4/toss_18_multiplayer.ckpt.meta')#log/123model.ckpt.meta
    new_saver.restore(sess,'tosslog4/toss_18_multiplayer.ckpt')#log/123model.ckpt
    y = tf.compat.v1.get_collection('pred_network')
   
    
    y=tf.argmax(y,2)+1

    #print(y)
    graph = tf.compat.v1.get_default_graph()
    input_x = graph.get_operation_by_name('input_x').outputs[0]
    keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
    zz=sess.run(y, feed_dict={input_x:X_,  keep_prob:1.0})[0]
    #zzz=zz.reshape(int(len(zz)/6),6)
    cnt=0
    for it in zz:
       print(cnt+1,':',it)
       cnt+=1
    #print(X_)
'''
    print(len(zz))
    #zz=sess.run(y, feed_dict={input_x:X_})[0]
    zzz=zz.reshape(int(len(zz)/2),2)
    print(zz.reshape(int(len(zz)/2),2))
    for it in zzz:
        grade = 0
        if it[0]==2:
           grade+=50
           print("0-14 right")
        if it[1]==4:
           grade+=50
        print("grade:",grade)
'''
    
