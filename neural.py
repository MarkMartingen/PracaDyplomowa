import tensorflow as tf
import numpy as np

n_inputs = 9
n_hidden = 27
n_outputs = 1


class QNetwork(object):
    def __init__(self):
        self.b1 = None
        self.b2 = None
        self.W1 = None
        self.W2 = None
        self.state_input = None
        self.target_output = None
        self.error = None
        self.s6 = None
        self.saver = None
        self.train = None
        self.loss = None
        self.sess = tf.Session()

        try:
            f = open('./ttt_model.meta', 'r')
            f.close()
            model_exists = True
        except IOError:
            model_exists = False

        self.build()
        #if model_exists:
         #   self.restore(self.sess)

    def build(self):
        self.state_input = tf.placeholder(tf.float32, (1, n_inputs), name='state_input')  # (n_inputs, )
        self.target_output = tf.placeholder(tf.float32, (1, n_outputs), name='target_output')  # (n_inputs, )
        self.b1 = tf.Variable([0.1] * n_hidden, name="b1")  # mala stala 0.1
        self.b2 = tf.Variable([0.1] * n_outputs, name="b2")
        self.W1 = tf.Variable(tf.random_uniform([n_inputs, n_hidden], minval=-1, maxval=1), name="W1")
        self.W2 = tf.Variable(tf.random_uniform([n_hidden, n_outputs], minval=-1, maxval=1), name="W2")
        self.s6 = tf.nn.softplus(tf.add(tf.matmul(tf.nn.softplus(tf.add(tf.matmul(self.state_input, self.W1), self.b1)),
                                                  self.W2), self.b2), name='s6')
        self.loss = tf.nn.l2_loss(self.s6 - self.target_output, name="loss")
        self.train = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(self.loss)
        self.saver = tf.train.Saver(tf.trainable_variables())

        init = tf.global_variables_initializer()
        self.sess.run(init)

    def save(self):
        self.saver.save(self.sess, './ttt_model')

    def restore(self, session):
        self.saver.restore(session, './ttt_model')

    def train_model(self, state, target):
        state = np.array(state).reshape(1, 9)  # shape (9,)
        target = np.array(target).reshape(1, 1)
        self.sess.run(self.train, feed_dict={self.state_input: state, self.target_output: target})

    def predict(self, state):
        state = np.array(state).reshape(1, 9)  # shape (9,)
        return self.sess.run(self.s6, feed_dict={self.state_input: state})

# def num_tensors(my_string):
#     num_tensors = len(tf.get_default_graph().get_operations())
#     print my_string, num_tensors


