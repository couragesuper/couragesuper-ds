import tensorflow as tf
from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets
from tensorflow.contrib.layers.python.layers import layers
from tensorflow.contrib.layers.python.layers import summaries
from tensorflow.contrib.layers.python.layers import regularizers
from tensorflow.contrib.framework.python.ops import arg_scope
from tensorflow.python.client import timeline


tf.set_random_seed(1234)

run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
run_metadata = tf.RunMetadata()

mnist = read_data_sets("/tmp/MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y_true = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32, [])


def slim_net_original(image, keep_prob):
    with arg_scope([layers.conv2d, layers.fully_connected], biases_initializer=tf.random_normal_initializer(stddev=0.1)):

        # conv2d(inputs, num_outputs, kernel_size, stride=1, padding='SAME',
        # activation_fn=nn.relu, normalizer_fn=None, normalizer_params=None,
        # weights_initializer=initializers.xavier_initializer(), weights_regularizer=None,
        # biases_initializer=init_ops.zeros_initializer, biases_regularizer=None, scope=None):
        net = layers.conv2d(image, 32, [5, 5], scope='conv1', weights_regularizer=regularizers.l1_regularizer(0.5))

        # max_pool(inputs, kernel_size, stride=2, padding='VALID', scope=None)
        net = layers.max_pool2d(net, 2, scope='pool1')

        net = layers.conv2d(net, 64, [5, 5], scope='conv2', weights_regularizer=regularizers.l2_regularizer(0.5))
        summaries.summarize_tensor(net, tag='conv2')

        net = layers.max_pool2d(net, 2, scope='pool2')

        net = layers.flatten(net, scope='flatten1')

        # fully_connected(inputs, num_outputs, activation_fn=nn.relu, normalizer_fn=None,
        # normalizer_params=None, weights_initializer=initializers.xavier_initializer(),
        # weights_regularizer=None, biases_initializer=init_ops.zeros_initializer,
        # biases_regularizer=None, scope=None):
        net = layers.fully_connected(net, 1024, scope='fc1')

        # dropout(inputs, keep_prob=0.5, is_training=True, scope=None)
        net = layers.dropout(net, keep_prob=keep_prob, scope='dropout1')

        net = layers.fully_connected(net, 10, scope='fc2')
    return net


y_pred = slim_net_original(tf.reshape(x, [-1, 28, 28, 1]), keep_prob)

with tf.name_scope('x_ent'):
    cross_entropy = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(y_pred, y_true))
    summaries.summarize_tensor(cross_entropy, tag='x_ent')

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

with tf.name_scope('accuracy'):
    correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_true, 1))
    accuracy = tf.reduce_mean(tf.to_float(correct_prediction))
    summaries.summarize_tensor(accuracy, tag='acc')

sess = tf.Session()

merged = tf.merge_all_summaries()
writer = tf.train.SummaryWriter('/tmp/layers/run1', sess.graph)


sess.run(tf.initialize_all_variables())

for i in range(1, 101):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    _, summary_str = sess.run([train_step, merged],
                              feed_dict={x:batch_xs, y_true:batch_ys, keep_prob: 0.5},
                              options=run_options,
                              run_metadata=run_metadata)
    writer.add_summary(summary_str, i)
    if (i % 10) == 0:
        test_xs, test_ys = mnist.test.next_batch(100)
        #test_xs, test_ys = [mnist.test.images, mnist.test.labels]
        train_acc = sess.run(accuracy, feed_dict={x:batch_xs, y_true:batch_ys, keep_prob:1})
        test_acc = sess.run(accuracy, feed_dict={x:test_xs, y_true:test_ys, keep_prob:1})
        print('Step %.4d : train_err = %.2f%% ; test_err = %.2f%%' % (i, (1 - train_acc) * 100, (1 - test_acc) * 100))


trace = timeline.Timeline(step_stats=run_metadata.step_stats)

with open('/tmp/layers/timeline.ctf.json', 'w') as outfile:
    outfile.write(trace.generate_chrome_trace_format())
