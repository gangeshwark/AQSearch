# HERE DEFINE
# 1)template consisting of numerical data points
# 2)stream consisting of numerical data points
template = [1, 2, 0, 1, 2]
stream = [1, 1, 0, 1, 2, 3, 1, 0, 1, 2, 1, 1, 1, 2, 7, 4, 5]

# the threshold for the matching process has to be chosen by the user -
# yet in reality the choice of threshold is a non-trivial problem regarding the quality of the matching process
# Getting Epsilon from the user
epsilon = input("Please define epsilon: ")
epsilon = float(epsilon)

# SPRING
# 1.Requirements
n = len(template)
D_recent = [float("inf")] * (n)
D_now = [0] * (n)
S_recent = [0] * (n)
S_now = [0] * (n)
d_rep = float("inf")
J_s = float("inf")
J_e = float("inf")
check = 0

# check/output
matches = []


# calculation of accumulated distance for each incoming value
def accdist_calc(incoming_value, template, distance_new, distance_recent):
    for i in range(len(template)):
        if i == 0:
            distance_new[i] = abs(incoming_value - template[i])
        else:
            distance_new[i] = abs(incoming_value - template[i]) + min(distance_new[i - 1], distance_recent[i],
                                                                      distance_recent[i - 1])
    return distance_new


# deduce starting point for each incoming value
def startingpoint_calc(template_length, starting_point_recent, starting_point_new, distance_new, distance_recent):
    for i in range(template_length):
        if i == 0:
            # here j+1 instead of j, because of the programm counting from 0 instead of from 1
            starting_point_new[i] = j + 1
        else:
            if distance_new[i - 1] == min(distance_new[i - 1], distance_recent[i], distance_recent[i - 1]):
                starting_point_new[i] = starting_point_new[i - 1]

            elif distance_recent[i] == min(distance_new[i - 1], distance_recent[i], distance_recent[i - 1]):
                starting_point_new[i] = starting_point_recent[i]

            elif distance_recent[i - 1] == min(distance_new[i - 1], distance_recent[i], distance_recent[i - 1]):
                starting_point_new[i] = starting_point_recent[i - 1]
    return starting_point_new


# 2.Calculation for each incoming point x.t - simulated here by simply calculating along the given static list
for j in range(len(stream)):

    x = stream[j]
    accdist_calc(x, template, D_now, D_recent)
    startingpoint_calc(n, S_recent, S_now, D_now, D_recent)

    # Report any matching subsequence
    if D_now[n - 1] <= epsilon:
        if D_now[n - 1] <= d_rep:
            d_rep = D_now[n - 1]
            J_s = S_now[n - 1]
            J_e = j + 1
            print "REPORT: Distance " + str(d_rep) + " with a starting point of " + str(J_s) + " and ending at " + str(
                J_e)

    # Identify optimal subsequence
    for i in range(n):
        if D_now[i] >= d_rep or S_now[i] > J_e:
            check += 1
    if check == n:
        print "MATCH: Distance " + str(d_rep) + " with a starting point of " + str(J_s) + " and ending at " + str(J_e)
        matches.append(str(d_rep) + "," + str(J_s) + "," + str(J_e))
        d_rep = float("inf")
        J_s = float("inf")
        J_e = float("inf")
        check = 0
    else:
        check = 0

    # define the recently calculated distance vector as "old" distance
    for i in range(n):
        D_recent[i] = D_now[i]
        S_recent[i] = S_now[i]

    print matches
