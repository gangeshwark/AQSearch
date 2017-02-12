import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial

from src.readArk import read_scp


class Test_Spring:
    # HERE DEFINE
    # 1)Y_query consisting of numerical data points
    # 2)X_corpus consisting of numerical data points
    def __init__(self, eps, Y_query, X_corpus):
        self.Y_query = Y_query
        self.X_corpus = X_corpus

        # self.Y_query = [11, 6, 9, 4]
        # self.X_corpus = [5, 12, 6, 10, 6, 5, 13]

        # the threshold for the matching process has to be chosen by the user -
        # yet in reality the choice of threshold is a non-trivial problem regarding the quality of the matching process
        # Getting Epsilon from the user
        # epsilon = input("Please define epsilon: ")
        self.epsilon = float(eps)

        # SPRING
        # 1.Requirements
        self.m = len(self.Y_query)
        self.n = len(self.X_corpus)
        self.D_recent = [float("inf")] * (self.m)
        self.D_now = [0] * (self.m)
        self.S_recent = [0] * (self.m)
        self.S_now = [0] * (self.m)
        self.d_min = float("inf")
        self.T_s = float("inf")
        self.T_e = float("inf")
        self.check = 0

        # check/output
        self.matches = []
        self.dist_matrix = np.ndarray(shape=(len(self.Y_query), len(self.X_corpus)), dtype=float)
        self.dis = np.ndarray(shape=(len(self.Y_query), len(self.X_corpus)), dtype=float)
        self.start_end_dist_data = []

    # calculation of accumulated distance for each incoming value
    def accdist_calc(self, incoming_value, j):
        for i in range(self.m):
            self.dis[i][j] = spatial.distance.cosine(incoming_value, self.Y_query[i]) ** 2
            if i == 0:
                # self.D_now[i] = abs(incoming_value - self.Y_query[i]) ** 2
                self.D_now[i] = spatial.distance.cosine(incoming_value, self.Y_query[i]) ** 2
                self.dist_matrix[i][j] = self.D_now[i]
            else:

                self.D_now[i] = spatial.distance.cosine(incoming_value, self.Y_query[i]) ** 2 + min(self.D_now[i - 1],
                                                                                                    self.D_recent[i],
                                                                                                    self.D_recent[
                                                                                                        i - 1])
                self.dist_matrix[i][j] = self.D_now[i]

    # deduce starting point for each incoming value
    def startingpoint_calc(self, j):
        for i in range(self.m):
            if i == 0:
                # here j+1 instead of j, because of the program counting from 0 instead of from 1
                self.S_now[i] = j + 1
            else:
                if self.D_now[i - 1] == min(self.D_now[i - 1], self.D_recent[i], self.D_recent[i - 1]):
                    self.S_now[i] = self.S_now[i - 1]

                elif self.D_recent[i] == min(self.D_now[i - 1], self.D_recent[i], self.D_recent[i - 1]):
                    self.S_now[i] = self.S_recent[i]

                elif self.D_recent[i - 1] == min(self.D_now[i - 1], self.D_recent[i], self.D_recent[i - 1]):
                    self.S_now[i] = self.S_recent[i - 1]

    def perform_dtw(self):
        j = 0
        # 2.Calculation for each incoming point x.t - simulated here by simply calculating along the given static list
        for j in range(self.n):

            x = self.X_corpus[j]
            self.accdist_calc(x, j)
            self.startingpoint_calc(j)

            # Report any matching subsequence
            if self.D_now[self.m - 1] <= self.epsilon:
                if self.D_now[self.m - 1] <= self.d_min:
                    self.d_min = self.D_now[self.m - 1]
                    self.T_s = self.S_now[self.m - 1]
                    self.T_e = j + 1
                    print "REPORT: Distance " + str(self.d_min) + " with a starting point of " + str(
                        self.T_s) + " and ending at " + str(
                        self.T_e)

            # Identify optimal subsequence
            for i in range(self.m):
                if self.D_now[i] >= self.d_min or self.S_now[i] > self.T_e:
                    self.check += 1
            if self.check == self.m:
                print "MATCH: Distance " + str(self.d_min) + " with a starting point of " + str(
                    self.T_s) + " and ending at " + str(self.T_e)
                self.matches.append(str(self.d_min) + "," + str(self.T_s) + "," + str(self.T_e))
                self.start_end_dist_data.append([self.T_s, self.T_e, self.d_min])
                self.d_min = float("inf")
                self.T_s = float("inf")
                self.T_e = float("inf")
                self.check = 0
            else:
                self.check = 0

            # define the recently calculated distance vector as "old" distance
            for i in range(self.m):
                self.D_recent[i] = self.D_now[i]
                self.S_recent[i] = self.S_now[i]

        print self.matches

        # self.dist_matrix = np.flipud(self.dist_matrix)
        print self.dist_matrix

        plt.matshow(self.dist_matrix, cmap=plt.cm.RdGy)
        plt.show()
        plt.matshow(self.dis, cmap=plt.cm.RdGy)
        plt.show()
        paths = self.find_all_paths()
        path_xs = []
        path_ys = []
        for path in paths:
            path_x = []
            path_y = []
            for point in path:
                path_x.append(point[0])
                path_y.append(point[1])
            path_xs.append(path_x)
            path_ys.append(path_y)

        plt.matshow(self.dist_matrix, cmap=plt.cm.RdGy)
        for x in xrange(len(path_xs)):
            plt.plot(path_xs[x], path_ys[x])
        plt.show()

        return self.dist_matrix

    def find_path(self, data):
        """
        Find the path given a start and end points.
        :param data: contains the start and end data
        :return: the path
        """
        j = data[1]
        i = self.dist_matrix.shape[0]
        path = [[j, i]]
        i -= 1
        j -= 1
        while i > 0 and j > 0:
            if self.dist_matrix[i - 1, j] == min(self.dist_matrix[i - 1, j - 1], self.dist_matrix[i - 1, j],
                                                 self.dist_matrix[i, j - 1]):
                i -= 1
            elif self.dist_matrix[i, j - 1] == min(self.dist_matrix[i - 1, j - 1], self.dist_matrix[i - 1, j],
                                                   self.dist_matrix[i, j - 1]):
                j -= 1
            else:
                i -= 1
                j -= 1
            path.append([j, i])
        return path

    def find_all_paths(self):
        """
        Finds paths for all the set of start and end points.
        :return: paths
        """
        paths = []
        for x in self.start_end_dist_data:
            paths.append(self.find_path(x))

        return paths


if __name__ == '__main__':
    q_bn_feature_matrix = [11, 6, 9, 4]
    c_bn_feature_matrix = [5, 12, 6, 10, 6, 5, 13]
    c_bn_feature_matrix = read_scp('outdir/bnf_database/raw_bnfea_fbank_pitch.1.scp')
    q_bn_feature_matrix = read_scp('outdir/bnf_query/raw_bnfea_fbank_pitch.1.scp')
    eps = 100
    sp = Test_Spring(eps, q_bn_feature_matrix, c_bn_feature_matrix)
    sp.perform_dtw()
