import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# 1.make array x and y size of 100
n_retry = 100
np.random.seed(0)
x_arr = [ np.random.normal( 0.0 , 0.9 ) for i in range(0,n_retry) ]
y_arr = [ x_arr[i] * 0.1 + 0.3 + np.random.normal(0.0, 0.05) for i in range(0,n_retry) ]

# 2.show graph
if True :
    plt.plot( x_arr, y_arr , 'ro' )
    plt.legend()
    plt.show()

# 3. tensor flow
W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))
y = W * x_arr + b

loss = tf.reduce_mean(tf.square(y - y_arr))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

for step in range(101):
    sess.run(train)
    if step % 10 == 0:
        print(step, sess.run(W), sess.run(b))

plt.plot(x_arr, y_arr, 'ro')
plt.plot(x_arr, sess.run(W) * x_arr + sess.run(b))
plt.legend()
plt.show()

