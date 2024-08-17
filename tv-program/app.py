from tkinter import *
from PIL import ImageTk, Image
import json
import webbrowser
import subprocess


# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Function to make a window fullscreen
def set_fullscreen(window):
    window.attributes('-fullscreen', True)

# Function to exit fullscreen mode
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

# Creating Tkinter object
root = Tk()

# Gives the window a title
root.title("Interactive Application")

# Set main window to fullscreen
set_fullscreen(root)

# Can be used to configure cursor background etc.
root.configure(cursor='dot')

# To show image
img = Image.open('tv.png')
resized_img = img.resize((100, 100))
img = ImageTk.PhotoImage(resized_img)

img_label = Label(root, image=img)
img_label.pack(pady=(10, 10))

text_label = Label(root, text='EasyTV')
text_label.pack()
text_label.config(font=('verdana', 24))

for i in range(6):
    block_frame = Frame(root, width=150, height=90, relief="solid")
    block_frame.pack()

    block_text = Label(root, text=data['texts'][i], font=("verdana", 30))
    block_text.pack()

# Store buttons in a list for navigation
option_buttons = []
current_selection = -1  # To track the selected button index
option_window = None  # To hold the reference to the new window

def open_link_in_browser(link):
    webbrowser.open(link)
    # Bring focus back to the Tkinter window after opening the link
    if option_window is not None and option_window.winfo_exists():
        option_window.focus_force()  # Focus on the options window
    else:
        root.focus_force()  # Focus on the main window if no options window exists

    # Bind the 'f' key to refocus on Tkinter after opening the link
    root.bind_all('<KeyPress-f>', lambda event: refocus_to_tkinter())

def refocus_to_tkinter():
    if option_window is not None and option_window.winfo_exists():
        option_window.focus_force()  # Focus on the options window
    else:
        root.focus_force()  # Focus on the main window

def return_to_previous(event):
    global option_window
    if option_window is not None and option_window.winfo_exists():
        option_window.destroy()

def click_button(event):
    if option_buttons:
        option_buttons[current_selection].invoke()

def show_options(key):
    global option_buttons, current_selection, option_window
    
    # Destroy previous window if it exists
    if option_window is not None and option_window.winfo_exists():
        option_window.destroy()
    
    # Get the options and heading from the JSON data
    options = data.get(f"{key}_options", [])
    heading = data.get(f"{key}_heading", "Options")

    # Create a new top-level window
    option_window = Toplevel(root)
    option_window.title("Select Option")
    
    # Set the new window to fullscreen
    set_fullscreen(option_window)

    # Add heading label
    heading_label = Label(option_window, text=heading, font=('verdana', 24))
    heading_label.pack(pady=(10, 10))

    option_buttons = []
    current_selection = 0

    for option in options:
        option_button = Button(option_window, text=option['text'], font=('verdana', 24), width=30, height=2, command=lambda l=option['link']: open_link_in_browser(l))
        option_button.pack(pady=10)
        option_buttons.append(option_button)

    highlight_selection()

    # Bind arrow keys to the new window for navigation
    option_window.bind('<Up>', lambda event: move_selection(-1))
    option_window.bind('<Down>', lambda event: move_selection(1))
    option_window.bind('<Return>', click_button)  # Enter key to click button
    option_window.bind('<space>', return_to_previous)  # Spacebar to return

    # Set focus to the window itself to ensure it captures key events
    option_window.focus_set()

    # Ensure the first button has focus
    if option_buttons:
        option_buttons[0].focus_set()

def highlight_selection():
    for i, button in enumerate(option_buttons):
        if i == current_selection:
            button.config(bg='lightblue')
            button.focus_set()  # Set focus to the highlighted button
        else:
            original_bg = button.master.cget('bg')  # Get the original background color
            button.config(bg=original_bg)

def move_selection(num):
    global current_selection
    current_selection = (current_selection + num) % len(option_buttons)
    highlight_selection()

def update_display(event):
    key = event.keysym.lower()
    if key in ['n', 'i', 'e', 'm', 'c']:
        show_options(key)
    
    if key == 'l':
        subprocess.run(['python3', 'web-scraping.py'])
        

def global_key_handler(event):
    key = event.keysym.lower()
    if key in ['n', 'i', 'e', 'm', 'c','l']:
        update_display(event)

# Bind key presses to the function for selecting n, i, e, m,l or c
root.bind_all('<KeyPress-n>', global_key_handler)
root.bind_all('<KeyPress-i>', global_key_handler)
root.bind_all('<KeyPress-e>', global_key_handler)
root.bind_all('<KeyPress-m>', global_key_handler)
root.bind_all('<KeyPress-c>', global_key_handler)
root.bind_all('<KeyPress-f>', lambda event: refocus_to_tkinter())
root.bind_all('<KeyPress-l>', global_key_handler)


# Bind the Escape key to exit fullscreen
root.bind('<Escape>', exit_fullscreen)

# Keeps the GUI on the main screen
root.mainloop()
