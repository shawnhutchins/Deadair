from tkinter import filedialog
from tktooltip import ToolTip
import customtkinter as ctk
import ffmpeg
import os

#add header Label
#check for mixed forward and backslashes in path
#add indication of success or failure
#add indication of progress
#make inputs for silence_threshold and min_silence_duration
#add something small to the output filename, first character for sorting

#Tries to run a ffmpeg filter silence remove on an input file
def remove_dead_air(input_file, output_file, silence_threshold=-30, min_silence_duration=0.5):
    """
    Removes dead air from a file using ffmpeg-python.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path for the output file with silence removed.
        silence_threshold (int): The volume level in dB below which audio is considered silence.
                                 Default is -30 dB.
        min_silence_duration (float): The minimum duration of silence (in seconds) to be removed.
                                      Default is 0.5 seconds.
    """
    try:
        (
            ffmpeg
            .input(input_file)
            .filter('silenceremove',
                    start_periods='0',  # Remove silence at the beginning
                    stop_periods='-1',  # Remove silence throughout the file
                    stop_duration=str(min_silence_duration),
                    detection='peak',
                    stop_threshold=str(silence_threshold) + 'dB')
            .output(output_file)
            .run(overwrite_output=True)
        )
        print(f"Dead air removed successfully. Output saved to: {output_file}")
    except ffmpeg.Error as e:
        print(f"Error removing dead air: {e.stderr.decode()}")

#Opens the folder select dialog and returns the file name
def select_folder():
    folder_name = filedialog.askdirectory(
        parent=window,
        title="Browse Folder"
    )
    return folder_name

#Opens the file select dialog and returns the file name
def select_file():
    file_name = filedialog.askopenfilename(
        parent=window,
        title="Browse File"
    )
    return file_name

#Sets input_var to selected folder
def select_input():
    input_var.set(select_folder())

#Sets output_var to selected folder
def select_output():
    output_var.set(select_folder())

#Gets the selected file, splits the file extension and stores it in file_type_var
def select_file_type():
    selected_file = select_file()
    _, file_extension = os.path.splitext(selected_file)
    file_type_var.set(file_extension)

#Precheckes before running
def validate_input():
    #check if any entries are empty
    if input_var.get() == "":
        print("Missing Input directory")
        return False
    if output_var.get() == "":
        print("Missing Output directory")
        return False
    if file_type_var.get() == "":
        print("Missing Filetype extension")
        return False
    # check if input and output are the same
    if input_var.get() == output_var.get():
        print("Input and Output should not be the same directory")
        return False
    return True

#Runs remove_dead_air() on every file in Input directory, of the selected file type
def script():
    try:
        for index, filename in enumerate(os.listdir(input_var.get())):
            _, file_extension = os.path.splitext(filename)
            if file_extension == file_type_var.get():
                remove_dead_air(os.path.join(input_var.get(), filename), os.path.join(output_var.get(), filename), db_var.get())
    except OSError as e:
        print(f"OS Error")

#Checks if the inputs are valid and if True, runs the script
def run():
    if validate_input():
        script()

#UI Constants
WINDOW_PADDING = 12
WIDGET_PADDING = 2
BUTTON_WIDTH = 60

#Main Window
window = ctk.CTk()
window.title("Dead Air Remove")
window.minsize(490, 154)
window.config(padx=WINDOW_PADDING, pady=WINDOW_PADDING)

#Entry Variables
input_var = ctk.StringVar()
output_var = ctk.StringVar()
file_type_var = ctk.StringVar()
db_var = ctk.IntVar()
db_var.set(-30)

#Header
header_title = ctk.CTkLabel(window, font=("Arial", 32, "bold"), text="DEAD AIR\nREMOVE")

#Main Content
content_frame = ctk.CTkFrame(window)

#Input, select the directory that contains the files you wish to process
input_select_button = ctk.CTkButton(content_frame, text="Input", command=select_input, width=BUTTON_WIDTH)
ToolTip(input_select_button, msg="Select a directory containing files to process")
input_entry = ctk.CTkEntry(content_frame, textvariable=input_var, width=400, state="readonly")

#Output, select a directory for your processed files to be placed in
output_select_button = ctk.CTkButton(content_frame, text="Output", command=select_output, width=BUTTON_WIDTH)
ToolTip(output_select_button, msg="Select a directory to export the processed files into")
output_entry = ctk.CTkEntry(content_frame, textvariable=output_var, width=400, state="readonly")

#Filetype, select a file to use its file extension
file_type_button = ctk.CTkButton(content_frame, text="Filetype", command=select_file_type, width=BUTTON_WIDTH)
ToolTip(file_type_button, msg="Select a file of the type you wish to process")
file_type_entry = ctk.CTkEntry(content_frame, textvariable=file_type_var, width=60, state="readonly", )

db_threshold_label = ctk.CTkLabel(content_frame, textvariable=db_var)
db_threshold_button = ctk.CTkButton(content_frame, text="dB", width=BUTTON_WIDTH)
db_threshold_slider = ctk.CTkSlider(content_frame, from_=-30, to=50, width=370, variable=db_var)

#Run Button
run_button = ctk.CTkButton(content_frame, text="Run", command=run, width= BUTTON_WIDTH)

#Configuring Grid
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

#Window Grid
header_title.grid(row=0, column=0, sticky="EW", pady=(10, 30))
content_frame.grid(row=1, column=0, sticky="EW")

#Content Frame Grid
input_select_button.grid(row=0, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
input_entry.grid(row=0, column=1, sticky="W", padx=WIDGET_PADDING, pady=WIDGET_PADDING)
output_select_button.grid(row=1, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
output_entry.grid(row=1, column=1, sticky="W", padx=WIDGET_PADDING, pady=WIDGET_PADDING)
file_type_button.grid(row=2, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
file_type_entry.grid(row=2, column=1, sticky="W", padx=WIDGET_PADDING, pady=WIDGET_PADDING)
db_threshold_label.grid(row=3, column=1, sticky="W", padx=WIDGET_PADDING + 6, pady=WIDGET_PADDING)
db_threshold_button.grid(row=3, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
db_threshold_slider.grid(row=3, column=1,sticky="E", padx=WIDGET_PADDING, pady=WIDGET_PADDING)
run_button.grid(row=4, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)

window.mainloop()
