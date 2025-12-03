from CTkToolTip import CTkToolTip as ToolTip
from tkinter import filedialog
import customtkinter as ctk
import threading
import ffmpeg
import os

# -----TASKS-----
#add a test button that fills the entries with the testing values for faster testing
#verify and or create input and output testing directories, no audio file may be ok
#style console print commands like make success msg green
#make a tab window that shows the command line
#add an entry for the file prefix with a default of DAR_
#add validation for the file prefix to make sure there are no special/illegal characters
#add validation for the file type to ensure that ffmpeg can process the file
#fix resizing of the window
# -----CONSIDERING-----
#add indication of success or failure
#check for mixed forward and backslashes in path
#put tooltips on the sliders to show the value of the slider
#disable widgets while processing files
#import only required parts of packages

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

#Button command to set the default dB value
def default_db_threshold():
    db_var.set(-30)

#Button command to set the default minimum silence duration
def default_min_silence():
    silence_var.set(0.5)

#Resets the progress bar state to 0 and updates the window
def progress_reset():
    progress_bar.set(0)
    window.update()

#Updates the value of the progress bar and then updates the window
def progress_update(current_value, max_value):
    normalize_value = (current_value + 1) / max_value
    progress_bar.set(normalize_value)
    window.update()

#Manages the different states that the run button can have
def run_button_update_state(state):
    match state:
        case "run":
            run_button.configure(text="Run", fg_color="SpringGreen4", hover_color="dark green", state="normal", command=run)
            run_button_tooltip.configure(message="Removes all dead air from each file in the input folder of the "
                                                "chosen filetype and saves the file in the output folder.")
        case "running":
            run_button.configure(text="Cancel", fg_color="red3", hover_color="red4", command=cancel_script_loop)
            run_button_tooltip.configure(message="Cancel the loop and finish the current file.")
        case "canceling":
            run_button.configure(text="⏳", state="disabled", fg_color="red4")
            run_button_tooltip.configure(message="Finishing last file, please wait.")
        case _:
            print(f"Unknown state for the run button. state: {state}")

#Cancels the script loop and communicates the cancel button has been pressed
def cancel_script_loop():
    cancel_loop_var.set(True)
    #Change run button to "finishing loop" state
    run_button_update_state("canceling")
    print("Script Canceled")

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
    run_button_update_state("running")
    try:
        for index, filename in enumerate(os.listdir(input_var.get())):
            if cancel_loop_var.get():
                break
            _, file_extension = os.path.splitext(filename)
            if file_extension == file_type_var.get():
                remove_dead_air(
                    os.path.join(input_var.get(), filename),
                    os.path.join(output_var.get(), FILE_PREFIX + filename),
                    db_var.get(),
                    silence_var.get()
                )
            progress_bar_tooltip.configure(message=f"{index + 1}/{len(os.listdir(input_var.get()))} files in directory")
            progress_update(index + 1, len(os.listdir(input_var.get())))
    except OSError as e:
        print(f"OS Error")
    run_button_update_state("run")
    cancel_loop_var.set(False)

#Checks if the inputs are valid and if True, runs the script
def run():
    if validate_input():
        progress_reset()
        script_thread = threading.Thread(target=script)
        script_thread.start()

def testing_fill_data():
    input_var.set("input")
    output_var.set("output")
    file_type_var.set(".m4a")

#UI Constants
WINDOW_PADDING = 12
WIDGET_PADDING = 2
BUTTON_WIDTH = 60
FILE_PREFIX = "DAR_"
TOOLTIP_DELAY = 0.05
TOOLTIP_BORDER_WIDTH = 2
TOOLTIP_BORDER_COLOR = "gray36"
TESTING = False

#Set Default Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#Main Window
window = ctk.CTk()
window.title("Dead Air Remove")
window.minsize(490, 216)
window.config(padx=WINDOW_PADDING, pady=WINDOW_PADDING)

#Widget Variables
input_var = ctk.StringVar()
output_var = ctk.StringVar()
file_type_var = ctk.StringVar()
db_var = ctk.IntVar(value=-30)
silence_var = ctk.DoubleVar(value=0.5)
cancel_loop_var = ctk.BooleanVar(value=False)

