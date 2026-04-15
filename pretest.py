import pandas as pd
from make_stimuli import blocks, sine_tone
import random
import sounddevice as sd
import tkinter as tk
from tkinter import simpledialog

block_indices = list(blocks.keys()) 
random.shuffle(block_indices)

isi = 0.4 # inter stimulus interval
canvas_width = 400.0
canvas_height = 400.0

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

# intialize variables
choices = ["first", "second"]
results = []

# ---------------------
# Experiment class
# ---------------------

class Experiment:
    def __init__(self, root):
        self.root = root       

        # Start window 
        self.start_label = tk.Label(root, text="Welcome to this experiment!", font=("Arial", 36))
        self.start_label.pack(pady=100)  
        self.instructions = tk.Label(root, text="You will either hear 2 tones OR see 2 rectangles\n" 
                                     "presented one after the other.\n\n\n" 
                                     "Press SPACE to continue", font=("Arial", 34))
        self.instructions.pack()
        
        # make canvas to draw rectangle later
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(expand=True, anchor='center')
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg='white')
        self.draw_canvas(False)

        self.root.bind("<space>", self.handle_events) 
        self.current_trial = -1 #so first increment lands at 0
        self.current_block = 0 
        self.waiting_for_block_start = True
        self.in_block = False
    
    def draw_canvas(self, visible): 
        if visible:
            self.canvas_frame.pack()
            self.canvas.pack()
        else:
            self.canvas_frame.pack_forget()
            self.canvas.pack_forget()
            

    def handle_events(self, event=None):
        # Blocks
        if self.waiting_for_block_start and not self.in_block:
            
            # clear screen if first block
            if hasattr(self, 'start_label'):
                self.start_label.destroy()
                self.instructions.destroy()

            # Set up UI if first time  
            if not hasattr(self, 'buttons'):

                self.message_label = tk.Label(root, text="", font=("Arial", 34))
                self.message_label.pack(pady=50)

                self.buttons = []
                for word in choices:
                    button = tk.Button(root, text=word, font=("Arial", 24), width=12, height=2,
                                    command=lambda choice=word: self.record_answer(choice))
                    button.pack()
                    self.buttons.append(button)

                # hide buttons
                for button in self.buttons:
                    button.pack_forget()
                self.root.update_idletasks()

            # Show task info
            block_type = block_indices[self.current_block]
            this_block = blocks[block_type]

            self.message_label.config(
                text=f'{this_block['block_instruction']}\n\nPress SPACE to start'       
            )

            self.this_block = this_block    # remember which block we are on
            self.waiting_for_block_start = False
            self.in_block = False
            return
        
        # Start trials
        if not self.waiting_for_block_start and not self.in_block:
            self.message_label.config(text="")  # clear old messages

            self.in_block = True
            self.current_trial = -1
            self.next_trial() 

    def flash_rectangles(self, first, second, block_name, delay, pause=int(1000*isi)):
        self.draw_canvas(True)

        for button in self.buttons:
            button.pack_forget()
        self.root.update_idletasks()
        
        
        if block_name == 'vertical_pos':
            coords1 = rectangle_coords(vertical_pos=first)
            coords2 = rectangle_coords(vertical_pos=second)
        else:
            coords1 = rectangle_coords(length=first)
            coords2 = rectangle_coords(length=second)

        self.rect1 = self.canvas.create_rectangle(*coords1, fill='black')

        def delete_first():
            self.canvas.delete(self.rect1)

        def show_second():
            self.rect2 = self.canvas.create_rectangle(*coords2, fill='black')
        
        def end_sequence():
            for button in self.buttons:
                button.pack(pady=10)
                button.config(state='normal') 

            self.canvas.delete(self.rect2)
            self.draw_canvas(False) 
            self.root.update_idletasks()
            
        self.root.after(delay, delete_first)
        self.root.after(delay+pause, show_second)
        self.root.after(pause+delay*2, end_sequence)
        
        
    def next_trial(self):
        self.message_label.config(text="") # clear message
        self.root.update_idletasks() # ensure clear message is drawn before playing
        
        # update trial counter
        self.current_trial += 1 
        
        # play sound
        stim_mapping = self.this_block['mapping']
        trial_indices = self.this_block['trial_indices']
        trial_idx = trial_indices[self.current_trial]
        
        first, second = stim_mapping[trial_idx]

        if self.this_block['name'] == 'frequency' or self.this_block['name'] == 'duration':

            for button in self.buttons:
                button.pack(pady=10)
                button.config(state='normal')
                self.root.update_idletasks()
                
            if self.this_block['name'] == 'frequency':
                tone1 = sine_tone(frequency=first)
                tone2 = sine_tone(frequency=second)
            else:
                tone1 = sine_tone(duration=first)
                tone2 = sine_tone(duration=second)
            
            silence = sine_tone(amplitude=0, duration=isi)
            
            sd.play(tone1)
            sd.wait()
            sd.play(silence)
            sd.wait()
            sd.play(tone2)
            sd.wait()  

        else:
            self.flash_rectangles(first, second, self.this_block['name'], 1000)
            self.root.update_idletasks()

                        
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

        # hide buttons and canvas
        for button in self.buttons:
            button.pack_forget()
        self.draw_canvas(False)

        self.message_label.config(
            text="You've finished a block! \n\n" \
            "Now the stimuli will change. \n\n" \
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

        self.message_label.config(text=self.this_block['trial_instruction'])
        self.root.update_idletasks()
        for button in self.buttons:
            button.config(state="disabled")
        
        trial_indices = self.this_block['trial_indices']

        if self.current_trial + 1 >= len(trial_indices):
            self.next_block()
        else:
            self.root.after(400, self.next_trial)
        
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