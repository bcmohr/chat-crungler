import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
import logging, json
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

class NewprojectApp:
    def __init__(self, master=None):
        logging.info("Starting new project")

        # vectors and dictionaries to easily access ui data
        self.chat_frames = []    # Vector to store chat frames
        self.text_widgets = []   # Vector to store text widgets
        self.button_states = {}  # Dictionary to store the state of each button
        self.button_labels = ["User", "Assistant", "System"] # Vector to store the possible button labels

        # window frame and size
        self.window = ttk.Window(themename='darkly') if master is None else ttk.Toplevel(master)
        self.window.minsize(290, 600)
        self.window.title("The Chat Crungler")
        
        # top frame widgets
        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(fill="x", pady=5)

        # main frame widgets and scrollbar widget
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(expand=True, fill="both", side="top")
        
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        def _on_frame_configure(event):
            #logging.info("Starting frame configure function")
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.inner_frame.bind("<Configure>", _on_frame_configure)

        def scroll_canvas(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.canvas.bind_all("<MouseWheel>", scroll_canvas)

        def adjust_text_width(event):
            # Estimate the width of a character in pixels (adjust as needed)
            box_char_offset = 19
            approx_char_width_in_pixels = 6
            window_width = event.width

            # Calculate new width in characters (adjust the subtraction value as needed)
            new_width_in_chars = max(1, (window_width - (box_char_offset*approx_char_width_in_pixels)) // approx_char_width_in_pixels)

            # Update each text widget's width
            for text_widget in self.text_widgets:
                text_widget.configure(width=new_width_in_chars)
            
        # Bind the function to the window's configure event
        self.canvas.bind("<Configure>", adjust_text_width)

        # Function to add a new chat frame inside the inner_frame
        def add_chat_frame1(self, start_state='User', start_text=''):
            # chat item frame (frame3)
            ## button frame to the left of text
            frame_c = ttk.Frame(self.inner_frame)
            frame_c.configure(height=200, width=200)
            frame4 = ttk.Frame(frame_c)
            frame4.configure(height=200, width=400)
            button1 = ttk.Button(frame4, text=start_state, style='info.Outline.TButton', width=8)
            button1.pack(side="top", padx=2, pady=2, fill="x")
            self.button_states[button1] = 0  # Initial state set to 0 (system)
            # Set the command for button1 after it's created
            button1.configure(command=lambda btn=button1: self.cycle_button_label(btn))
            #button2 = ttk.Button(frame4, style='dark.TButton')
            #button2.configure(text='button2')
            #button2.pack(side="top", padx=2, pady=2, fill="x")
            #button3 = ttk.Button(frame4, style='dark.TButton')
            #button3.configure(text='button3')
            #button3.pack(side="top", padx=2, pady=2, fill="x")
            #button4 = ttk.Button(frame4, style='dark.TButton')
            #button4.configure(text='button4')
            #button4.pack(side="top", padx=2, pady=2, fill="x")
            # Update button5 to delete its parent frame
            button5 = ttk.Button(frame4, text='Delete', style='danger.Outline.TButton', command=lambda: self.delete_chat_frame2(frame_c))
            button5.pack(side="top", padx=2, pady=2, fill="x")
            frame4.pack(side="left")
            ## text frame to the right of button frame
            text1 = tk.Text(frame_c)
            text1.configure(height=4, width=10, wrap="word", )
            text1.pack(expand=True, fill="x", side="right", padx=5, pady=5)
            text1.insert("1.0", start_text)
            frame_c.pack(fill="x", padx=10, pady=10, side="top")
            self.chat_frames.append(frame_c)
            self.text_widgets.append(text1)
            # Pack and append to list
            self.window.update_idletasks()
            self.inner_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            #logging.info("Added new chat frame")
            #logging.info(self.chat_frames)
        
        

        

        top_button1 = ttk.Button(self.top_frame, text='Generate', style='success.Outline.TButton', width=16)
        top_button1["command"] = self.print_text
        top_button1.pack(side="left", padx=12, pady=12, )

        top_button2 = ttk.Button(self.top_frame, text="Add Message", command=self.add_chat_frame2, style='warning.Outline.TButton', width=16)
        top_button2.pack(side="left", padx=12, pady=12)

        combobox1_values = ["Base URL", 'http://localhost:8765/v1', 'http://localhost:8000/v1']
        self.combobox1 = ttk.Combobox(self.top_frame, values=combobox1_values, width=21)
        self.combobox1.pack(side="left", padx=12, pady=12)
        self.combobox1.set(combobox1_values[1])

        combobox2_values = ["Temp.", 0, 0.3, 0.5, 0.7, 1]
        self.combobox2 = ttk.Combobox(self.top_frame, values=combobox2_values, width=5)
        self.combobox2.pack(side="left", padx=12, pady=12)
        self.combobox2.set(combobox2_values[1])
        
        combobox3_values = ["Max Tok.", 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        self.combobox3 = ttk.Combobox(self.top_frame, values=combobox3_values, width=8)
        self.combobox3.pack(side="left", padx=12, pady=12)
        self.combobox3.set(combobox3_values[1])

        combobox4_values = ["Top_P", 1, 2, 4, 8, 16, 32, 64, 128]
        self.combobox4 = ttk.Combobox(self.top_frame, values=combobox4_values, width=5)
        self.combobox4.pack(side="left", padx=12, pady=12)
        self.combobox4.set(combobox4_values[1])

        combobox5_values = ["Fq. Pen.", 0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9, 1.1, 1.3]
        self.combobox5 = ttk.Combobox(self.top_frame, values=combobox5_values, width=4)
        self.combobox5.pack(side="left", padx=12, pady=12)
        self.combobox5.set(combobox5_values[1])

        combobox6_values = ["Pr. Pen.", 0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.9, 1.1, 1.3]
        self.combobox6 = ttk.Combobox(self.top_frame, values=combobox6_values, width=4)
        self.combobox6.pack(side="left", padx=12, pady=12)
        self.combobox6.set(combobox6_values[1])

        self.label_tx7 = ttk.Label(self.top_frame, text="Stop Tokens:")
        self.label_tx7.pack(side="left", padx=12, pady=12)
        
        textbox7_values = '["\\n", "User: "]'
        self.textbox7 = tk.Entry(self.top_frame, width=20)#, font=tk.font.Font(size=12))
        self.textbox7.pack(side="left", padx=12, pady=12, fill="y")
        self.textbox7.insert(0, textbox7_values)

        #add_chat_frame1(self, "System", "You are a helpful assistant. Answer professionally and concisely. Admit when you don't know enough to speak confidently on a topic.")
        #add_chat_frame1(self, "User",   "Write a quick email asking Brennan if he's available to meet. Make it sound like a riddle...")
        add_chat_frame1(self, "System", "Answer VERY briefly.")
        add_chat_frame1(self, "User",   "Are you an ai assistant?")

    def delete_chat_frame2(self, frame_to_delete):
        # Remove the frame from the UI
        frame_to_delete.pack_forget()
        frame_to_delete.destroy()

        # Update the chat_frames and text_widgets lists
        if frame_to_delete in self.chat_frames:
            index = self.chat_frames.index(frame_to_delete)
            self.chat_frames.remove(frame_to_delete)
            del self.text_widgets[index]

    # Function to add a new chat frame inside the inner_frame
    def add_chat_frame2(self, start_state='User', start_text=''):
        # chat item frame (frame3)
        ## button frame to the left of text
        frame_c = ttk.Frame(self.inner_frame)
        frame_c.configure(height=200, width=200)
        frame4 = ttk.Frame(frame_c)
        frame4.configure(height=200, width=200)
        button1 = ttk.Button(frame4, text=start_state, style='info.Outline.TButton', width=8)
        button1.pack(side="top", padx=2, pady=2, fill="x")
        self.button_states[button1] = 0  # Initial state set to 0 (system)
        # Set the command for button1 after it's created
        button1.configure(command=lambda btn=button1: self.cycle_button_label(btn))
        #button2 = ttk.Button(frame4, style='dark.TButton')
        #button2.configure(text='button2')
        #button2.pack(side="top", padx=2, pady=2, fill="x")
        #button3 = ttk.Button(frame4, style='dark.TButton')
        #button3.configure(text='button3')
        #button3.pack(side="top", padx=2, pady=2, fill="x")
        #button4 = ttk.Button(frame4, style='dark.TButton')
        #button4.configure(text='button4')
        #button4.pack(side="top", padx=2, pady=2, fill="x")
        # Update button5 to delete its parent frame
        button5 = ttk.Button(frame4, text='Delete', style='danger.Outline.TButton', command=lambda: self.delete_chat_frame2(frame_c))
        button5.pack(side="top", padx=2, pady=2, fill="x")
        frame4.pack(side="left")
        ## text frame to the right of button frame
        text1 = tk.Text(frame_c)
        text1.configure(height=6, width=10, wrap="word", )
        text1.pack(expand=True, fill="x", side="right", padx=5, pady=5)
        text1.insert("1.0", start_text)
        frame_c.pack(fill="x", padx=10, pady=10, side="top")
        self.chat_frames.append(frame_c)
        self.text_widgets.append(text1)
        # Pack and append to list
        self.window.update_idletasks()
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        #logging.info("Added new chat frame")
        #logging.info(self.chat_frames)

    def print_text(self):
        chat_contents = []
        for frame_c, text_widget in zip(self.chat_frames, self.text_widgets):
            frame4 = frame_c.winfo_children()[0]  # Assuming frame4 is the first child of frame_c
            role_button = frame4.winfo_children()[0]  # Assuming the role button is the first child of frame4
            role = role_button.cget("text").lower()  # Get the text of the button to determine the role

            text = text_widget.get("1.0", "end-1c")
            chat_contents.append({"role": role, "content": text})

        json_output = json.dumps(chat_contents, indent=4)
        #print(json_output)
        client = OpenAI(base_url=self.combobox1.get(), api_key="not-needed")
        stop = []
        stop = str(self.textbox7.get())
        completion = client.chat.completions.create(
            model="local-model",  # this field is currently unused
            messages=chat_contents,
            temperature=float(self.combobox2.get()),
            max_tokens=int(self.combobox3.get()), # Desired output length.
            top_p=int(self.combobox4.get()),
            frequency_penalty=float(self.combobox5.get()),
            presence_penalty=float(self.combobox6.get()),
            stop=json.loads(stop)  # Stop generating text when a string in this list is generated

        )
        # Print the result
        #print(completion.choices[0].message)
        self.add_chat_frame2("Assistant", completion.choices[0].message.content)

    def cycle_button_label(self, button):
        # Get current state of this button
            state = self.button_states[button]

            # Update the state
            new_state = (state + 1) % len(self.button_labels)
            self.button_states[button] = new_state

            # Update the button text
            button.configure(text=self.button_labels[new_state])


    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = NewprojectApp()
    app.run()
