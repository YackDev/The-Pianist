import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft

fs = 44100
duration = 3
t = np.linspace(0, duration, duration * fs)

F_i = [130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94]
f_i = [246.94, 220.00, 196.00, 174.61, 164.81, 146.83, 130.81]
all_notes = F_i + f_i

x = np.zeros_like(t)
T_i = [0.4, 0.6, 0.3, 0.5, 0.5, 0.3, 0.4]
t_i = [0.0, 0.4, 1.0, 1.3, 1.8, 2.3, 2.6]

for i in range(7):
    u = np.where(np.logical_and(t >= t_i[i], t <= t_i[i] + T_i[i]), 1, 0)
    x += np.sin(2 * np.pi * F_i[i] * t) * u
    x += np.sin(2 * np.pi * f_i[i] * t) * u

sd.play(x, 3 * fs)
sd.wait()

fn1, fn2 = np.random.randint(0, 512, 2)
print("Noise 1 =", fn1, "\nNoise 2 =", fn2)

noise = np.sin(2 * np.pi * fn1 * t) + np.sin(2 * np.pi * fn2 * t)

x_n = x + noise
sd.play(x_n, 3 * fs)
sd.wait()

N = len(t)
f = np.linspace(0,44100/2,int(N/2))
x_n_fft = fft(x_n)
x_n_mag = 2/N * np.abs(x_n_fft[:N//2])

threshold = 0.2 * np.max(x_n_mag)
peaks = []
for i in range(len(f)):
    if x_n_mag[i] > threshold and all(abs(f[i] - note) > 10 for note in all_notes):
        peaks.append((x_n_mag[i], f[i]))

peaks.sort(reverse=True)
if len(peaks) >= 2:
    fn1_identified, fn2_identified = peaks[0][1], peaks[1][1]
else:
    fn1_identified, fn2_identified = fn1, fn2

estimated_noise = (np.sin(2 * np.pi * fn1_identified * t) + np.sin(2 * np.pi * fn2_identified * t))

x_filtered = x_n - estimated_noise

plt.figure()

plt.subplot(3, 1, 1)
plt.plot(t, x)
plt.title('Original Signal (Time Domain)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, 0.8)

plt.subplot(3, 1, 2)
plt.plot(t, x_n)
plt.title('Noisy Signal (Time Domain)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, 0.8)

plt.subplot(3, 1, 3)
plt.plot(t, x_filtered)
plt.title('Filtered Signal (Time Domain)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, 0.8)

plt.tight_layout()
plt.show()

plt.figure()

plt.subplot(3, 1, 1)
plt.plot(f, 2/N * np.abs(fft(x)[:N//2]))
plt.title('Original Signal (Frequency Domain)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.xlim(0, 512)

plt.subplot(3, 1, 2)
plt.plot(f, x_n_mag)
plt.title('Noisy Signal (Frequency Domain)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.xlim(0, 512)

plt.subplot(3, 1, 3)
plt.plot(f, 2/N * np.abs(fft(x_filtered)[:N//2]))
plt.title('Filtered Signal (Frequency Domain)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.xlim(0, 512)

plt.tight_layout()
plt.show()

sd.play(x_filtered, 3 * fs)