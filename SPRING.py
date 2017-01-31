import numpy as np

"""
The threshold for the matching process has to be chosen by the user - yet in reality the choice of threshold is
a non-trivial problem regarding the quality of the matching process
"""


class SPRING_DTW:
    def __init__(self, eps, q_mfcc, c_mfcc):
        # HERE DEFINE
        # 1)template consisting of numerical data points
        # 2)stream consisting of numerical data points
        self.template = q_mfcc
        self.stream = c_mfcc

        self.epsilon = float(eps)

        # SPRING
        # 1.Requirements
        self.n = len(self.template)  # 71
        print "Length of template: " + str(self.n)

        self.D_recent = [float("inf")] * (self.n)
        self.D_now = [0] * (self.n)
        self.S_recent = [0] * (self.n)
        self.S_now = [0] * (self.n)
        """
        self.D_recent = np.full(self.template.shape[0], float("inf"), dtype=int)
        self.D_now = np.full(self.template.shape[0], 0, dtype=int)
        self.S_recent = np.full(self.template.shape[0], 0, dtype=int)
        self.S_now = np.full(self.template.shape[0], 0, dtype=int)
        """
        self.d_rep = float("inf")
        self.J_s = float("inf")
        self.J_e = float("inf")
        self.check = 0

        # check/output
        self.matches = []
        self.start_end_data = []

        self.dist_matrix = np.ndarray(shape=(self.template.shape[0], self.stream.shape[0]), dtype=float)

        print "DIST MATRIX Shape: ", self.dist_matrix.shape

    # calculation of accumulated distance for each incoming value
    def accdist_calc(self, incoming_value, template, Distance_new, Distance_recent, j):
        # for eculidean distance of 2 vectors, use dist = np.linalg.norm(a-b)
        for i in range(len(template)):
            if i == 0:
                Distance_new[i] = np.linalg.norm(incoming_value - template[i])
                self.dist_matrix[i][j] = Distance_new[i]
            else:
                Distance_new[i] = np.linalg.norm(incoming_value - template[i]) + min(Distance_new[i - 1],
                                                                                     Distance_recent[i],
                                                                                     Distance_recent[i - 1])
                self.dist_matrix[i][j] = Distance_new[i]

        return Distance_new

    # deduce starting point for each incoming value
    def startingpoint_calc(self, template_length, starting_point_recent, starting_point_new, Distance_new,
                           Distance_recent, j):
        for i in range(template_length):
            if i == 0:
                # here j+1 instead of j, because of the program counting from 0 instead of from 1
                starting_point_new[i] = j
            else:
                if Distance_new[i - 1] == min(Distance_new[i - 1], Distance_recent[i],
                                              Distance_recent[i - 1]):
                    starting_point_new[i] = starting_point_new[i - 1]
                elif Distance_recent[i] == min(Distance_new[i - 1], Distance_recent[i],
                                               Distance_recent[i - 1]):
                    starting_point_new[i] = starting_point_recent[i]
                elif Distance_recent[i - 1] == min(Distance_new[i - 1], Distance_recent[i],
                                                   Distance_recent[i - 1]):
                    starting_point_new[i] = starting_point_recent[i - 1]
        return starting_point_new

    def find_path(self, data):
        x = data[1]
        y = self.dist_matrix.shape[0]
        path = [[x, y]]
        i = y - 1
        j = x - 1
        while i > 0 and j > 0:
            if i == 0:
                j -= 1
            elif j == 0:
                i -= 1
            else:
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
        path.append([data[0], 0])
        return path

    def find_all_paths(self, ):
        paths = []
        for x in self.start_end_data:
            paths.append(self.find_path(x))

        return paths

    def main(self):
        l = len(self.stream)
        print "Length of stream: " + str(l)
        for j in range(l):

            x = self.stream[j]
            self.accdist_calc(x, self.template, self.D_now, self.D_recent, j)
            self.startingpoint_calc(self.n, self.S_recent, self.S_now, self.D_now, self.D_recent, j)

            # Report any matching subsequence
            if self.D_now[self.n - 1] <= self.epsilon:
                if self.D_now[self.n - 1] <= self.d_rep:
                    self.d_rep = self.D_now[self.n - 1]
                    self.J_s = self.S_now[self.n - 1]
                    self.J_e = j + 1
                    print "REPORT: Distance " + str(self.d_rep) + " with a starting point of " + str(
                        self.J_s) + " and ending at " + str(self.J_e)

            # Identify optimal subsequence
            for i in range(self.n):
                if self.D_now[i] >= self.d_rep or self.S_now[i] > self.J_e:
                    self.check = self.check + 1
            if self.check == self.n:
                print "MATCH: Distance " + str(self.d_rep) + " with a starting point of " + str(
                    self.J_s) + " and ending at " + str(self.J_e)
                self.matches.append(str(self.d_rep) + "," + str(self.J_s) + "," + str(self.J_e))
                self.start_end_data.append([self.J_s, self.J_e])
                self.d_rep = float("inf")
                self.J_s = float("inf")
                self.J_e = float("inf")
                self.check = 0
            else:
                self.check = 0

            # define the recently calculated distance vector as "old" distance
            for i in range(self.n):
                self.D_recent[i] = self.D_now[i]
                self.S_recent[i] = self.S_now[i]

        return self.dist_matrix, self.matches, self.start_end_data, self.find_all_paths()
