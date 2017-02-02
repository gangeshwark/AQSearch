import argparse
from src import model_mfcc, model_ark, compare_queries as cq

help = """
Values accepted for module argument:
    1. mfcc
    2. bnf (default)
    3. compare
"""

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--module", help=help, nargs='?', required=True)
args = parser.parse_args()

if __name__ == '__main__':
    if args.module == 'mfcc':
        print "Performing DTW on MFCC Features"
        c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
        q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'
        AQS = model_mfcc.AQSearch(c_audio_path=c_wave_path)
        AQS.search(q_audio_path=q_wave_path)

    elif args.module == 'bnf':
        print "Performing DTW on Bottle Neck Features"
        AQS = model_ark.AQSearch()
        AQS.search()

    elif args.module == 'compare':
        d = cq.CompareQueries()
        d.build_mean_matrix()
