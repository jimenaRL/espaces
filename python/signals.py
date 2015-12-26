import pyaudio
import wave
import sys
import os

import numpy as np

import librosa
from moviepy.audio.io import ffmpeg_audiowriter
import audioread

class Signal():

    """Class handling audio signal

    A Signal is fairly a numpy array (called data) and a set of attributes

    Attributes
    ----------
    *data* : array
        a numpy array containing the signal data
    *n_chan* : int
        The number of channel
    *length* : int
        The length in samples (integer) of the signal
        (total dimension of the numpy array is n_chan x length)
    *fs* : int
        The sampling frequency
    *location* :  str , optional
        Where the original file is located on the disk
    *sample_width* : int
        Various bit format exist for wav file, this allows to handle it
    *is_normalized* : bool
        A boolean telling is the numpy array has been normalized
        (which here means its values are between -1 and 1)
    *energy* : float
        The energy (:math:`\sum_i x[i]^2`) of the array
    """

    # defaults attributes
    n_chan = 0
    length = 0
    fs = 0
    location = ""
    sample_width = 2
    is_normalized = False
    energy = 0

    # Constructor
    def __init__(self, data, fs=0, normalize=False, mono=False, crop=None):
        """ Simple constructor from a numpy array (data) or a path to an audio file 
    parameters
    ----------
    data: string, int or numpy array
        if string: file name to load the data from (can be any type supported by ffmpeg)
        if numpy array: array containing the signal data, shape is (length x channels)
    fs: int
        the sampling frequency
    normalize: bool, optionnal
        whether to normalize the signal (e.g. max will be 1)
    mono:  bool, optionnal
        keep only the first channel
    crop:  float list with 2 elements, optionnal
        crop the signal from the first element of the list (in seconds) to the second one

        """

        if crop and crop[0]>crop[1]:
            raise ValueError("Negative duration: %1.2fs (crop=[%1.2f,%1.2f])" %(crop[1]-crop[0],crop[0],crop[1]))


        if isinstance(data, str) and  os.path.exists(data): # init the signal with a file path
            self.load_from_file(data, crop, fs=fs)
            crop = None
        else:
            self.data = np.array(data)
            # remove any nans or infs data
            self.data[np.isnan(self.data)] = 0
            self.data[np.isinf(self.data)] = 0

            if len(self.data.shape) > 2:
                raise ValueError("Cannot process more than 2D arrays")

            if len(self.data.shape) > 1:
                if self.data.shape[0] < self.data.shape[1]:
                    # by convention channels are stored as columns
                    self.data = self.data.transpose()
            if fs > 0:
                self.fs = fs
            else:
                raise ValueError("Can not instantiate a signal from raw data without a sampling frequency")

        # Convert to mono if necessary (taking mean of channels)
        if mono and len(self.data.shape) == 2:
            self.data = self.data.mean(axis=1)

        # mono signals are stored as nx1 matrices instead of vector for code
        # simplification
        if len(self.data.shape) == 1:
            self.data = self.data.reshape((-1, 1))

        self.length = self.data.shape[0]
        self.n_chan = self.data.shape[1]

        # crop signal
        if crop is not None:
            self.crop(crop[0], crop[1])

        if normalize & (self.length > 0):
            print "Normalizing Signal"
            norm = self.data.max()
            self.data = self.data.astype(float) / float(norm)
            self.is_normalized = True

        self.energy = np.sum(self.data ** 2)

    def __getitem__(self, key):
        """
        get an excerpt of the signal using a slice as key (limits in seconds)
        """
        if isinstance(key, slice):
            if key.start:
                start_sample = key.start*self.fs
            else:
                start_sample = None
            if key.stop and key.stop<=self.get_duration():
                stop_sample = key.stop*self.fs
            else:
                stop_sample = None
            return Signal(self.data[start_sample:stop_sample, :], self.fs, normalize=False)
        else:
            raise TypeError("Argument not recognized as a slice")


    def load_from_file(self, file_name, crop=None, fs=None):

        self.location = file_name

        if fs == 0:
            fs = None

        offset = 0.0
        duration = None
        if crop:
            offset = crop[0]
            duration = crop[1] - crop[0]

        self.data, self.fs = librosa.load(file_name, mono=False, sr=fs,
                                          offset=offset, duration=duration,
                                          dtype=np.float64)

        self.data = self.data.T

    def plot(self, pltStr="b-", legend=None):
        """ plot the array using matplotlib """
        import matplotlib.pyplot as plt
        plt.plot(self.data, pltStr)
        if legend is not None:
            plt.legend((legend))
        plt.show()

    # cropping routine
    def crop(self, start=0, stop=None):
        """ cropping routine
        ------------------------
            start, stop: float
                start time and stop time in seconds
        """
        if stop is None:
            stop = self.get_duration()

        if (start * self.fs > self.length):
            raise ValueError("Start time (%1.2fs) is greater than the signal duration (%1.2fs)." % (
                start, self.get_duration()))
        if (stop < 0):
            raise ValueError("Stop time (%1.2fs) is less than 0" % (stop))
        if (start < 0):
            print "WARNING : Start time (%1.2fs) should be greater than 0" % start
            start = 0
        if (stop * self.fs > self.length):
            print "WARNING : Stop time (%1.2fs) should not be greater than the signal duration (%1.2fs)." %(stop, self.get_duration())
            stop = self.get_duration()

        self.data = self.data[start * self.fs: stop * self.fs, :]
        self.length = self.data.shape[0]

    def write(self, fileOutputPath):
        """ Write the current signal at the specified location in wav format

            This is done using the movepy library that requires ffmpeg"""

        faw = ffmpeg_audiowriter.FFMPEG_AudioWriter(
            fileOutputPath, self.fs, codec="pcm_s16le", nchannels=self.n_chan)
        faw.write_frames((self.data * (2 ** 15)).astype(np.int16))
        faw.close()

    def copy(self):
        copy = Signal(self.data.copy(), self.fs)
        copy.location = self.location
        copy.n_chan = self.n_chan
        copy.sample_width = self.sample_width
        copy.is_normalized = self.is_normalized
        return copy

    def play(self, start=0, end=None, verbose=True):
        """Routine to play the signal using pyaudio
        ---------------
        start, end: float
            start time and end time in second
        """

        BUFFER_SIZE = 1024
        n_bytes_per_sample = 2
        try:
            import pyaudio
        except ImportError:
            print "WARNING: PyAudio (https://people.csail.mit.edu/hubert/pyaudio/) is needed for playback."
            return
        p = pyaudio.PyAudio()

        if sys.platform=='darwin' and self.fs == 22050:
            sig_to_play = self.copy()
            sig_to_play.resample(44100)
        else:
            sig_to_play = self

        stream = p.open(format=pyaudio.paInt16,
                        channels=self.n_chan,
                        rate=sig_to_play.fs,
                        output=True)

        data = (sig_to_play[start:end].data
                * (2.**14.)).astype(np.int16).tostring()

        if verbose:
            print "Start playing. (CTL+C should work for interrupting)."

        for t in xrange(0, len(data), BUFFER_SIZE):
            stream.write(data[t:t + BUFFER_SIZE])
            if verbose:
                monitor_string = "Playing: %1.2fs (absolute), %1.2fs (relative)" % (start+(t/float(sig_to_play.fs*sig_to_play.n_chan*n_bytes_per_sample)),(t/float(sig_to_play.fs*sig_to_play.n_chan*n_bytes_per_sample)))
                sys.stdout.write("\r%s" % monitor_string)
                sys.stdout.flush()

        if verbose:
            sys.stdout.write("\r")
            sys.stdout.flush()
            print ""

        stream.stop_stream()
        stream.close()
        p.terminate()

    def save_max_format(self,file_name):
        """ Saves signal in a file file for Max ~pfft object """
        with open(file_name, 'w') as f:
            for t in range(len(self.data)):
                f.write('%i,%f\n' % (t,self.data[t]))

    def save_image(self,file_name,title=''):
        """ Saves an image of the signal """
        import matplotlib.pyplot as plt
        t_plot  = np.linspace(0.0, self.length/self.fs, self.length)
        fig, ax = plt.subplots(1,figsize=(8, 8))

        ax.plot(t_plot,self.data,'g')
        ax.set_title(title)
        ax.set_xlabel('seconds')

        fig.savefig(file_name)