#Header
header_title = ctk.CTkLabel(window, font=("Arial", 32, "bold"), text="DEAD AIR\nREMOVE")

#Main Content
content_frame = ctk.CTkFrame(window)

#Input, select the directory that contains the files you wish to process
input_select_button = ctk.CTkButton(content_frame, text="Input", command=select_input, width=BUTTON_WIDTH)
input_entry = ctk.CTkEntry(content_frame, textvariable=input_var, width=400, state="readonly")

#Output, select a directory for your processed files to be placed in
output_select_button = ctk.CTkButton(content_frame, text="Output", command=select_output, width=BUTTON_WIDTH)
output_entry = ctk.CTkEntry(content_frame, textvariable=output_var, width=400, state="readonly")

#Filetype, select a file to use its file extension
file_type_button = ctk.CTkButton(content_frame, text="Filetype", command=select_file_type, width=BUTTON_WIDTH)
file_type_entry = ctk.CTkEntry(content_frame, textvariable=file_type_var, width=60, state="readonly")

#dB Threshold slider
db_threshold_button = ctk.CTkButton(content_frame, text="dB", command=default_db_threshold, width=BUTTON_WIDTH)
db_threshold_label = ctk.CTkLabel(content_frame, textvariable=db_var)
db_threshold_slider = ctk.CTkSlider(content_frame, from_=-30, to=50, width=370, variable=db_var)

#Minimum Silence Duration slider
min_silence_button = ctk.CTkButton(content_frame, text="Silence", command=default_min_silence, width=BUTTON_WIDTH)
min_silence_label = ctk.CTkLabel(content_frame, textvariable=silence_var)
min_silence_slider = ctk.CTkSlider(content_frame, from_=0, to=10, width=370, variable=silence_var)

#Run Button
run_button = ctk.CTkButton(content_frame, text="Run", command=run, width=BUTTON_WIDTH, fg_color="SpringGreen4", hover_color="dark green")

#Progress Bar
progress_bar = ctk.CTkProgressBar(content_frame, orientation="horizontal", width=380, height=20, progress_color="#729A65")
progress_bar.set(0)

#ToolTips
ToolTip(input_select_button, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="Select a directory containing files to process")
ToolTip(output_select_button, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="Select a directory to export the processed files into")
ToolTip(file_type_button, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="Select a file of the type you wish to process")
ToolTip(db_threshold_button, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="The volume level in dB below which audio is considered silence. Default is -30 dB")
ToolTip(min_silence_button, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="The minimum duration of silence (in seconds) to be removed. Default is 0.5 seconds.")
run_button_tooltip = ToolTip(run_button, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="Removes all dead air from each file in the input folder of the "
            "chosen filetype and saves the file in the output folder.")
progress_bar_tooltip = ToolTip(progress_bar, delay=TOOLTIP_DELAY, border_color=TOOLTIP_BORDER_COLOR, border_width=TOOLTIP_BORDER_WIDTH,
    message="0/0 files in directory")

#Configuring Grid -----------------------------------------------------------------------------------------------------
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

db_threshold_button.grid(row=3, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
db_threshold_label.grid(row=3, column=1, sticky="W", padx=WIDGET_PADDING + 6, pady=WIDGET_PADDING)
db_threshold_slider.grid(row=3, column=1,sticky="E", padx=WIDGET_PADDING, pady=WIDGET_PADDING)

min_silence_button.grid(row=4, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
min_silence_label.grid(row=4, column=1, sticky="W", padx=WIDGET_PADDING + 6, pady=WIDGET_PADDING)
min_silence_slider.grid(row=4, column=1, sticky="E", padx=WIDGET_PADDING, pady=WIDGET_PADDING)

run_button.grid(row=5, column=0, padx=WIDGET_PADDING, pady=WIDGET_PADDING)
progress_bar.grid(row=5, column=1, padx=WIDGET_PADDING, pady=WIDGET_PADDING)

if TESTING: testing_fill_data()

window.mainloop()
