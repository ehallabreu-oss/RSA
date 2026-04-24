import numpy as np

stimuli = {'sound': {'frequency': np.linspace(1,3,3), 'duration': np.linspace(1,3,3)},
           'space': {'vertical_height': np.linspace(1,3,3), 'length': np.linspace(1,3,3)}}


combinations_sound = []
for freq in stimuli['sound']['frequency']:
    for dur in stimuli['sound']['duration']:
        combinations_sound.append([int(freq), int(dur)])

combinations_space = []
for height in stimuli['space']['vertical_height']:
    for length in stimuli['space']['length']:
        combinations_sound.append([int(height), int(length)])