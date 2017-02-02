"""
Model to compare different versions of the same query to do the following:
    1. Mean features of the queries
    2. Find the threshold

Approach:
1. remove the silence from the query audio clips (VAD) - currently done manually.
2. Taking no of frames of the features into consideration, take the feature matrix with median no of frames.
3. Map the features of these queries and take the mean value of the features in the mapped frame.
4. Similarly find variance matrix
"""
import matplotlib.pyplot as plt
import numpy as np

from SPRING import SPRING_DTW
from src.readArk import read_scp


class Dummy:
    def __init__(self):

        self.q1_bn_feature_matrix = read_scp('outdir/bnf_hello1/raw_bnfea_fbank_pitch.1.scp')
        self.q2_bn_feature_matrix = read_scp('outdir/bnf_hello2/raw_bnfea_fbank_pitch.1.scp')
        self.q3_bn_feature_matrix = read_scp('outdir/bnf_hello3/raw_bnfea_fbank_pitch.1.scp')
        self.q4_bn_feature_matrix = read_scp('outdir/bnf_hello4/raw_bnfea_fbank_pitch.1.scp')
        self.q5_bn_feature_matrix = read_scp('outdir/bnf_hello5/raw_bnfea_fbank_pitch.1.scp')
        self.q6_bn_feature_matrix = read_scp('outdir/bnf_hello6/raw_bnfea_fbank_pitch.1.scp')
        self.feature_array = [self.q1_bn_feature_matrix,
                              self.q2_bn_feature_matrix,
                              self.q3_bn_feature_matrix,
                              self.q4_bn_feature_matrix,
                              self.q5_bn_feature_matrix,
                              self.q6_bn_feature_matrix]
        self.n = len(self.feature_array)  # no of query samples

    def frame_length(self, matrix):
        """
        Function to return the number of frames in a feature matrix.
        """
        return matrix.shape[0]

    def median(self):
        m = []
        for x in xrange(self.n):
            m.append(self.frame_length(self.feature_array[x]))

        m.sort()
        print m
        if self.n % 2 == 0:
            val = m[self.n / 2]
        else:
            val = m[(self.n - 1) / 2]
        x = 0
        for x in xrange(self.n):
            if val == self.feature_array[x].shape[0]:
                break

        return x

    def change_range(self, matrix):
        newMatrix = np.ndarray(shape=matrix.shape)
        newMax = 1
        newMin = -1

        for r in xrange(matrix.shape[0]):
            # oldMin = np.amin(matrix[r])
            if r == 0:
                oldMin = np.amin(matrix[0])
            else:
                oldMin = np.amin(matrix[max(0, r - 40):r])
            oldMax = np.amax(matrix[r])
            for c in xrange(matrix.shape[1]):
                newMatrix[r][c] = (((matrix[r][c] - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin

        return newMatrix

    def build_mean_matrix(self):
        # 1. Find the median matrix
        median_matrix = self.median()
        print median_matrix

        # 2. find dtw of the median matrix with others

        for x in xrange(self.n):
            print "\nPerforming DTW on features of %d and %d" % (median_matrix, x)
            # if x == median_matrix:
            # continue
            sp = SPRING_DTW(2000, self.feature_array[x], self.feature_array[median_matrix])
            matrix, matches, start_end_data, paths = sp.main()
            print matches
            # matrix = np.flipud(matrix)
            matrix = self.change_range(matrix)
            # Plot heat map
            fig, ax = plt.subplots()
            ax.matshow(matrix, cmap=plt.cm.RdGy)
            path_xs = []
            path_ys = []
            for path in paths:
                print path
                path_x = []
                path_y = []
                for point in path:
                    path_x.append(point[0])
                    path_y.append(point[1])

                path_xs.append(path_x)
                path_ys.append(path_y)

            print len(path_xs), len(path_ys)
            for x in xrange(len(path_xs)):
                plt.plot(path_xs[x], path_ys[x])
            plt.show()

            for p in start_end_data:
                print p[0], p[1]


if __name__ == '__main__':
    d = Dummy()
    d.build_mean_matrix()
