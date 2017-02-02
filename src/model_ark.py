import matplotlib.pyplot as plt
import numpy as np
from src.spring import SpringDTW
from src.readArk import read_scp


# TODO: class to play audio from a particular frame.
class AudioPlay:
    def __init__(self):
        pass

    def play(self, file_path, start, end):
        pass


class AQSearch:
    def __init__(self):
        """
        Initialize with the corpus audio file
        """
        self.c_bn_feature_matrix = 0
        self.q_bn_feature_matrix = 0

    @staticmethod
    def change_range(matrix):
        """
        Change the range of the values in the matrix by maintaining the ratio
        :param matrix: The matrix to change the range
        :return: the new matrix after changing the range
        """
        new_matrix = np.ndarray(shape=matrix.shape)
        new_max = 1000
        new_min = 0
        for r in xrange(matrix.shape[0]):
            old_min = np.amin(matrix[0]) if r == 0 else np.amin(matrix[max(0, r - 40):r])
            old_max = np.amax(matrix[r])
            for c in xrange(matrix.shape[1]):
                new_matrix[r][c] = (((matrix[r][c] - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
        return new_matrix

    def plot_distance(self, matrix, path_xs, path_ys):
        """
        Plots the distance matrix
        :param matrix: The distance matrix
        :param path_xs: The x co-ordinate values of the path
        :param path_ys: The y co-ordinate values of the path
        :return: None
        """
        fig, ax = plt.subplots()
        ax.matshow(matrix, cmap=plt.cm.RdGy)
        plt.show()

        plt.figure(1)
        plt.subplot(211)
        plt.plot(matrix[0], 'r-', matrix[50], 'b--', matrix[56], 'g-')

        plt.subplot(212)
        matrix = self.change_range(matrix)
        plt.plot(matrix[0], 'r-', matrix[50], 'b--', matrix[56], 'g-')

        plt.show()
        fig, ax = plt.subplots()
        ax.matshow(matrix, cmap=plt.cm.RdGy)
        for x in xrange(len(path_xs)):
            plt.plot(path_xs[x], path_ys[x])
        plt.show()

    # TODO: Add the method to flip the paths too
    @staticmethod
    def flip(matrix):
        """
        To flip the matrix upside down.
        :param matrix: The matrix to be flipped
        :return: the flipped matrix
        """
        return np.flipud(matrix)

    def search(self):
        """
        To search the corpus file for the occurrences of the query audio.
        :return: None
        """
        path_xs = []
        path_ys = []
        self.c_bn_feature_matrix = read_scp('outdir/bnf_allhello/raw_bnfea_fbank_pitch.1.scp')
        self.q_bn_feature_matrix = read_scp('outdir/bnf_hello1/raw_bnfea_fbank_pitch.1.scp')
        sp = SpringDTW(1000, self.q_bn_feature_matrix, self.c_bn_feature_matrix)
        matrix, matches, start_end_data, paths = sp.perform_dtw()
        matrix = self.flip(matrix)
        for path in paths:
            path_x = []
            path_y = []
            for point in path:
                path_x.append(point[0])
                path_y.append(point[1])
            path_xs.append(path_x)
            path_ys.append(path_y)

        self.plot_distance(matrix, path_xs, path_ys)


if __name__ == '__main__':
    c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
    q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'

    AQS = AQSearch()
    AQS.search()
