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
    height: int=30,
    length: int=80,
    vertical_pos: int=20,
    horizontal_pos: int=10,
    canvas_height: int=canvas_height
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

def make_trials(stim_list, num_repetions):
    stim_pairs = []
    for stim in stim_list[1:]:
        stim_pairs.append([float(stim_list[0]), float(stim)])
        stim_pairs.append([float(stim), float(stim_list[0])])

    stim_pairs_repeat = stim_pairs * num_repetions
    stim_mapping = {i: stim_pairs_repeat[i] for i in range(len(stim_pairs_repeat))}
    
    trial_indices = list(stim_mapping.keys()) 
    random.shuffle(trial_indices) 

    return stim_mapping, trial_indices

stimuli = {'frequency'   : [log_scale(400, 410, 8),
                            'You will hear two tones', 'Choose the HIGHEST tone'], 
           'duration'    : [log_scale(0.5, 0.7, 8),
                            'You will hear two tones', 'Choose the LONGEST tone'], 
           'vertical_pos': [np.arange(30, 38, 1),
                            'You will see two rectangles', 'Choose the HIGHEST rectangle'],
           'length'      : [np.arange(80, 88, 1),
                            'You will see two rectangles', 'Choose the LONGEST rectangle']}

blocks = {}
for stimulus in stimuli:
    mapping, trial_indices = make_trials(stimuli[stimulus][0], num_repetions=5)
    
    blocks[stimulus] = {'mapping': mapping, 
                        'trial_indices': trial_indices,
                        'block_instruction': f'{stimuli[stimulus][1]}\n\n{stimuli[stimulus][2]}',
                        'trial_instruction': stimuli[stimulus][2],
                        'name': stimulus}