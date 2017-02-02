import scipy.io.wavfile
from python_speech_features import logfbank

class FeatureExtractor:
    def __init__(self):
        pass

    def fbank(self, path):
        # wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
        #wave_path = '/Users/amblee0306/Desktop/RA2/my4Hellow.wav'
        # filenew = '/Users/amblee0306/Desktop/RA2/queryHellow.wav'
        wave_path = path

        rate, signal = scipy.io.wavfile.read(str(wave_path))

        fbank_feat = logfbank(signal, samplerate=16000, winlen=0.020, winstep=0.01,
                           nfilt=24, nfft=512, lowfreq=0, highfreq=None, preemph=0.97)

        #print fbank_feat
        #print fbank_feat.shape
        return fbank_feat

