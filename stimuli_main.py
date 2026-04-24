import numpy as np
import random

def make_trials(stim_list, num_repetions):
    stim_pairs = []
    for stim in stim_list[1:]:
        stim_pairs.append([stim_list[0], stim])
        stim_pairs.append([stim, stim_list[0]])

    stim_pairs_repeat = stim_pairs * num_repetions
    stim_mapping = {i: stim_pairs_repeat[i] for i in range(len(stim_pairs_repeat))}
    
    trial_indices = list(stim_mapping.keys()) 
    random.shuffle(trial_indices) 

    return stim_mapping, trial_indices

stimuli = {'sound': {'frequency': np.linspace(1,3,3), 'duration': np.linspace(1,3,3)},
           'space': {'vertical_height': np.linspace(1,3,3), 'length': np.linspace(1,3,3)}}

blocks = {}
combinations = {}

for domain in stimuli:
    
    combinations[domain] = []
    params = list(stimuli[domain].keys())
    
    for param1 in stimuli[domain][params[0]]:
        for param2 in stimuli[domain][params[1]]:
            combinations[domain].append([int(param1),int(param2)])

    mapping, trial_indices = make_trials(combinations[domain], 1)
    
    blocks[domain] = {'mapping': mapping, 
                      'trial_indices': trial_indices,
                      'name': domain}

    
