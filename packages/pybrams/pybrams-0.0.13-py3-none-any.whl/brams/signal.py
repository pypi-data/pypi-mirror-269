import numpy as np

import matplotlib.pyplot as plt


from typing import Optional, Dict, Any

from .wav import Wav
from .pps import PPS
from .airplane_removal import AirplaneRemoval
from .beacon_removal import BeaconRemoval

from .locations import Location

from scipy.signal import stft, istft, check_NOLA

from scipy.special import erfcinv

SHORT_TO_FLOAT_FACTOR = 1 << 15

BEACON_MIN_FREQUENCY = 900 #1400 #900
BEACON_MAX_FREQUENCY = 1400 #1600 #1400

DURATION_PLOT = 3
OVERLAPS_PLOT = 0.9

class Signal:

    def __init__(self, wav: Wav, type: str, location:Location, properties: Dict[str, Any] = {}):
        
        self.samplerate = properties.get("samplerate", wav.header.samplerate)
        self.wav = wav
        self.data = wav.data.signal if wav.data.signal.dtype == np.float64 else (wav.data.signal / SHORT_TO_FLOAT_FACTOR).astype(np.float64)
        self.pps = PPS(wav.pps.index, wav.pps.time)
        self.type = type
        self.location = location
        self.beacon_frequency = properties.get("beacon_frequency")


    def compute_fft(self):

        self.nfft = len(self.data)
        self.fft = np.fft.fft(self.data, self.nfft) / self.nfft
        self.real_fft_freq = np.fft.rfftfreq(self.nfft, d = 1 / self.samplerate)
        self.real_fft = np.fft.rfft(self.data, self.nfft) / self.nfft


    def process(self):

        self.pps.correct(self.type)
        self.wav.pps.pps = [val for pair in zip(self.pps.index, self.pps.time) for val in pair]
        self.compute_beacon_frequency()
        self.wav.data.set(self.data)
        

    def __json__(self) -> Dict[str, Any]:

        return {
            "samplerate": self.samplerate,
            "beacon_frequency": self.beacon_frequency
        }


    def __eq__(self, other):
        
        if isinstance(other, Signal):

            return (
                (self.data == other.data).all() and
                self.samplerate == other.samplerate
            )

        return False
    
    
    def compute_beacon_frequency(self):

        self.compute_fft()

        indices_beacon_range = np.argwhere((self.real_fft_freq >= BEACON_MIN_FREQUENCY) & 
                                             (self.real_fft_freq <= BEACON_MAX_FREQUENCY))
        reduced_real_fft = self.real_fft[indices_beacon_range]
        reduced_real_fft_freq = self.real_fft_freq[indices_beacon_range]
        beacon_index = np.argmax(abs(reduced_real_fft))
        
        self.beacon_frequency = reduced_real_fft_freq[beacon_index][0]    

        
    def clean(self):

        """ Remove airplanes and direct beacon from signal """
    
        
        self.plot_spectrogram(title = f"Initial spectrogram")

        beacon_removal = BeaconRemoval(self)
        self.data = beacon_removal.remove_interference()
        
        self.plot_spectrogram(title = f"Spectrogram without beacon")

        
        """ airplane_removal = AirplaneRemoval(self)
        self.data = airplane_removal.remove_interference()

        self.plot_spectrogram(title = f"Spectrogram without airplane and beacon")  """

        
  
    def plot_spectrogram(self, title = "Raw spectrogram", half_range_spect = 100, export=False, filename=None, subplot=False, frame=True):

        from scipy.signal import spectrogram
        import matplotlib.pyplot as plt

        self.nfft = len(self.data)

        fft_points_plot = np.floor(DURATION_PLOT*self.samplerate).astype(int)
        n_overlap_plot = np.floor(OVERLAPS_PLOT*fft_points_plot).astype(int)

        # Compute spectrogram
        freq_vector, time_vector, spect = spectrogram(self.data, fs=self.samplerate, window='hann', nperseg=fft_points_plot, noverlap=n_overlap_plot, mode='magnitude')

        spect = np.abs(spect)

        spect_min_frequency = self.beacon_frequency - half_range_spect
        spect_max_frequency = self.beacon_frequency + half_range_spect

        spect_min_frequency_index = np.argmin(np.abs(freq_vector - spect_min_frequency))
        spect_max_frequency_index = np.argmin(np.abs(freq_vector - spect_max_frequency))  

        freq_vector = freq_vector[spect_min_frequency_index:spect_max_frequency_index+1]
        spect = spect[spect_min_frequency_index:spect_max_frequency_index+1, :]

        # Compute spectrogram stats
        spect_max = np.max(spect)
        spect_mu = np.mean(spect)

        # Display spectrogram in dB.
        if not subplot:
            plt.figure()
        plt.pcolormesh(time_vector, freq_vector, 10 * np.log10(spect / spect_max), cmap='jet')

        # Set colorbar limits and display it.
        cmin, cmax = plt.gci().get_clim()
        plt.clim(10 * np.log10(spect_mu / spect_max), cmax)
        
        if frame:
            plt.colorbar()
            # Set figure title and labels
            plt.title(title)
            plt.xlabel('Time [s]')
            plt.ylabel('Freq [Hz]')

        else:
            plt.axis("off")

        if export:
            save_path = filename if filename else "spectrogram.png"
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)

        else:
            plt.show()


        plt.close()

   