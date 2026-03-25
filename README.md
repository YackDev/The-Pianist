# The-Pianist

A Python signal processing demo that synthesizes a short piano melody, corrupts it with random noise, and then identifies and removes that noise, comparing the results in both the time and frequency domains.

This script walks through a complete audio signal processing pipeline:

Synthesis: Builds a musical signal by layering ascending and descending C major scale notes with controlled timing.<br>
Noise injection: Adds two random-frequency sinusoidal noise tones to corrupt the signal.<br>
Noise identification: Uses FFT (Fast Fourier Transform) analysis to detect the noise frequencies in the spectrum.<br>
Filtering: Subtracts the estimated noise from the corrupted signal to recover the original.<br>
Visualization: Plots all three signals (original, noisy, filtered) in both time and frequency domains.<br>
Playback: Plays each version of the signal through your audio device.

To execute the program, just run the Python file.
