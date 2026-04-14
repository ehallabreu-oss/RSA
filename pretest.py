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

frequency_stims = log_scale(400, 800, 1)

duration_stims = log_scale(0.5, 1, 1)

def make_trials(stim_list):
    stim_pairs = []
    for stim in stim_list[1:]:
        stim_pairs.append([float(stim_list[0]), float(stim)])
        stim_pairs.append([float(stim), float(stim_list[0])])

    stim_mapping = {i: stim_pairs[i] for i in range(len(stim_pairs))}
    
    trial_indices = list(stim_mapping.keys()) # create a list of all indices
    random.shuffle(trial_indices) # shuffle them randomly

    return stim_mapping, trial_indices

freq_mapping, freq_trial_indices = make_trials(frequency_stims)
dur_mapping, dur_trial_indices = make_trials(duration_stims)

blocks = {'frequency' : {'mapping': freq_mapping, 
               'trial_indices': freq_trial_indices, 
               'name': 'frequency', 
               'instruction': 'Choose the HIGHEST tone'}, 
          'duration' : {'mapping': dur_mapping, 
               'trial_indices': dur_trial_indices, 
               'name': 'duration', 
               'instruction': 'Choose the LONGEST tone'}}

block_indices = list(blocks.keys()) 
random.shuffle(block_indices)

# intialize variables
choices = ["first", "second"]
results = []

# ---------------------
# Experiment class
# ---------------------

class Experiment:
    def __init__(self, root):
        self.root = root       

        # --- Start window ---
        self.start_label = tk.Label(root, text="Welcome to this experiment!", font=("Arial", 36))
        self.start_label.pack(pady=30)  
        self.instructions = tk.Label(root, text="You will hear 2 tones, one after the other.\n" \
        "Choose which from the 2 you think is highest.\n\n" \
        "Press SPACE to continue", font=("Arial", 34))
        self.instructions.pack(pady=20)

        self.root.bind("<space>", self.handle_events) # bind space key
  
        self.current_trial = -1 #so first increment lands at 0
        self.current_block = 0 
        self.waiting_for_block_start = True
        self.in_block = False

    def handle_events(self, event=None):

        # Blocks
        if self.waiting_for_block_start and not self.in_block:
            
            # clear screen if first block
            if hasattr(self, 'start_label'):
                self.start_label.destroy()
                self.instructions.destroy()

            # Set up UI if first time  
            if not hasattr(self, 'buttons'):

                self.message_label = tk.Label(root, text="", font=("Arial", 28))
                self.message_label.pack(pady=70)

                self.buttons = []
                for word in choices:
                    button = tk.Button(root, text=word, font=("Arial", 24), width=12, height=2,
                                    command=lambda choice=word: self.record_answer(choice))
                    button.pack(pady=10)
                    self.buttons.append(button)

                # hide buttons
                for button in self.buttons:
                    button.pack_forget()

            # Show task info
            block_type = block_indices[self.current_block]
            this_block = blocks[block_type]
            self.this_block = this_block    # remember which block we are on

            self.message_label.config(
                text=f'{this_block['instruction']}\n\nPress SPACE to start'       
            )

            self.waiting_for_block_start = False
            self.in_block = False
            return
        
        # Start trials
        if not self.waiting_for_block_start and not self.in_block:
            self.message_label.config(text="")  # clear old messages

            for button in self.buttons:
                button.pack(pady=10)
                button.config(state='normal')

            self.in_block = True
            self.current_trial = -1
            self.next_trial() 

    def next_trial(self):
        self.message_label.config(text="") # clear message
        self.root.update_idletasks() # ensure clear message is drawn before playing
        for button in self.buttons:
            button.config(state="normal")
        
        # update trial counter
        self.current_trial += 1 
        
        # play sound
        stim_mapping = self.this_block['mapping']
        trial_indices = self.this_block['trial_indices']
        trial_idx = trial_indices[self.current_trial]
        
        first, second = stim_mapping[trial_idx]

        if self.this_block['name'] == 'frequency':
            tone1 = sine_tone(frequency=first)
            tone2 = sine_tone(frequency=second)
        else:
            tone1 = sine_tone(duration=first)
            tone2 = sine_tone(duration=second)

        sd.play(tone1) 
        sd.wait()
        sd.play(tone2)
        sd.wait()
    
        #remember which stim was played 
        self.first = first
        self.second = second
        self.current_trial_idx = trial_idx

    def next_block(self):
        self.current_block += 1

        if self.current_block >= len(blocks):
            print("Experiment finished!")
            self.end_experiment()
            return None

        # hide buttons
        for button in self.buttons:
            button.pack_forget()

        self.message_label.config(
            text="You've finished a block! \n\n" \
            "Now the stimuli will change. \n\n" \
            f"{self.this_block['instruction']}\n\n" \
            "Press SPACE to continue"
        )
    
        self.waiting_for_block_start = True
        self.in_block = False
          
    def record_answer(self, choice): 
        first = self.first
        second = self.second

        if choice == "first":
            response = first
        else:
            response = second

        if first > second:
            highest = first
        else:
            highest = second
   
        results.append({
            "index": self.current_trial_idx,
            "block": self.this_block['name'],
            "first": first,
            "second": second,
            "response": response,
            "correct_response": highest,
            "score": 1 if response == highest else 0   
        })

        self.message_label.config(text=self.this_block['instruction'])
        self.root.update_idletasks()
        for button in self.buttons:
            button.config(state="disabled")
        
        trial_indices = self.this_block['trial_indices']

        if self.current_trial + 1 >= len(trial_indices):
            self.next_block()
        else:
            self.root.after(500, self.next_trial)
        
    def end_experiment(self):
        df = pd.DataFrame(results)
        file_name = f"tone_discrimination_results.csv"
        df.to_csv(file_name, index=False)
        print(df)
        self.root.quit() #close window

# ---------------
# Run Experiment
# ---------------

root = tk.Tk() # create main window
root.geometry("900x800")
root.withdraw()
root.deiconify()
Experiment(root) # create experiment object inside main window
root.mainloop() # start the GUI event loop