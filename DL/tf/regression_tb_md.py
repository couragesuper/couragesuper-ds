import numpy as np
import tensorflow as tf
from tensorflow.python.client import timeline

run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
run_metadata = tf.RunMetadata()

tf.set_random_seed(1234)

with tf.name_scope('data'):
    with tf.name_scope('x'):
        x = tf.random_normal([100], mean=0.0, stddev=0.9, name='rand_normal_x')
    with tf.name_scope('y'):
        y_true = x * tf.constant(0.1, name='real_slope') + tf.constant(0.3, name='bias') + tf.random_normal([100], mean=0.0, stddev=0.05, name='rand_normal_y')

with tf.name_scope('W'):
    W = tf.Variable(tf.random_uniform([], minval=-1.0, maxval=1.0))
    tf.scalar_summary('function/W', W)

with tf.name_scope('b'):
    b = tf.Variable(tf.zeros([]))
    tf.scalar_summary('function/b', b)

with tf.name_scope('function'):
    y_pred = W * x + b
        

with tf.name_scope('error'):
    loss = tf.reduce_mean(tf.square(y_pred - y_true))
    tf.scalar_summary('error', loss)

with tf.name_scope('train'):
    optimizer = tf.train.GradientDescentOptimizer(0.05)
    train = optimizer.minimize(loss)

init = tf.initialize_all_variables()

sess = tf.Session()

merged = tf.merge_all_summaries()
writer = tf.train.SummaryWriter('/tmp/regression/run1', sess.graph)



sess.run(init)

for step in range(1, 101):
    _, summary_str, slope, intercept, error = sess.run([train, merged, W, b, loss],
                                                       options=run_options,
                                                       run_metadata=run_metadata)
    if step % 10 == 0:
        writer.add_summary(summary_str, step)
        print('Step %.3d ; W = %.5f ; b = %.5f; loss = %.5f' % (step, slope, intercept, error))
    if step % 50 == 0:
        writer.add_run_metadata(run_metadata, 'step%d' % step)


#trace = timeline.Timeline(step_stats=run_metadata.step_stats)

#with open('timeline.ctf.json', 'w') as outfile:
#    outfile.write(trace.generate_chrome_trace_format())
