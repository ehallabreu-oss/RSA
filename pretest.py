import pandas as pd
import numpy as np
import random
import sounddevice as sd
import tkinter as tk
from tkinter import simpledialog

# making the tones
def log_scale(min, max, num_steps):
    stimuli = np.empty(num_steps+1)
    for n in range(num_steps+1):
        stimuli[n] = min*(max/min)**(n/num_steps)
    return stimuli

def sine_tone(
        frequency: int=400,
        duration: float=0.5,
        amplitude: float=0.5,
        sample_rate: int=44100
        ) -> np.ndarray:
    
    n_samples = int(duration * sample_rate)
    
    time_points = np.linspace(0, duration, n_samples, False)
    sine = np.sin(2*np.pi*frequency*time_points) * amplitude

    return sine

frequency_stims = log_scale(400, 410, 12)


freq_pairs = []
for freq in frequency_stims[1:]:
    freq_pairs.append([float(frequency_stims[0]), float(freq)])
    freq_pairs.append([float(freq), float(frequency_stims[0])])

mapping = {i: freq_pairs[i] for i in range(len(freq_pairs))}

# Randomize order
trial_indices = list(mapping.keys()) # create a list of all indices
random.shuffle(trial_indices) # shuffle them randomly

# intialize variables
choices = ["first", "second"]
results = []

# ---------------------
# Experiment class
# ---------------------

class Experiment:
    def __init__(self, root):
        self.root = root       
        self.participant_id = participant_id

        # --- Start window ---
        self.start_label = tk.Label(root, text="Welcome to this experiment!", font=("Arial", 36))
        self.start_label.pack(pady=30)  
        self.instructions = tk.Label(root, text="You will hear 2 tones, one after the other.\n" \
        "Choose which from the 2 you think is highest.\n\n" \
        "2 tones will immediately play after you press space! \n\n" \
        "Press SPACE to begin", font=("Arial", 34))
        self.instructions.pack(pady=20)

        self.root.bind("<space>", self.start_experiment) # bind space key
  
        self.current_trial = -1 #so first increment lands at 0
        self.started = False  

    def start_experiment(self, event=None):
        if self.started: # if it started, space bar does nothing
            return None
        self.started = True

        # clears initial instructrions
        self.start_label.destroy()
        self.instructions.destroy()
        self.root.unbind("<space>")

        # between trial labels
        self.label = tk.Label(root, text="Which tone is the highest?", font=("Arial", 28))
        self.label.pack(pady=20) #add to the window with vertical padding
        self.message_label = tk.Label(root, text="", font=("Arial", 28))
        self.message_label.pack(pady=30)

        self.buttons = []
        for word in choices:
            button = tk.Button(root, text=word, font=("Arial", 24), width=12, height=2,
                               command=lambda choice=word: self.record_answer(choice))
            button.pack(pady=10)
            self.buttons.append(button)

        self.next_trial()

    def next_trial(self):
        self.message_label.config(text="") # clear message
        self.root.update_idletasks() # ensure clear message is drawn before playing
        for button in self.buttons:
            button.config(state="normal")
        self.current_trial += 1 # move to next trial

        # end experiment if no more trials
        if self.current_trial >= len(trial_indices):
            print("Experiment finished!")
            self.end_experiment()
            return None

        # play sound
        idx = trial_indices[self.current_trial] # get index of current trial
        freq_pair = mapping[idx]    # get corresponding frequency pair
        tone1 = sine_tone(frequency=freq_pair[0])
        tone2 = sine_tone(frequency=freq_pair[1])
        sd.play(tone1) 
        sd.wait()
        sd.play(tone2)
        sd.wait()

        #remember which stim was played
        self.current_idx = idx

    def record_answer(self, choice): 
        freq1, freq2 = freq_pairs[self.current_idx]
        
        if choice == "first":
            response = freq1
        else:
            response = freq2

        if freq1 > freq2:
            highest = freq1
        else:
            highest = freq2
   
        results.append({
            "index": self.current_idx,
            "freq1": freq1,
            "freq2": freq2,
            "response": response,
            "correct_response": highest,
            "score": 1 if response == highest else 0   
        })

        self.message_label.config(text="Next tone pair...")
        self.root.update_idletasks()
        for button in self.buttons:
            button.config(state="disabled")
        self.root.after(700, self.next_trial)
        
    def end_experiment(self):
        df = pd.DataFrame(results)
        file_name = f"{self.participant_id}_tone_discrimination_results.csv"
        df.to_csv(file_name, index=False)
        print(df)
        self.root.quit() #close window

# ---------------
# Run Experiment
# ---------------

root = tk.Tk() # create main window
root.geometry("900x800")
root.withdraw()
participant_id = simpledialog.askstring("Participant ID", "Enter your participant ID:")
root.deiconify()
Experiment(root) # create experiment object inside main window
root.mainloop() # start the GUI event loop