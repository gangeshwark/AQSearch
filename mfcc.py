import scipy.io.wavfile
import numpy as np
import matplotlib
import wave
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from bob import ap
import sys

class FeatureExtractor():

    def __init__(self):
        pass

    def mfcc(self, path):
        # wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
        wave_path = path


        rate, signal = scipy.io.wavfile.read(str(wave_path))

        print rate
        print signal
        print len(signal)

        print len(signal) / rate  # no of seconds in corpus file

        win_length_ms = 20  # The window length of the cepstral analysis in milliseconds
        win_shift_ms = 10  # The window shift of the cepstral analysis in milliseconds
        n_filters = 24  # The number of filter bands
        n_ceps = 20  # The number of cepstral coefficients
        f_min = 0.  # The minimal frequency of the filter bank
        f_max = 8000.  # The maximal frequency of the filter bank
        delta_win = 2  # The integer delta value used for computing the first and second order derivatives
        pre_emphasis_coef = 0.97  # The coefficient used for the pre-emphasis
        dct_norm = True  # A factor by which the cepstral coefficients are multiplied
        mel_scale = True  # Tell whether cepstral features are extracted on a linear (LFCC) or Mel (MFCC) scale

        c = ap.Ceps(rate, win_length_ms, win_shift_ms, n_filters, n_ceps, f_min, f_max, delta_win, pre_emphasis_coef,
                    mel_scale, dct_norm)
        csignal = np.cast['float'](signal)  # vector should be in **float**
        mfcc = c(csignal)
        mfcc = np.delete(mfcc, 0, 1)
        print len(mfcc)  # number of frames
        print mfcc.shape
        print len(mfcc[0])  # no of elements
        print mfcc

        # Plot Query Audio
        q_audio = wave.open(wave_path, 'r')

        # Extract Raw Audio from Wav File
        signal = q_audio.readframes(-1)
        signal = np.fromstring(signal, 'Int16')

        # If Stereo
        if q_audio.getnchannels() == 2:
            print 'Just mono files'
            sys.exit(0)
        """
        plt.figure(1)
        plt.title('Signal Wave...')
        plt.plot(signal)
        plt.show()
        """
        # Plot the features
        #fig = plt.figure()
        #ax = fig.gca(projection='3d')
        #ax.plot_surface(mfcc, mfcc, mfcc)
        return mfcc


"""
c_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/my4Hellow.wav'
q_wave_path = '/home/gangeshwark/PycharmProjects/AQSearch/data/queryHellow.wav'

crate, csignal = scipy.io.wavfile.read(str(c_wave_path))
qrate, qsignal = scipy.io.wavfile.read(str(q_wave_path))

print crate, qrate
print csignal, qsignal

print len(csignal)/crate # no of seconds in corpus file
print len(qsignal)/qrate # no of seconds in query file

win_length_ms = 20 # The window length of the cepstral analysis in milliseconds
win_shift_ms = 10 # The window shift of the cepstral analysis in milliseconds
n_filters = 24 # The number of filter bands
n_ceps = 20 # The number of cepstral coefficients
f_min = 0. # The minimal frequency of the filter bank
f_max = 8000. # The maximal frequency of the filter bank
delta_win = 2 # The integer delta value used for computing the first and second order derivatives
pre_emphasis_coef = 0.97 # The coefficient used for the pre-emphasis
dct_norm = True # A factor by which the cepstral coefficients are multiplied
mel_scale = True # Tell whether cepstral features are extracted on a linear (LFCC) or Mel (MFCC) scale

c = ap.Ceps(crate, win_length_ms, win_shift_ms, n_filters, n_ceps, f_min, f_max, delta_win, pre_emphasis_coef, mel_scale, dct_norm)
csignal = np.cast['float'](csignal) # vector should be in **float**
c_mfcc = c(csignal)
print len(c_mfcc) # number of frames
print c_mfcc.shape
print len(c_mfcc[0]) # no of elements

c = ap.Ceps(qrate, win_length_ms, win_shift_ms, n_filters, n_ceps, f_min, f_max, delta_win, pre_emphasis_coef, mel_scale, dct_norm)
qsignal = np.cast['float'](qsignal) # vector should be in **float**
q_mfcc = c(qsignal)
print len(q_mfcc) # number of frames
print q_mfcc.shape
print len(q_mfcc[0]) # no of elements
print q_mfcc

import sys

# Plot Query Audio
q_audio = wave.open(q_wave_path,'r')

#Extract Raw Audio from Wav File
signal = q_audio.readframes(-1)
signal = np.fromstring(signal, 'Int16')


#If Stereo
if q_audio.getnchannels() == 2:
    print 'Just mono files'
    sys.exit(0)

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()

c_audio = wave.open(c_wave_path,'r')
#Extract Raw Audio from Wav File
signal = c_audio.readframes(-1)
signal = np.fromstring(signal, 'Int16')


#If Stereo
if c_audio.getnchannels() == 2:
    print 'Just mono files'
    sys.exit(0)

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()


# Plot the features
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(q_mfcc, q_mfcc, q_mfcc)

"""
