import numpy as np
import sounddevice as sd
import random

def log_scale(min, max, num_steps):
    stimuli = np.empty(num_steps+1)
    for n in range(num_steps+1):
        stimuli[n] = min*(max/min)**(n/num_steps)
    return stimuli

def sine_tone(
        frequency: int=400,
        duration: float=1.0,
        amplitude: float=0.5,
        sample_rate: int=44100
        ) -> np.ndarray:
    
    n_samples = int(duration * sample_rate)
    
    time_points = np.linspace(0, duration, n_samples, False)
    sine = np.sin(2*np.pi*frequency*time_points) * amplitude

    return sine

frequency_stimuli = log_scale(400, 430, 12)
duration_list = log_scale(1, 2, 12)
duration_stims = log_scale(0.5, 1, 12)

tone_pairs = []
for tone in frequency_stimuli[1:]:
    tone_pairs.append([float(frequency_stimuli[0]), float(tone)])
    tone_pairs.append([float(tone), float(frequency_stimuli[0])])

mapping = {i: tone_pairs[i] for i in range(len(tone_pairs))}

# Randomize order
trial_indices = list(mapping.keys()) # create a list of all indices
random.shuffle(trial_indices) # shuffle them randomly

print(mapping)
print(trial_indices)

# for freq in frequency_list:
#     mysound = sine_tone(frequency=freq)
#     sd.play(mysound)
#     sd.wait()

# for dur in duration_list:
#     mysound = sine_tone(duration=dur)
#     sd.play(mysound)
#     sd.wait()

mysound = sine_tone(frequency=frequency_stimuli[12])
sd.play(mysound)
sd.wait()

