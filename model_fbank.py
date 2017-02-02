from fbank import FeatureExtractor
from SPRING import SPRING_DTW
import numpy as np
import matplotlib.pyplot as plt


# for euclidean distance of 2 vectors, use dist = numpy.linalg.norm(a-b)

class AQSearch:
    # initialize with the corpus audio file
    def __init__(self, c_audio_path):
        self.FE = FeatureExtractor()

        self.c_fbank_feature_matrix = self.FE.fbank(c_audio_path)
        self.q_fbank_feature_matrix = 0
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

    # send the query file for searching in the corpus file.
    def search(self, q_audio_path):
        self.q_fbank_feature_matrix = self.FE.fbank(q_audio_path)

        sp = SPRING_DTW(443, self.q_fbank_feature_matrix, self.c_fbank_feature_matrix)
        matrix, matches, start_end_data, paths = sp.main()

        print matches
        print len(matches)
        print matrix, matrix.shape
        matrix = self.change_range(matrix)
        fig, ax = plt.subplots()
        matrix = np.flipud(matrix)
        ax.matshow(matrix, cmap=plt.cm.OrRd)
        """for (i, j), z in np.ndenumerate(temp):
            if i == 0:
                ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
        """
        plt.show()


if __name__ == '__main__':
    #c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
    #q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'
    c_wave_path = '/Users/amblee0306/Desktop/RA2/my4Hellow.wav'
    q_wave_path = '/Users/amblee0306/Desktop/RA2/queryHellow.wav'

    AQS = AQSearch(c_audio_path=c_wave_path)
    AQS.search(q_audio_path=q_wave_path)
