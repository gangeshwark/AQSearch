import scipy.io.wavfile
from python_speech_features import mfcc

class FeatureExtractor:
    def __init__(self):
        pass

    def mfcc(self, path):
        # wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
        #wave_path = '/Users/amblee0306/Desktop/RA2/my4Hellow.wav'
        # filenew = '/Users/amblee0306/Desktop/RA2/queryHellow.wav'
        wave_path = path

        rate, signal = scipy.io.wavfile.read(str(wave_path))

        mfcc_feat = mfcc(signal, samplerate=16000, winlen=0.020, winstep=0.01, numcep=20,
                         nfilt=24, nfft=512, lowfreq=0, highfreq=None, preemph=0.97, ceplifter=20, appendEnergy=True)

        print mfcc_feat
        print mfcc_feat.shape
        return mfcc_feat



#the audio signal from which to compute features. Should be an N*1 array.

#mfcc_feat=mfcc(signal,rate)

#the mfcc function returns a numpy array of size(NUMFRAMES by numcep) containing features.
#each row holds 1 feature vector
#numcep is the number of cepstrum to return, defauly 13.
#https://github.com/jameslyons/python_speech_features

