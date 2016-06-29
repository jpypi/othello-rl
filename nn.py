#!/usr/bin/env python3

import math
import numpy as np
import random
import pickle
from scipy.special import expit


class NN:
    def __init__(self, layer_dims, learning_rate):
        self.learning_rate = learning_rate
        self.layer_dims = layer_dims
        self.layers = []
        for i in range(len(layer_dims)-1):
            self.layers.append(np.random.normal(0, 1, size=(layer_dims[i+1], layer_dims[i]+1)))

        self.activation_func  = None
        self.dactivation_func = None

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.layers, f)

    def load(self, filename):
        with open(filename, "rb") as f:
            self.layers = pickle.load(f)

    def mkVec(self, vector1D, add_bias = True):
        return np.reshape(vector1D, (len(vector1D), 1))

    def getOutput(self, input_vector):
        outputs = input_vector
        for i in range(len(self.layers)):
            outputs = activation(self.layers[i]@np.vstack((outputs, 1)))
        #outputs = softmax(self.layers[-1]@np.vstack((outputs, 1)))

        return outputs

    def backProp(self, sample, target):
        # Propagate forwards to get the network's layers' outputs
        outputs = [sample]
        for i in range(len(self.layers)):
            outputs.append(activation(self.layers[i].dot(np.vstack((outputs[i], 1)))))
        #outputs.append(softmax(self.layers[-1].dot(np.vstack((outputs[-1], 1)))))
        #print(outputs[-1])

        #final_out = self.layers[-1].dot(outputs[-1])
        #am = np.zeros_like(final_out)
        #am[np.argmax(final_out)] = 1
        #outputs.append(am)


        # These will still need to be multiplied by the output from the previous layer
        # e.g. layer_deltas[0]*outputs[-2]
        layer_deltas = np.empty(len(outputs) - 1, object)

        # Output layer is special
        layer_deltas[-1] = (target - outputs[-1]) * dactivation(outputs[-1]) #outputs[-1]*(1 - outputs[-1])

        #self.layers[-1] += self.learning_rate * np.c_[outputs[-2].T, 1] * layer_deltas[-1]

        # i == current layer; Walk backwards from second to last layer (Hence
        # start at -2, because len-1 is the last element) Also recall that
        # range "end" is exclusive.
        for i in range(len(layer_deltas) - 2, -1, -1):
            # Need to do i+1 because outputs[0] == the input sample, and i+1 is
            # the ith layer's output

            #layer_derivative = outputs[i+1] * (1 - outputs[i+1])
            layer_derivative = dactivation(outputs[i+1])

            # Compute the layer delta
            layer_deltas[i] = layer_derivative * (self.layers[i+1].T.dot(layer_deltas[i + 1])[:-1])

            # Update the weights
            #self.layers[i] += self.learning_rate * np.c_[outputs[i].T, 1] * layer_deltas[i]

        for i in range(len(self.layers)):
            # Because outputs[0] == input sample, layer[i] input == outputs[i]
            # This is delta_weights
            self.layers[i] += self.learning_rate * np.c_[outputs[i].T, 1] * layer_deltas[i]

        return outputs[-1]


def relu(x):
    return np.multiply(x > 0, x)

def drelu(x):
    return np.float64(x > 0)


def softmax(x):
    e = np.exp(x)
    return e/np.sum(e)


def activation(x):
    #return expit(x)
    ##return 1.7159 * math.tanh(2/3*x)
    #print(x)

    return np.tanh(x)#list(map(math.tanh, x))
    #return np.multiply(x > 0, x)


def dactivation(x):
    #v = expit(x)
    #return v*(1-v)
    #return 1 - math.tanh(x)**2

    return 1 - np.tanh(x)**2#list(map(lambda y: 1 - math.tanh(y)**2, x))
    #return np.float64(x > 0)
