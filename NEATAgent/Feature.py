import numpy as np
import math
from sklearn import neural_network


class RandomNeuralNetFeature(object):
    def __init__(self, input_dimension, output_dimension):
        # create random example
        state = [np.random.rand(input_dimension) for i in range(1)]

        test_phi = [np.random.rand(output_dimension) for i in range(1)]

        self.clf = neural_network.MLPRegressor(alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        self.clf.fit(state, test_phi)

    def phi(self, state):
        return self.clf.predict([state]).flatten()


class DiscretizedFeature(object):
    def __init__(self, input_dimension, output_dimension, intervals=None):
        self.input_dimension = input_dimension
        self.output_dimension = output_dimension
        if intervals:
            self.intervals = intervals  # is a 3d list

    def phi(self, state):
        """
        Takes State vector and returns a discretized feature vector of 1's or 0's
        :param state: 
        :return: feature vector of size outputDimension where each element is binary
        """

        featureData = np.zeros(self.output_dimension, dtype=float)
        count = 0
        for i in range(self.input_dimension):
            for j in range(len(self.intervals[i])):
                featureData[count] = self.discretise(state[i], self.intervals[i][j][0], self.intervals[i][j][1])
                count += 1

        return featureData


    @staticmethod
    def discretise(value, min_value, max_value):
        """
        Discretize the given value into 0 or 1 by checking if in the interval (min_value, max_value)
        :param value: 
        :param min_value: 
        :param max_value: 
        :return: 
        """
        # return 1.0 if value in range(min_value, max_value) else 0.0
        if min_value <= value <= max_value:
            return 1.0
        else:
            return 0.0


    @staticmethod
    def create_partition(min_value, max_value, partition_size):
        delta = 0.00000000001
        results = [] # could initialise this with array of zeros
        interval = math.fabs(max_value - min_value) / partition_size
        for i in range(partition_size):
            # save the minimal and maximum for each interval
            results.append((min_value + interval * i + delta, min_value + interval * (i + 1)))

        return results
