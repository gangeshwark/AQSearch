from mfcc import FeatureExtractor
from SPRING import SPRING_DTW
import numpy as np
from readArk import read_scp
import matplotlib.pyplot as plt


# for eculidean distance of 2 vectors, use dist = numpy.linalg.norm(a-b)
class AudioPlay():
    def __init__(self):
        pass

    def play(self, file_path, start, end):
        pass


class AQSearch():
    # initialize with the corpus audio file
    def __init__(self, c_audio_path):
        # self.FE = FeatureExtractor()

        # self.c_mfcc_feature_matrix = self.FE.mfcc(c_audio_path)
        # print self.c_mfcc_feature_matrix
        pass

    def change_range(self, matrix):
        newMatrix = np.ndarray(shape=matrix.shape)
        newMax = 1
        newMin = -1
        for x in xrange(matrix.shape[0]):
            oldMin = min(matrix[x])
            oldMax = max(matrix[x])
            for y in xrange(matrix.shape[1]):
                newMatrix[x][y] = (((matrix[x][y] - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin

        return newMatrix

    # send the query file for searching in the corpus file.
    def search(self, q_audio_path):
        # self.q_mfcc_feature_matrix = self.FE.mfcc(q_audio_path)
        self.c_bn_feature_matrix = read_scp('outdir/bnf_database/raw_bnfea_fbank_pitch.1.scp')
        self.q_bn_feature_matrix = read_scp('outdir/bnf_query/raw_bnfea_fbank_pitch.1.scp')

        sp = SPRING_DTW(1000, self.q_bn_feature_matrix, self.c_bn_feature_matrix)
        matrix, matches, start_end_data = sp.main()
        matrix = self.change_range(matrix)
        print matches
        print len(matches)

        for x in start_end_data:
            print x[0], x[1]
        # print matrix, matrix.shape
        fig, ax = plt.subplots()
        matrix = np.flipud(matrix)
        ax.matshow(matrix, cmap=plt.cm.RdGy)
        """
        for (i, j), z in np.ndenumerate(temp):
            if i == 0:
                ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
        """
        plt.show()



        import pyaudio
        import wave
        import sys


if __name__ == '__main__':
    c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
    q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'

    AQS = AQSearch(c_audio_path=c_wave_path)
    AQS.search(q_audio_path=q_wave_path)
