import tensorflow as tf
import numpy as np

n_inputs = 9
n_hidden = 54
n_hidden_2 = 27
n_outputs = 1
training_size = 2000

class QNetwork(object):
    def __init__(self):
        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.W1 = None
        self.W2 = None
        self.W3 = None
        self.state_input = None
        self.target_output = None

        #self.state_input_training = None
        #self.target_output_training = None

        self.error = None
        self.s6 = None
        self.s7 = None
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
        if model_exists:
            self.restore(self.sess)
            print 'model restored...'

    def build(self):
        self.state_input = tf.placeholder(tf.float32, (1, n_inputs), name='state_input')  # (n_inputs, )
        self.target_output = tf.placeholder(tf.float32, (1, n_outputs), name='target_output')  # (n_inputs, )


        #self.state_input_training = tf.placeholder(tf.float32, (training_size, n_inputs), name='state_input_training')
        #self.target_output_training = tf.placeholder(tf.float32, (training_size, n_outputs), name='target_output_training')

        self.b1 = tf.Variable([0.1] * n_hidden, name="b1")  # mala stala 0.1
        self.b2 = tf.Variable([0.1] * n_outputs, name="b2")
        self.b3 = tf.Variable([0.1] * n_hidden_2, name="b3")

        self.W1 = tf.Variable(tf.random_uniform([n_inputs, n_hidden], minval=-1, maxval=1), name="W1")
        self.W2 = tf.Variable(tf.random_uniform([n_hidden_2, n_outputs], minval=-1, maxval=1), name="W2")
        self.W3 = tf.Variable(tf.random_uniform([n_hidden, n_hidden_2], minval=-1, maxval=1), name="W2")

        #self.s6 = tf.nn.tanh(tf.add(tf.matmul(tf.nn.tanh(tf.add(tf.matmul(self.state_input, self.W1), self.b1)), self.W2), self.b2), name='s6')

        self.s6 = tf.nn.tanh(tf.add(tf.matmul(tf.nn.tanh(
            tf.add(tf.matmul(tf.nn.tanh(tf.add(tf.matmul(self.state_input, self.W1), self.b1)), self.W3), self.b3)),self.W2),self.b2),
            name='s6')

        self.loss = tf.nn.l2_loss(self.s6 - self.target_output, name="loss")
        self.train = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(self.loss)
        self.saver = tf.train.Saver(tf.trainable_variables())

        init = tf.global_variables_initializer()
        self.sess.run(init)

    def save(self):
        self.saver.save(self.sess, './ttt_model')

    def restore(self, session):
        self.saver.restore(session, './ttt_model')

    def train_model(self, state_train, target_train):
        for i in range(training_size):
            state = np.array(state_train[i]).reshape(1, n_inputs)  # shape (9,)
            target = np.array(target_train[i]).reshape(1, n_outputs)
            self.sess.run(self.train, feed_dict={self.state_input: state, self.target_output: target})

    def predict(self, state):
        state = np.array(state).reshape(1, n_inputs)  # shape (9,)
        return self.sess.run(self.s6, feed_dict={self.state_input: state})




# N = QNetwork()
# state=np.array([1,2,3,4,5,6,7,8,9])
# state2 = np.array([state, state])
# target = np.array([7,7])
# N.train_model(state2, target)
# print N.predict(state2)

