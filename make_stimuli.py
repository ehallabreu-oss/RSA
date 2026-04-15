import numpy as np
import random

canvas_height = 400.0

def sine_tone(
        frequency: float=400.0,
        duration: float=0.5,
        amplitude: float=0.5,
        sample_rate: int=44100
        ) -> np.ndarray:
    
    n_samples = int(duration * sample_rate)
    
    time_points = np.linspace(0, duration, n_samples, False)
    sine = np.sin(2*np.pi*frequency*time_points) * amplitude

    return sine
    
def rectangle_coords(
    height: float=30.0,
    length: float=80.0,
    vertical_pos: float=20.0,
    horizontal_pos: float=10.0,
    canvas_height: float=canvas_height
    ):

    x1 = horizontal_pos
    x2 = x1 + length
    y1 = canvas_height - vertical_pos 
    y2 = y1 - height

    return x1, y1, x2, y2
def log_scale(min, max, num_steps):
    stimuli = np.empty(num_steps+1)
    for n in range(num_steps+1):
        stimuli[n] = min*(max/min)**(n/num_steps)
    return stimuli

def make_trials(stim_list):
    stim_pairs = []
    for stim in stim_list[1:]:
        stim_pairs.append([float(stim_list[0]), float(stim)])
        stim_pairs.append([float(stim), float(stim_list[0])])

    stim_mapping = {i: stim_pairs[i] for i in range(len(stim_pairs))}
    
    trial_indices = list(stim_mapping.keys()) 
    random.shuffle(trial_indices) 

    return stim_mapping, trial_indices


stimuli = {'frequency'   : [log_scale(400, 800, 1),
                            'Choose the HIGHEST tone'], 
           'duration'    : [log_scale(0.5, 1, 1),
                            'Choose the LONGEST tone'], 
           'vertical_pos': [log_scale(30, 60, 1),
                            'Choose the HIGHEST rectangle'],
           'length'      : [log_scale(80, 160, 1),
                            'Choose the LONGEST rectangle']}

blocks = {}
for stimulus in stimuli:
    mapping, trial_indices = make_trials(stimuli[stimulus][0])
    message = stimuli[stimulus][1]
    blocks[stimulus] = {'mapping': mapping, 
                        'trial_indices': trial_indices,
                        'instruction': message,
                        'name': stimulus}
    
print(stimuli['frequency'])
