from mfcc import FeatureExtractor
from SPRING import SPRING_DTW
import numpy as np
from readArk import read_scp
import matplotlib.pyplot as plt


# for euclidean distance of 2 vectors, use dist = numpy.linalg.norm(a-b)

# class to play audio from a particular frame.
class AudioPlay:
    def __init__(self):
        pass

    def play(self, file_path, start, end):
        pass


class AQSearch:
    # initialize with the corpus audio file
    def __init__(self):
        self.c_bn_feature_matrix = 0
        self.q_bn_feature_matrix = 0
        pass

    def change_range(self, matrix):
        newMatrix = np.ndarray(shape=matrix.shape)
        newMax = 1000
        newMin = 0

        for r in xrange(matrix.shape[0]):
            if r == 0:
                oldMin = np.amin(matrix[0])
            else:
                oldMin = np.amin(matrix[max(0, r - 40):r])
            oldMax = np.amax(matrix[r])
            for c in xrange(matrix.shape[1]):
                newMatrix[r][c] = (((matrix[r][c] - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
                # newMatrix[r][c] = (((matrix[r][c] - oldMin)/oldMax)-0.5)*2

        return newMatrix

    def distance_cost_plot(self, distances, path_x, path_y):
        im = plt.imshow(distances, interpolation='nearest', cmap='RdGy')
        plt.gca().invert_yaxis()
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()
        plt.colorbar()

        plt.show()

    def flip_path_matrix(self):
        pass

    # send the query file for searching in the corpus file.
    def search(self):
        # self.q_mfcc_feature_matrix = self.FE.mfcc(q_audio_path)
        path_xs = []
        path_ys = []
        path_x = []
        path_y = []
        self.c_bn_feature_matrix = read_scp('outdir/bnf_allhello/raw_bnfea_fbank_pitch.1.scp')
        self.q_bn_feature_matrix = read_scp('outdir/bnf_hello1/raw_bnfea_fbank_pitch.1.scp')

        sp = SPRING_DTW(1000, self.q_bn_feature_matrix, self.c_bn_feature_matrix)
        matrix, matches, start_end_data, paths = sp.main()

        # matrix = np.flipud(matrix)
        print matches
        print len(matches)

        for x in start_end_data:
            print x[0], x[1]

        # print matrix, matrix.shape
        # self.distance_cost_plot(matrix, path_xs, path_ys)

        fig, ax = plt.subplots()
        ax.matshow(matrix, cmap=plt.cm.RdGy)
        plt.show()

        '''
        ax.plot(matrix[0], 'r-', matrix[69], 'g-')
        matrix = self.change_range(matrix)
        ax.plot(matrix[0], 'r-', matrix[69], 'g-')
        '''
        plt.figure(1)
        plt.subplot(211)
        plt.plot(matrix[0], 'r-', matrix[50], 'b--', matrix[56], 'g-')

        plt.subplot(212)
        matrix = self.change_range(matrix)
        plt.plot(matrix[0], 'r-', matrix[50], 'b--', matrix[56], 'g-')
        plt.show()

        fig, ax = plt.subplots()
        ax.matshow(matrix, cmap=plt.cm.RdGy)
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
            print path_xs[x]
            print path_ys[x]
            print "\n"
            plt.plot(path_xs[x], path_ys[x])
        plt.show()

        """
        for (i, j), z in np.ndenumerate(temp):
            if i == 0:
                ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
        """

        import pyaudio
        import wave
        import sys


if __name__ == '__main__':
    c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
    q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'

    AQS = AQSearch()
    AQS.search()
