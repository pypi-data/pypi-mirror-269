# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:29:32 2023

@author: joachimb
"""

import json_fix
import numpy as np
import datetime
from dataclasses import dataclass

from brams import files

from scipy.signal import blackman, filtfilt, find_peaks, hilbert, savgol_filter, spectrogram, freqz
from scipy.special import erfcinv, fresnel
from scipy.interpolate import interp1d

import scipy.stats as stats

import matplotlib.pyplot as plt

from types import MappingProxyType

from KDEpy import FFTKDE

from utils.global_constants import WAVELENGTH

IDENTIFICATION_HALF_RANGE_FREQUENCY = 100
FILTERING_HALF_RANGE_FREQUENCY = 300
FILTERING_LENGTH_KERNEL = 1001
PREPADDING_DURATION = 3
POSTPADDING_DURATION = 5
SG_ORDER = 3

NOISE_DURATION = 1

# Time delays
AMPL_SG_WINDOW_DURATION = 50*1E-3 #s
MIN_PEAK_PROMINENCE_AMPL = 0.10
MIN_PEAK_HEIGHT_AMPL = 0.30

MINIMUM_SNR = 2 # 3 dB
MAXIMUM_RISE_DURATION = 2
MINIMUM_RISE_DURATION = 0.01

TIMING_CORRECTIONS = MappingProxyType({"AR": 24.5 * 1E-3, "ICOM": 1.9 * 1E-3, "RSP2": 33.3 * 1E-3})

# Pre-t0
MINIMUM_CROPPED_PHASE_VALUE = -14.098024352514232 # Corresponds to 4 Fresnel zones - 10.939944483167269 # Corresponds to 3 Fresnel zones before t0 -14.098024352514232 # Corresponds to 4 Fresnel zones  10.939944483167269 # Corresponds to 3 Fresnel zones before t0

PHASE_SG_WINDOW = 1
PROMINENCE_PHASE = -MINIMUM_CROPPED_PHASE_VALUE*0.1 # rad
MAXIMUM_PHASE_VALUE = -0.5135047640574028 # rad

FRESNEL_PARAMETER_AT_MAXIMUM_PHASE = 0.571758 
MINIMUM_FRESNEL_PARAMETER = -10
NUMBER_FRESNEL_PARAMETERS = 10000

MAXIMUM_DURATION_KNEE_TO_MAXIMUM_PHASE = 0.2

NUMBER_OFFSETS_AROUND_T0 = 150
NUMBER_OFFSETS_AFTER_MINIMUM_PHASE = 60

DISTANCE_PEAKS_CORRELATION = 1
NUMBER_PEAKS_CORRELATION = 50

MINIMUM_LENGTH_SLIDING_SLOPE = 50
NUMBER_WINDOWS_SLIDING_SLOPE = 12
MINIMUM_corr_coeff = 0.9
MINIMUM_SIZE_HISTOGRAM = 50
POINTS_AROUND_HISTOGRAM_PEAK = 30


@dataclass
class Meteor:

    frequency: float = None
    ampl_timing: float = None
    timing: float = None
    noise: float = None
    fresnel_speed: float = None
    fresnel_std: float = None
    corr_coeff: float = None
    SNR: float = None
          
    def __json__(self):
        
        return self.__dict__

    def extract_infos(self, start:str, end:str, file:files.File, plot:bool):
        print("")
        print(f"Extracting meteor infos for {file.system_code} ...")
                        

        start_dt = datetime.datetime.fromisoformat(f"{start}+00:00")
        end_dt = datetime.datetime.fromisoformat(f"{end}+00:00")

        shifted_pps = file.signal.pps.timestamps.get_s() - file.signal.pps.timestamps.get_s()[0]
        index_pps = file.signal.pps.index
        
        user_start = start_dt.timestamp()
        user_end = end_dt.timestamp()

        sample_user_start = round((user_start - file.wav.header.start_us / 1e6) * file.signal.samplerate)
    
        if sample_user_start < 0:
            return
        
        sample_user_end = round((user_end - file.wav.header.start_us / 1e6) * file.signal.samplerate)
        
        user_signal = file.signal.data[sample_user_start : sample_user_end + 1]
        
        filtered_user_signal, _ = self.filter_signal(user_signal, file)

        hilbert_user_signal = hilbert(filtered_user_signal)
        i_user_signal, q_user_signal = np.real(hilbert_user_signal), np.imag(hilbert_user_signal)

        user_ampl = np.sqrt(i_user_signal**2 + q_user_signal**2)

        ampl_sg_window_points = round(AMPL_SG_WINDOW_DURATION * file.signal.samplerate)
        user_ampl = self.apply_sg_filter(user_ampl, ampl_sg_window_points, SG_ORDER)
        
        index_meteor_peak = np.argmax(user_ampl)
        
        sample_meteor_start = sample_user_start + index_meteor_peak - round(PREPADDING_DURATION * file.signal.samplerate)
        sample_meteor_end = sample_user_start + index_meteor_peak + round(POSTPADDING_DURATION * file.signal.samplerate)
        
        meteor_signal = file.signal.data[sample_meteor_start : sample_meteor_end + 1]
        
        filtered_meteor_signal, meteor_frequency = self.filter_signal(meteor_signal, file)
        
        times = np.empty(len(meteor_signal))
        samples_meteor = np.arange(sample_meteor_start, sample_meteor_end + 1)

        for i in range(len(meteor_signal)):
            times[i] = self.extrapolate_time(samples_meteor[i], shifted_pps, index_pps, file.signal.samplerate)
    
        shifted_times = times - times[0]
        
        hilbert_meteor_signal = hilbert(filtered_meteor_signal)
        i_meteor_signal, q_meteor_signal = np.real(hilbert_meteor_signal), np.imag(hilbert_meteor_signal)

        meteor_ampl = np.sqrt(i_meteor_signal**2 + q_meteor_signal**2)
       
        if plot:
            plt.figure()
            plt.title(f"{file.system_code} ({file.type})")
            plt.plot(times, meteor_ampl)
            plt.xlabel("Time [s]")
            plt.ylabel("Ampl [-]")
            plt.tight_layout()
            plt.grid(True)
            plt.show()

        meteor_ampl = self.apply_sg_filter(meteor_ampl, ampl_sg_window_points, SG_ORDER)
        meteor_derivative_ampl = self.apply_sg_filter(meteor_ampl, ampl_sg_window_points, SG_ORDER, 1)        
        normalized_meteor_ampl = meteor_ampl/max(meteor_ampl)
        
        noise = np.arange(round(NOISE_DURATION * file.signal.samplerate))
        median_noise = np.median(normalized_meteor_ampl[noise])

        power_noise = np.sum(normalized_meteor_ampl[noise]**2)/len(normalized_meteor_ampl[noise])

        index_global_max_ampl = np.argmax(normalized_meteor_ampl)
        index_ref_max_ampl = index_global_max_ampl

        """ local_indices_max_ampl, _ = find_peaks(normalized_meteor_ampl[noise[-1]:index_global_max_ampl], height = median_noise + MIN_PEAK_HEIGHT_AMPL*(normalized_meteor_ampl[index_global_max_ampl] - median_noise), prominence = MIN_PEAK_PROMINENCE_AMPL + median_noise)

        if any(local_indices_max_ampl):
            index_ref_max_ampl = min(noise[-1] + local_indices_max_ampl) """

        start_rise = -1
        condition_minimum = normalized_meteor_ampl[noise[-1]:index_ref_max_ampl+1] < median_noise
        local_indices_minimum_ampl = np.where(condition_minimum)[0]

        if any(local_indices_minimum_ampl):
            start_rise = noise[-1] + local_indices_minimum_ampl[-1]
        
        if start_rise == -1:
            print("Min ampl not found")
            return
              
        indices = np.arange(len(normalized_meteor_ampl))
        
        rise = np.where((indices <= index_global_max_ampl) & (indices >= start_rise))[0]  
        
        if (len(rise) == 0):
            print("No rise found")
            return
        
            
        start_exponential = index_global_max_ampl
        local_end_exponential = np.argmax(normalized_meteor_ampl[start_exponential:] < median_noise)
        end_exponential = start_exponential + local_end_exponential
        exponential = np.arange(start_exponential, end_exponential)
        
        if (len(exponential) == 0):
            print("No exponential found")
            return
                
        echo = np.concatenate((rise, exponential))
        not_echo = np.setdiff1d(indices, echo)
                    
        index_meteor_in_rise = np.argmax(normalized_meteor_ampl[rise] >= (median_noise + 0.42711*(normalized_meteor_ampl[index_ref_max_ampl] - median_noise)))
        index_meteor = index_meteor_in_rise + rise[0]
        meteor_sample = index_meteor + sample_meteor_start

        index_inflection = np.argmax(meteor_derivative_ampl)

        power_echo = np.sum(normalized_meteor_ampl[echo]**2)/len(normalized_meteor_ampl[echo])
        self.SNR = power_echo/power_noise

        print("SNR = ", 10*np.log10(self.SNR), " dB")
        print("Rise duration = ", 1000*len(rise)/file.signal.samplerate, " ms")  
        
        if plot:
            # Plot split signal
            plt.figure()
            plt.plot(times[rise], normalized_meteor_ampl[rise], '.g', label = 'Rise')
            plt.plot(times[exponential], normalized_meteor_ampl[exponential], '.b', label = "Exponential")
            plt.plot(times[not_echo], normalized_meteor_ampl[not_echo], '.r', label = "Not echo")
            plt.plot(times[index_meteor], normalized_meteor_ampl[index_meteor], '*', markersize = 14, label = r'$t_{0}$')
            plt.plot(times[index_ref_max_ampl], normalized_meteor_ampl[index_ref_max_ampl], 'd', markersize = 14, label = 'Ref max')
            plt.grid(True)
            plt.xlabel('Time [s]')
            plt.ylabel('Ampl [-]')
            plt.legend(loc='best')
            plt.title(f"Smooth ampl curve")          
            plt.tight_layout()
            plt.show()

        if plot:
            # Plot split signal
            plt.figure()
            plt.plot(times, normalized_meteor_ampl, label = 'Signal')
            plt.plot(times[index_meteor], normalized_meteor_ampl[index_meteor], '*', markersize = 14, label = r'$t_{0}$')
            plt.grid(True)
            plt.xlabel('Time [s]')
            plt.ylabel('Ampl [-]')
            plt.legend(loc='best')
            plt.title(f"Ampl curve after beacon and airplane subtraction")          
            plt.tight_layout()
            plt.show()

        if self.SNR < MINIMUM_SNR or index_inflection not in rise or len(rise) < (MINIMUM_RISE_DURATION*file.signal.samplerate) or len(rise) > (MAXIMUM_RISE_DURATION*file.signal.samplerate) or index_meteor_in_rise == 0:
            print("No meteor detected")
            return
        
        #self.compute_doppler_shift(file, times, rise[0], rise[-1], filtered_meteor_signal, meteor_frequency, plot)
        
        print("meteor sample = ", meteor_sample)


        self.frequency = meteor_frequency
        self.ampl_timing = self.extrapolate_time(meteor_sample, file.signal.pps.timestamps.get_s(), file.signal.pps.index, file.signal.samplerate) - TIMING_CORRECTIONS[file.type]
        self.timing = self.ampl_timing   
        
        print("Meteor timing successfully determined !")
        
        self.compute_pre_t0_speed(file, normalized_meteor_ampl, i_meteor_signal, q_meteor_signal, times, shifted_times, index_meteor, sample_meteor_start, index_global_max_ampl, plot)
    
    
    def compute_doppler_shift(self, file, times, start_rise, end_rise, meteor_signal, meteor_frequency, plot):
        
        time_crossings = self.find_zero_crossings(times, meteor_signal)
                
        number_crossings = len(time_crossings)
        NUMBER_PERIODS_AVERAGE = 20
        number_crossings_average = 2*NUMBER_PERIODS_AVERAGE + 1
        number_doppler_average = number_crossings - number_crossings_average + 1
        
        time_crossings_average = np.zeros(number_doppler_average)
        doppler_shift_average = np.zeros(number_doppler_average)
   
        for i in range(number_doppler_average):
            time_crossings_average[i] = np.mean(time_crossings[i : i+number_crossings_average])
            doppler_shift_average[i] = (number_crossings_average-1) / (2 * (time_crossings[i+number_crossings_average-1]-time_crossings[i] ))
            #○print("end index = ", i+number_crossings_average)
                
        doppler_shift = 1/(2*np.gradient(time_crossings))
        
        if plot:
            plt.figure()
            plt.plot(time_crossings, doppler_shift)
            plt.plot(time_crossings_average, doppler_shift_average)
            plt.title(f"{file.system_code}")          
            plt.show()
        
        TIME_SPAN_DOPPLER = 0.2
        MINIMUM_DOPPLER_SHIFT = 30
        
        time_start_rise = times[start_rise]
        time_end_rise = times[end_rise]
        
        index_start_rise_average = np.argmin(abs(time_crossings_average - time_start_rise))
        index_end_rise_average = np.argmin(abs(time_crossings_average - time_end_rise))
        
           
        index_start_doppler = index_start_rise_average + np.argmax(doppler_shift_average[index_start_rise_average : index_end_rise_average+1])
        #index_start_doppler = index_start_rise_average
        time_start_doppler = time_crossings_average[index_start_doppler]
        index_end_doppler = np.argmin(abs(time_crossings_average - (time_start_doppler + TIME_SPAN_DOPPLER)))

        time_crossings_average_crop = time_crossings_average[index_start_doppler : index_end_doppler+1]
        doppler_shift_average_crop = doppler_shift_average[index_start_doppler : index_end_doppler+1]
        
        if plot:
            plt.figure()
            plt.plot(time_crossings_average_crop, doppler_shift_average_crop)
            plt.title(f"{file.system_code}")          
            plt.show()
            
        index_end_fit = np.where(doppler_shift_average_crop < meteor_frequency + MINIMUM_DOPPLER_SHIFT)[0][0]
        index_start_fit = 1
        
        time_crossings_average_fit = time_crossings_average_crop[index_start_fit:index_end_fit]
        doppler_shift_average_fit = doppler_shift_average_crop[index_start_fit:index_end_fit]
        
        if plot:
            plt.figure()
            plt.title(f"{file.system_code} ({file.type})")
            plt.plot(time_crossings_average_fit, doppler_shift_average_fit)
            plt.show()
            

    def find_zero_crossings(self, times, signal):
        idx = np.where(signal[1:] * signal[:-1] < 0)[0]
        time_crossings = np.zeros(len(idx))
        
        for i, j in enumerate(idx):
            time_crossings[i] = np.interp(0.0, signal[j:j+2], times[j:j+2])      
            
        return time_crossings
    

    def compute_pre_t0_speed(self, file, normalized_meteor_ampl, i_meteor_signal, q_meteor_signal, times, shifted_times, index_meteor, sample_meteor_start, index_global_max_ampl, plot):
        
        meteor_phase = np.arctan2(q_meteor_signal, i_meteor_signal)

        meteor_phase_unwrapped = np.unwrap(meteor_phase)
        corrected_meteor_phase = meteor_phase_unwrapped - (2 * np.pi * self.frequency * shifted_times)
        
        meteor_phase = self.apply_sg_filter(corrected_meteor_phase, PHASE_SG_WINDOW, SG_ORDER)
    
        indices_minimum_phase, _ = find_peaks(-meteor_phase, prominence = PROMINENCE_PHASE)
        index_minimum_phase = self.find_closest_smaller(indices_minimum_phase, index_meteor)
        
        index_maximum_phase = index_meteor + np.argmax(corrected_meteor_phase[index_meteor:index_global_max_ampl+1])
        
        shifted_meteor_phase = meteor_phase - (meteor_phase[index_maximum_phase] - MAXIMUM_PHASE_VALUE)
        
        index_t0 = index_maximum_phase
        while shifted_meteor_phase[index_t0] > -np.pi/4:
            index_t0 = index_t0 - 1
            if index_t0 <= 0:
                return
        
        if abs(shifted_meteor_phase[index_t0] + np.pi/4) > abs(shifted_meteor_phase[index_t0] + np.pi/4):
            index_t0 = index_t0 + 1
            
        if (index_t0 <= index_minimum_phase):
            return
        
        cropped_meteor_phase = shifted_meteor_phase[index_minimum_phase : index_maximum_phase + 1]
        
        
        if plot:
            plt.figure()
            plt.title(f"{file.system_code} ({file.type})")
            plt.plot(times[index_minimum_phase : index_maximum_phase+1], cropped_meteor_phase)
            plt.show() 
    
        fresnel_parameters_to_maximum_phase = np.linspace(MINIMUM_FRESNEL_PARAMETER, FRESNEL_PARAMETER_AT_MAXIMUM_PHASE, NUMBER_FRESNEL_PARAMETERS)
        
        fresnel_reference_point = -0.5 - 0.5j
        
        fresnel_sine, fresnel_cosine = fresnel(fresnel_parameters_to_maximum_phase)
        fresnel_integral = fresnel_cosine + 1j * fresnel_sine
        fresnel_phase = np.unwrap(np.angle(fresnel_integral - fresnel_reference_point))    
        fresnel_phase = -fresnel_phase
        
        index_maximum_fresnel_phase = np.argmax(fresnel_phase)
        fresnel_phase = fresnel_phase - (fresnel_phase[index_maximum_fresnel_phase] - MAXIMUM_PHASE_VALUE)
        
        cropped_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(cropped_meteor_phase)
        
        index_knee = self.find_knee(cropped_fresnel_parameters) + index_minimum_phase
        
        if plot:
            fig, ax = plt.subplots()
            twin = ax.twinx()
            plt.title(f"{file.system_code} ({file.type})")
            p1, = ax.plot(times[index_knee-500:index_knee+500], corrected_meteor_phase[index_knee-500:index_knee+500], label = "Phase", color = 'red')
            p2, = twin.plot(times[index_knee-500:index_knee+500], normalized_meteor_ampl[index_knee-500:index_knee+500], label = "Amplitude", color = 'blue')
            plt.legend(handles=[p1, p2])
            plt.show()
        
        minimum_meteor_cropped_phase, index_minimum_meteor_cropped_phase = np.min(cropped_meteor_phase), np.argmin(cropped_meteor_phase)
        
        if minimum_meteor_cropped_phase > MINIMUM_CROPPED_PHASE_VALUE or index_minimum_meteor_cropped_phase > 0 or abs(index_knee - index_maximum_phase) > MAXIMUM_DURATION_KNEE_TO_MAXIMUM_PHASE*file.signal.samplerate:
            print("No pre-t0 speed detected")
            return
        
        fresnel_stds = np.array([])
        fresnel_speeds = np.array([])
        corr_coeffs = np.array([])
        indices_t0 = np.array([], dtype = np.int64)
        indices_start_phase = np.array([], dtype = np.int64)
        offsets_minimum_phase = np.arange(NUMBER_OFFSETS_AFTER_MINIMUM_PHASE)
        
        for offset_minimum_phase in offsets_minimum_phase:
            fresnel_std, fresnel_speed, corr_coeff, index_t0 = self.get_pre_t0_speed_correlation(index_knee, index_minimum_phase + offset_minimum_phase, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase)
            fresnel_stds = np.append(fresnel_stds, fresnel_std)
            fresnel_speeds = np.append(fresnel_speeds, fresnel_speed)
            corr_coeffs = np.append(corr_coeffs, corr_coeff)
            indices_start_phase = np.concatenate((indices_start_phase, (index_minimum_phase + offset_minimum_phase)*np.ones(len(index_t0), dtype = np.int64)))
            indices_t0 = np.append(indices_t0, index_t0)
            
    
        if not corr_coeffs.size or max(corr_coeffs) < MINIMUM_corr_coeff:
            print("Too small pre-t0 correlation")
            return
        
        good_fresnel_speeds = fresnel_speeds[np.where(corr_coeffs > MINIMUM_corr_coeff)]
        good_corr_coeffs = corr_coeffs[np.where(corr_coeffs > MINIMUM_corr_coeff)]
        good_indices_start_phase = indices_start_phase[np.where(corr_coeffs > MINIMUM_corr_coeff)]
        good_indices_t0 = indices_t0[np.where(corr_coeffs > MINIMUM_corr_coeff)]
        
        indices_sorted_speeds = np.argsort(good_fresnel_speeds)
        good_sorted_fresnel_speeds = good_fresnel_speeds[indices_sorted_speeds]
        good_sorted_corr_coeffs = good_corr_coeffs[indices_sorted_speeds]
        good_sorted_indices_start_phase = good_indices_start_phase[indices_sorted_speeds]
        good_sorted_indices_t0 = good_indices_t0[indices_sorted_speeds]
     
        peaks, _ = find_peaks(good_sorted_corr_coeffs, distance = DISTANCE_PEAKS_CORRELATION)

        if not peaks.size:
            print("No pre-t0 speed peak found ")
            return

        n_highest_peaks = np.argsort(-good_sorted_corr_coeffs[peaks])[:NUMBER_PEAKS_CORRELATION]
        indices_n_highest_peaks = peaks[n_highest_peaks]
        
        peaks_sorted_fresnel_speeds = good_sorted_fresnel_speeds[indices_n_highest_peaks]
        peaks_sorted_corr_coeffs = good_sorted_corr_coeffs[indices_n_highest_peaks]
        peaks_sorted_indices_start_phase = good_sorted_indices_start_phase[indices_n_highest_peaks]
        peaks_sorted_indices_t0 = good_sorted_indices_t0[indices_n_highest_peaks]

        print("higest R² speed =", peaks_sorted_fresnel_speeds[0])
        print("peaks sorted coeff = ", peaks_sorted_corr_coeffs[0:10])
        
        """ if plot:
            plt.figure()
            plt.plot(good_sorted_fresnel_speeds, good_sorted_corr_coeffs, 'o')
            plt.plot(peaks_sorted_fresnel_speeds, peaks_sorted_corr_coeffs, 'xr')
            plt.show() """
                
        best_fresnel_std, best_fresnel_speed, best_median_corr_coeff, best_index_t0, best_peak_index = self.check_pre_t0_speed_histograms_pssst(peaks_sorted_indices_start_phase, peaks_sorted_indices_t0, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase) 
        
        print("lowest STD speed = ", best_fresnel_speed)

        meteor_sample = best_index_t0 + sample_meteor_start
        
        self.timing = self.extrapolate_time(meteor_sample, file.signal.pps.timestamps.get_s(), file.signal.pps.index, file.signal.samplerate) - TIMING_CORRECTIONS[file.type]
        self.fresnel_speed = peaks_sorted_fresnel_speeds[best_peak_index]
        self.fresnel_std = best_fresnel_std
        self.corr_coeff = peaks_sorted_corr_coeffs[best_peak_index]

        print("Pre-t0 speed successfully determined !")
        print("fresnel speed = ", self.fresnel_speed)
        
      
    def get_pre_t0_speed_correlation(self, index_meteor, index_minimum_phase, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase):    
        best_fresnel_speeds = np.array([])
        std_fresnel_speeds = np.array([])
        median_corr_coeffs = np.array([])
        best_indices_t0 = np.array([], dtype = np.int32)
        
        index_t0_guesses = np.arange(index_meteor - NUMBER_OFFSETS_AROUND_T0, index_meteor + NUMBER_OFFSETS_AROUND_T0 + 1)
        
        for index_t0_guess in index_t0_guesses:
            
            if index_t0_guess - index_minimum_phase < MINIMUM_LENGTH_SLIDING_SLOPE:
                continue
            
            sliding_slope_meteor_phase = shifted_meteor_phase[index_minimum_phase:index_t0_guess+1]
            sliding_slope_meteor_phase = sliding_slope_meteor_phase - sliding_slope_meteor_phase[-1] - np.pi/4
            
            if min(sliding_slope_meteor_phase) > MINIMUM_CROPPED_PHASE_VALUE:
                continue
                        
            sliding_slope_times = times[index_minimum_phase:index_t0_guess+1]
            
            try:
                sliding_slope_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(sliding_slope_meteor_phase)
            except:
                print('Lack of points making the interpolation impossible. Probably due to a decreasing phase curve.')
                continue
            
            sliding_slope_fresnel_distance = sliding_slope_fresnel_parameters*np.sqrt(WAVELENGTH/2) 
                        
            speed, intercept, corr_coeff, _, _ = stats.linregress(sliding_slope_times, sliding_slope_fresnel_distance)

            best_fresnel_speeds = np.append(best_fresnel_speeds, speed)
            std_fresnel_speeds = np.append(std_fresnel_speeds, 1/corr_coeff)
            median_corr_coeffs = np.append(median_corr_coeffs, corr_coeff)
            
            best_indices_t0 = np.append(best_indices_t0, index_t0_guess)
    
        return std_fresnel_speeds, best_fresnel_speeds, median_corr_coeffs, best_indices_t0
                
      
        
    def check_pre_t0_speed_histograms_pssst(self, indices_start_phase, indices_t0, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase):
        best_fresnel_speeds = np.array([])
        std_fresnel_speeds = np.array([])
        median_corr_coeffs = np.array([])
        
        peak_indices = np.arange(0, len(indices_start_phase))
                
        for i in range(len(indices_start_phase)):
            
            index_start_phase = indices_start_phase[i]
            index_t0 = indices_t0[i]
                
            sliding_slope_meteor_phase = shifted_meteor_phase[index_start_phase:index_t0+1]
            sliding_slope_meteor_phase = sliding_slope_meteor_phase - sliding_slope_meteor_phase[-1] - np.pi/4
                        
            sliding_slope_times = times[index_start_phase:index_t0+1]
            
            try:
                sliding_slope_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(sliding_slope_meteor_phase)
            except:
                print('Lack of points making the interpolation impossible. Probably due to a decreasing phase curve.')
                continue
            
            sliding_slope_fresnel_distance = sliding_slope_fresnel_parameters*np.sqrt(WAVELENGTH/2) 
                        
            maximum_window_length = len(sliding_slope_meteor_phase)
            minimum_window_length = maximum_window_length - NUMBER_WINDOWS_SLIDING_SLOPE + 1 
            
            window_lengths = np.arange(minimum_window_length, maximum_window_length+1)
            
            fresnel_speed_histogram = np.array([])
            fresnel_intercept_histogram = np.array([])
            corr_coeffs = np.array([])
            
            for window_length in window_lengths:
                
                for window_start in range(maximum_window_length-window_length+1):
                    
                    window_fresnel_distance = sliding_slope_fresnel_distance[window_start:window_start+window_length]
                    window_times = sliding_slope_times[window_start:window_start+window_length]
                    
                    window_speed, window_intercept, window_corr_coeff, _, _ = stats.linregress(window_times, window_fresnel_distance)
                    
                    if (window_corr_coeff > MINIMUM_corr_coeff):
                        fresnel_speed_histogram  = np.append(fresnel_speed_histogram, window_speed)
                        fresnel_intercept_histogram = np.append(fresnel_intercept_histogram, window_intercept)
                        corr_coeffs = np.append(corr_coeffs, window_corr_coeff)

            if len(fresnel_speed_histogram) >= MINIMUM_SIZE_HISTOGRAM:

                kde_speeds, kde_speed_density = FFTKDE(kernel = 'gaussian', bw = 'silverman').fit(fresnel_speed_histogram).evaluate()
                
                peak_speeds_indices, _ = find_peaks(kde_speed_density, height = (None, None))
                peak_speeds = kde_speeds[peak_speeds_indices]
                
                peak_intercepts = np.array([])
                
                for peak_speed in peak_speeds:
                    closest_intercept_indices = self.find_closest_indices(fresnel_intercept_histogram, peak_speed, POINTS_AROUND_HISTOGRAM_PEAK)
                    cropped_fresnel_intercept_histogram = fresnel_intercept_histogram[closest_intercept_indices]
                    
                    kde_intercepts, kde_intercept_density = FFTKDE(kernel = 'gaussian', bw = 'silverman').fit(cropped_fresnel_intercept_histogram).evaluate()
                    peak_intercepts_indices, peak_intercepts_dict = find_peaks(kde_intercept_density, height = (None, None))
                    peak_intercepts_heights = peak_intercepts_dict['peak_heights']       
                    highest_peak_intercepts_index = peak_intercepts_indices[np.argmax(peak_intercepts_heights)]
                    peak_intercepts = np.append(peak_intercepts, kde_intercepts[highest_peak_intercepts_index])
                    
                residual_intercepts = abs(peak_intercepts + peak_speeds*times[index_t0])
                best_intercept_index = np.argmin(residual_intercepts)
                
                best_fresnel_speeds = np.append(best_fresnel_speeds, peak_speeds[best_intercept_index])
                std_fresnel_speeds = np.append(std_fresnel_speeds, np.std(fresnel_speed_histogram))
                median_corr_coeffs = np.append(median_corr_coeffs, np.median(corr_coeffs))
                
                
        final_std_fresnel_speed, index_minimum_std_fresnel_speeds = np.min(std_fresnel_speeds), np.argmin(std_fresnel_speeds)
        final_fresnel_speed = best_fresnel_speeds[index_minimum_std_fresnel_speeds]
        final_median_corr_coeff = median_corr_coeffs[index_minimum_std_fresnel_speeds]
        
        final_index_t0 = indices_t0[index_minimum_std_fresnel_speeds]
        final_peak_index = peak_indices[index_minimum_std_fresnel_speeds]
    
        return final_std_fresnel_speed, final_fresnel_speed, final_median_corr_coeff, final_index_t0, final_peak_index   
    
    
    def filter_signal(self, signal, file:files.File):
        # Filter signal
        
        real_fft_signal = np.fft.rfft(signal, len(signal)) / len(signal)
        real_fft_signal_freq = np.fft.rfftfreq(len(signal), d = 1 / file.signal.samplerate)
        
        indices_signal_range = np.argwhere( (real_fft_signal_freq >= file.signal.beacon_frequency - IDENTIFICATION_HALF_RANGE_FREQUENCY) &
                                            (real_fft_signal_freq <= file.signal.beacon_frequency + IDENTIFICATION_HALF_RANGE_FREQUENCY)
                                          )
        
        real_fft_signal = real_fft_signal[indices_signal_range]
        real_fft_signal_freq = real_fft_signal_freq[indices_signal_range]
        signal_index = np.argmax(abs(real_fft_signal))
        
        signal_frequency = real_fft_signal_freq[signal_index][0]
        
        signal_fc_low = (signal_frequency + FILTERING_HALF_RANGE_FREQUENCY) / file.signal.samplerate
        signal_fc_high = (signal_frequency - FILTERING_HALF_RANGE_FREQUENCY) / file.signal.samplerate
        
        filtered_signal = apply_blackman_filter(signal, signal_fc_low, signal_fc_high, FILTERING_LENGTH_KERNEL)

        #filtered_signal = bandpass_butter_filter(signal, signal_frequency - FILTERING_HALF_RANGE_FREQUENCY, signal_frequency + FILTERING_HALF_RANGE_FREQUENCY, file.signal.samplerate, order = 3)

        return filtered_signal, signal_frequency
    
    def apply_sg_filter(self, array, window, order, deriv = 0, mode = 'mirror'):

        if window > order:

            return savgol_filter(array, window, order, deriv = deriv, mode = mode)

        return array
 
    def extrapolate_time(self, sample, timestamps, sample_numbers, fs):
        # Find the time corresponding to the determined sample
        index = self.find_nearest(sample_numbers, sample)
        closest_timestamp = timestamps[index]
        time = closest_timestamp + (sample - sample_numbers[index]) / fs
        return time
    
    def find_closest_smaller(self, arr, value):
        limit = float('-inf')
        closest = -1
        for num in arr:
            if num < value and num > limit:
                closest = num
        return closest
    
    def find_closest_smaller_values(self, value, array, number_of_samples):     
        smaller_values = array[array < value]
        sorted_values = np.sort(smaller_values)
        return sorted_values[-number_of_samples:]

    def find_nearest(self, array, value):
        return (np.abs(array - value)).argmin() 
    
    def find_closest_indices(self, array, value, n):
        # Calculate the absolute differences between the array elements and the value
        absolute_diff = np.abs(array - value)
    
        # Sort the absolute differences and get the indices of the sorted elements
        sorted_indices = np.argsort(absolute_diff)
    
        # Return the first n indices
        return sorted_indices[:n]
    
    def find_knee(self, signal):
        residual = np.zeros(len(signal)-1)
        for i in range (len(signal)-1):
            signal1, signal2 = np.split(signal, [i+1])
            sse1, sse2 = self.sum_squared_diff(signal1), self.sum_squared_diff(signal2)
            residual[i] = sse1 + sse2
        index_knee = np.argmin(residual) + 1
        return index_knee
        
    def sum_squared_diff(self, signal):
        x = np.arange(len(signal))
        y = signal
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        y_pred = m*x + c
        deviation = np.sum((y - y_pred)**2)
        return deviation
    
    def wav_to_spect(self, signal, ffts, overlaps, fs, freq_beacon, title, half_range_spect):
        """
        Convert .wav file to a spectrogram

        Parameters:
        signal (ndarray): Audio signal data
        ffts (int): Number of points to use for the FFT
        overlaps (int): Number of points for overlap between adjacent segments
        fs (int): Sampling frequency of the signal
        freq_beacon (int): Beacon frequency
        title (str): Title for the figure
        half_range_spect (int): Half window duration around the beacon frequency

        Returns:
        spect (ndarray): Spectrogram data
        freq_vector (ndarray): Frequency vector
        time_vector (ndarray): Time vector
        """

        # Compute spectrogram
        freq_vector, time_vector, spect = spectrogram(signal, fs=fs, window='hann', nperseg=ffts, noverlap=overlaps, mode='magnitude')

        spect = np.abs(spect)
        df = fs / ffts

        filter = np.logical_and(freq_vector >= (freq_beacon - half_range_spect), freq_vector <= (freq_beacon + half_range_spect))
        freq_vector = freq_vector[filter]
        spect = spect[filter,:]

        # Compute spectrogram stats
        spect_max = np.max(spect)
        spect_mu = np.mean(spect)

        # Display spectrogram in dB.
        plt.pcolormesh(time_vector, freq_vector, 10 * np.log10(spect / spect_max), cmap='jet')
        plt.axis('tight')

        # Set colorbar limits and display it.
        cmin, cmax = plt.gci().get_clim()
        plt.clim(10 * np.log10(spect_mu / spect_max), cmax)
        plt.colorbar()

        # Set figure title and labels
        plt.title(title)
        plt.xlabel('Time [s]')
        plt.ylabel('Freq [Hz]')
        plt.grid()
        
        plt.show()  
        
    def get_pre_t0_speed_histograms_pssst(self, index_meteor, index_minimum_phase, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase):
        best_fresnel_speeds = np.array([])
        std_fresnel_speeds = np.array([])
        median_corr_coeffs = np.array([])
        best_indices_t0 = np.array([], dtype = np.int32)
        
        index_t0_guesses = np.arange(index_meteor - NUMBER_OFFSETS_AROUND_T0, index_meteor + NUMBER_OFFSETS_AROUND_T0 + 1)
        
        for index_t0_guess in index_t0_guesses:
            if index_t0_guess - index_minimum_phase < MINIMUM_LENGTH_SLIDING_SLOPE:
                continue
            
            sliding_slope_meteor_phase = shifted_meteor_phase[index_minimum_phase:index_t0_guess+1]
            sliding_slope_meteor_phase = sliding_slope_meteor_phase - sliding_slope_meteor_phase[-1] - np.pi/4
                        
            sliding_slope_times = times[index_minimum_phase:index_t0_guess+1]
            
            try:
                sliding_slope_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(sliding_slope_meteor_phase)
            except:
                print('Lack of points making the interpolation impossible. Probably due to a decreasing phase curve.')
                continue
            
            sliding_slope_fresnel_distance = sliding_slope_fresnel_parameters*np.sqrt(WAVELENGTH/2) 
                        
            maximum_window_length = len(sliding_slope_meteor_phase)
            minimum_window_length = maximum_window_length - NUMBER_WINDOWS_SLIDING_SLOPE + 1 
            
            window_lengths = np.arange(minimum_window_length, maximum_window_length+1)
            
            fresnel_speed_histogram = np.array([])
            fresnel_intercept_histogram = np.array([])
            corr_coeffs = np.array([])
            
            for window_length in window_lengths:
                
                for window_start in range(maximum_window_length-window_length+1):
                    
                    window_fresnel_distance = sliding_slope_fresnel_distance[window_start:window_start+window_length]
                    window_times = sliding_slope_times[window_start:window_start+window_length]
                    
                    window_speed, window_intercept, window_corr_coeff, _, _ = stats.linregress(window_times, window_fresnel_distance)
                    
                    if (window_corr_coeff > MINIMUM_corr_coeff):
                        fresnel_speed_histogram  = np.append(fresnel_speed_histogram, window_speed)
                        fresnel_intercept_histogram = np.append(fresnel_intercept_histogram, window_intercept)
                        corr_coeffs = np.append(corr_coeffs, window_corr_coeff)

            if len(fresnel_speed_histogram) >= MINIMUM_SIZE_HISTOGRAM:
                kde_speeds, kde_speed_density = FFTKDE(kernel = 'gaussian', bw = 'silverman').fit(fresnel_speed_histogram).evaluate()
                
                peak_speeds_indices, _ = find_peaks(kde_speed_density, height = (None, None))
                peak_speeds = kde_speeds[peak_speeds_indices]
                
                peak_intercepts = np.array([])
                
                for peak_speed in peak_speeds:
                    closest_intercept_indices = self.find_closest_indices(fresnel_intercept_histogram, peak_speed, POINTS_AROUND_HISTOGRAM_PEAK)
                    cropped_fresnel_intercept_histogram = fresnel_intercept_histogram[closest_intercept_indices]
                    
                    kde_intercepts, kde_intercept_density = FFTKDE(kernel = 'gaussian', bw = 'silverman').fit(cropped_fresnel_intercept_histogram).evaluate()
                    peak_intercepts_indices, peak_intercepts_dict = find_peaks(kde_intercept_density, height = (None, None))
                    peak_intercepts_heights = peak_intercepts_dict['peak_heights']       
                    highest_peak_intercepts_index = peak_intercepts_indices[np.argmax(peak_intercepts_heights)]
                    peak_intercepts = np.append(peak_intercepts, kde_intercepts[highest_peak_intercepts_index])
                    
                residual_intercepts = abs(peak_intercepts + peak_speeds*times[index_t0_guess])
                best_intercept_index = np.argmin(residual_intercepts)
                
                best_fresnel_speeds = np.append(best_fresnel_speeds, peak_speeds[best_intercept_index])
                std_fresnel_speeds = np.append(std_fresnel_speeds, np.std(fresnel_speed_histogram))
                median_corr_coeffs = np.append(median_corr_coeffs, np.median(corr_coeffs))
                
                best_indices_t0 = np.append(best_indices_t0, index_t0_guess)
        
        final_std_fresnel_speed, index_minimum_std_fresnel_speeds = np.min(std_fresnel_speeds), np.argmin(std_fresnel_speeds)
        final_fresnel_speed = best_fresnel_speeds[index_minimum_std_fresnel_speeds]
        final_median_corr_coeff = median_corr_coeffs[index_minimum_std_fresnel_speeds]
        
        final_index_t0 = best_indices_t0[index_minimum_std_fresnel_speeds]
    
        return std_fresnel_speeds, best_fresnel_speeds, median_corr_coeffs,  best_indices_t0
    
from numpy import hanning, hamming, blackman

def apply_blackman_filter(signal, fc_low, fc_high, N):
    # Filter signal with a band-pass Blackman filter
    
    n = np.arange(N)

    # Low-pass Blackman filter
    low_blackman_filter = np.sinc(2 * fc_low * (n - (N - 1) / 2.)) * blackman(N)
    low_blackman_filter = low_blackman_filter / np.sum(low_blackman_filter)

    # High-pass Blackman filter
    high_blackman_filter = np.sinc(2 * fc_high * (n - (N - 1) / 2.)) * blackman(N)
    high_blackman_filter = high_blackman_filter / np.sum(high_blackman_filter)
    high_blackman_filter = -high_blackman_filter  # Convert to high-pass
    high_blackman_filter[int(np.floor(N / 2))] = high_blackman_filter[int(np.floor(N / 2))] + 1

    # Convolution between high-pass and low-pass filters
    blackman_filter = np.convolve(low_blackman_filter, high_blackman_filter)

    b = blackman_filter
    a = np.array([1.])

    filtered_signal_blackman = filtfilt(b, a, signal, axis=0, padtype='odd', padlen = 3*(max(len(b),len(a))-1))

    return filtered_signal_blackman


from scipy.signal import butter, filtfilt, lfilter, bessel, cheby1, cheby2

def bandpass_butter_filter(signal, lowcut, highcut, fs, order=5):
    """
    Apply bandpass Butterworth filter to the input signal.

    Parameters:
    signal : array_like
        Input signal to be filtered.
    lowcut : float
        Lower cutoff frequency of the bandpass filter.
    highcut : float
        Upper cutoff frequency of the bandpass filter.
    fs : float
        Sampling frequency of the input signal.
    order : int, optional
        Order of the Butterworth filter. Default is 5.

    Returns:
    filtered_signal : array_like
        Filtered signal.

    """
    # Normalize cutoff frequencies
    low = lowcut / (0.5 * fs)
    high = highcut / (0.5 * fs)

    # Design Butter filter
    b, a = butter(order, [low, high], btype='bandpass')

    """ w, h = freqz(b, a)

    fig = plt.figure()
    plt.title('Digital filter frequency response')
    plt.plot(w * fs/(2*np.pi), 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude [dB]', color='b')
    plt.xlabel('Frequency [rad/sample]') """


    # Apply filter
    filtered_signal = filtfilt(b, a, signal)

    return filtered_signal


def hampel(data, window_size = 50, n_sigma = 3):
    """
    Applies the Hampel filter to a 1-dimensional numpy array for outlier detection.
    """

    half_window = window_size // 2
    data_len = len(data)
    filtered_data = data.copy()

    # Preallocate memory for threshold and outlier_indices arrays
    thresholds = np.empty(data_len, dtype=np.float32)
    outlier_indices = np.empty(data_len, dtype=np.int32)
    median_absolute_deviations = np.empty(data_len, dtype=np.float32)
    medians = np.empty(data_len, dtype=np.float32)

    num_outliers = 0

    for i in range(half_window, data_len - half_window):
        window = data[i - half_window: i + half_window + 1].copy()
        window_length = len(window)
        median = np.median(window)

        for j in range(window_length):
            window[j] = np.abs(window[j] - median)

        median_absolute_deviation = np.median(window)
        threshold = n_sigma * 1.4826 * median_absolute_deviation
        thresholds[i] = threshold
        median_absolute_deviations[i] = median_absolute_deviation
        medians[i] = median

        if abs(data[i] - median) > threshold:
            filtered_data[i] = median
            outlier_indices[num_outliers] = i
            num_outliers += 1


    return filtered_data