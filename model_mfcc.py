from mfcc import FeatureExtractor
from SPRING import SPRING_DTW
import numpy as np
from readArk import read_scp
import matplotlib.pyplot as plt


# for eculidean distance of 2 vectors, use dist = numpy.linalg.norm(a-b)

class AQSearch():
    # initialize with the corpus audio file
    def __init__(self, c_audio_path):
        self.FE = FeatureExtractor()

        self.c_mfcc_feature_matrix = self.FE.mfcc(c_audio_path)
        pass



    # send the query file for searching in the corpus file.
    def search(self, q_audio_path):
        self.q_mfcc_feature_matrix = self.FE.mfcc(q_audio_path)

        sp = SPRING_DTW(220, self.q_mfcc_feature_matrix, self.c_mfcc_feature_matrix)
        matrix, matches = sp.main()

        print matches
        print len(matches)
        print matrix, matrix.shape
        fig, ax = plt.subplots()
        matrix = np.flipud(matrix)
        ax.matshow(matrix, cmap=plt.cm.OrRd)
        """for (i, j), z in np.ndenumerate(temp):
            if i == 0:
                ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
        """
        plt.show()


if __name__ == '__main__':
    c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
    q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'

    AQS = AQSearch(c_audio_path=c_wave_path)
    AQS.search(q_audio_path=q_wave_path)