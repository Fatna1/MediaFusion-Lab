#Fourier Transform (FFT) Algorithm

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
import os

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists('output'):
        os.makedirs('output')

def fourier_transform_analysis(audio_path):
    #Algorithm 5: Fourier Transform for frequency analysis
    
    try:
        # Read audio file
        sample_rate, audio_data = wavfile.read(audio_path)
        
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalize audio data
        audio_data = audio_data / np.max(np.abs(audio_data))
        
        # Apply Fourier Transform
        # Formula: X(k) = Σ x(n) * e^(-j2πkn/N)
        fft_values = fft(audio_data)
        
        # Get frequency bins
        n = len(audio_data)
        frequencies = np.fft.fftfreq(n, 1/sample_rate)
        
        # Get magnitude spectrum (only positive frequencies)
        positive_freqs = frequencies[:n//2]
        magnitude_spectrum = np.abs(fft_values[:n//2])
        
        # Create plot
        ensure_output_dir()
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Time domain signal
        plt.subplot(2, 1, 1)
        time_axis = np.arange(len(audio_data)) / sample_rate
        plt.plot(time_axis, audio_data)
        plt.title('Time Domain Signal (Original Audio)')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        # Plot 2: Frequency spectrum
        plt.subplot(2, 1, 2)
        plt.plot(positive_freqs, magnitude_spectrum)
        plt.title('Frequency Domain (FFT Magnitude Spectrum)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)
        plt.xlim(0, sample_rate//2)  # Limit to Nyquist frequency
        
        plt.tight_layout()
        output_path = 'output/fft_plot.png'
        plt.savefig(output_path)
        plt.close()
        
        # Find dominant frequencies
        top_indices = np.argsort(magnitude_spectrum)[-5:]
        top_frequencies = positive_freqs[top_indices]
        
        result_msg = (f"FFT Analysis complete.\n"
                      f"Mathematical principle: FFT converts time domain to frequency domain.\n"
                      f"Formula: X(k) = Σ x(n) * e^(-j2πkn/N)\n"
                      f"Sample rate: {sample_rate} Hz\n"
                      f"Audio duration: {len(audio_data)/sample_rate:.2f} seconds\n"
                      f"Dominant frequencies (Hz): {', '.join([f'{f:.1f}' for f in top_frequencies])}\n"
                      f"Spectrum plot saved to {output_path}")
        
        return output_path, result_msg
        
    except Exception as e:
        return None, f"Error processing audio: {str(e)}"
#Noise Reduction (Low-pass Filter)
def noise_reduction(audio_path, cutoff_freq=1000):
    """
    Algorithm 6: Simple noise reduction using low-pass filter
    Principle: Remove high-frequency components (noise) by applying FFT, 
               zeroing high frequencies, then inverse FFT
    Formula: 
        - Apply FFT: X(f) = FFT(x(t))
        - Apply filter: X_filtered(f) = X(f) for |f| < cutoff, else 0
        - Inverse FFT: x_filtered(t) = IFFT(X_filtered(f))
    """
    try:
        # Read audio file
        sample_rate, audio_data = wavfile.read(audio_path)
        
        # Convert to mono if stereo
        original_shape = audio_data.shape
        if len(original_shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalize
        audio_data = audio_data / np.max(np.abs(audio_data))
        
        # Apply Fourier Transform
        fft_values = fft(audio_data)
        
        # Create low-pass filter in frequency domain
        n = len(fft_values)
        freqs = np.fft.fftfreq(n, 1/sample_rate)
        
        # Formula: keep frequencies below cutoff_freq, zero out higher frequencies
        filter_mask = np.abs(freqs) <= cutoff_freq
        filtered_fft = fft_values * filter_mask
        
        # Apply inverse FFT to get filtered signal
        # Formula: x_filtered(t) = IFFT(X_filtered(f))
        filtered_audio = np.real(ifft(filtered_fft))
        
        # Normalize filtered audio
        filtered_audio = filtered_audio / np.max(np.abs(filtered_audio))
        
        # Convert back to original format (16-bit PCM)
        filtered_audio_int16 = (filtered_audio * 32767).astype(np.int16)
        
        # Restore stereo if original was stereo
        if len(original_shape) > 1:
            filtered_audio_int16 = np.column_stack([filtered_audio_int16, filtered_audio_int16])
        
        # Save filtered audio
        ensure_output_dir()
        output_path = 'output/noise_reduced.wav'
        wavfile.write(output_path, sample_rate, filtered_audio_int16)
        
        # Create comparison plot
        plt.figure(figsize=(12, 8))
        
        # Original audio FFT
        plt.subplot(2, 1, 1)
        original_fft = np.abs(fft(audio_data))
        freqs_plot = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        plt.plot(freqs_plot[:len(freqs_plot)//2], original_fft[:len(original_fft)//2])
        plt.title('Original Audio Frequency Spectrum (Before Noise Reduction)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)
        plt.xlim(0, sample_rate//2)
        
        # Filtered audio FFT
        plt.subplot(2, 1, 2)
        filtered_fft_plot = np.abs(fft(filtered_audio))
        plt.plot(freqs_plot[:len(freqs_plot)//2], filtered_fft_plot[:len(filtered_fft_plot)//2])
        plt.title(f'Filtered Audio Frequency Spectrum (Low-pass filter, cutoff={cutoff_freq}Hz)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)
        plt.xlim(0, sample_rate//2)
        
        plt.tight_layout()
        comparison_path = 'output/noise_reduction_comparison.png'
        plt.savefig(comparison_path)
        plt.close()
        
        result_msg = (f"Noise reduction complete using low-pass filter.\n"
                      f"Mathematical principle: Apply FFT, zero high frequencies (> {cutoff_freq} Hz), then IFFT.\n"
                      f"Formula: X_filtered(f) = X(f) for |f| < {cutoff_freq}, else 0\n"
                      f"              x_filtered(t) = IFFT(X_filtered(f))\n"
                      f"Cutoff frequency: {cutoff_freq} Hz\n"
                      f"Output saved to {output_path}\n"
                      f"Comparison plot saved to {comparison_path}")
        
        return output_path, result_msg
        
    except Exception as e:
        return None, f"Error processing audio: {str(e)}"

# Test functions
if __name__ == "__main__":
    print("Audio Algorithms Module")
    print("-" * 30)
    print("Functions available:")
    print("1. fourier_transform_analysis(audio_path)")
    print("2. noise_reduction(audio_path, cutoff_freq=1000)")