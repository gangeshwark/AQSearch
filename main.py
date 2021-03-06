import argparse
from src import model_mfcc, model_bnf, compare_queries as cq

help = """
    Features list: mfcc, bnf (default), compare
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--feature", help=help, nargs='?', required=True)
parser.add_argument("-q", "--query", help=help, nargs='?', required=False)
parser.add_argument("-c", "--corpus", help=help, nargs='?', required=False)
args = parser.parse_args()

if __name__ == '__main__':
    if args.feature == 'mfcc':
        print "Performing DTW on MFCC Features"
        c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
        q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'
        AQS = model_mfcc.AQSearch(c_audio_path=c_wave_path)
        AQS.search(q_audio_path=q_wave_path)

    elif args.feature == 'bnf':
        print "Performing DTW on Bottle Neck Features"
        q_path = args.query
        c_path = args.corpus
        AQS = model_bnf.AQSearch(q_path, c_path)

        AQS.search()

    elif args.feature == 'compare':
        print "Performing cross-DTW on Bottle Neck Features of sample queries"
        d = cq.CompareQueries()
        d.build_mean_matrix()
