"""
Model to compare different versions of the same query to do the following:
    1. Mean features of the queries
    2. Find the threshold

Approach:
1. remove the silence from the query audio clips (VAD)
2. Taking no of frames of the features into consideration, take the feature matrix with median no of frames.
3. Map the features of these queries and take the mean value of the features in the mapped frame.
4. Similarly find variance matrix
"""
