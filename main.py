from tkinter import filedialog
import customtkinter as ctk
import ffmpeg
import os

#convert to customtkinter
#add tool tips
#add indication of success or failure
#add indication of progress

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

#Opens the folder select dialog and sets the input_label to the path value
def select_folder():
    folder_name = filedialog.askdirectory(
        parent=window,
        title="Browse Folder"
    )
    return folder_name

def select_file():
    file_name = filedialog.askopenfilename(
        parent=window,
        title="Select one of the files to be processed"
    )
    return file_name

def select_input():
    input_var.set(select_folder())

def select_output():
    output_var.set(select_folder())

def select_file_type():
    selected_file = select_file()
    _, file_extension = os.path.splitext(selected_file)
    file_type_var.set(file_extension)

def run_script():
    try:
        for index, filename in enumerate(os.listdir(input_var.get())):
            _, file_extension = os.path.splitext(filename)
            if file_extension == file_type_var.get():
                remove_dead_air(os.path.join(input_var.get(), filename), os.path.join(output_var.get(), filename))
    except OSError as e:
        print(f"OS Error")

#UI elements
PADDING = 16
BTN_WIDTH = 60

#Main window
window = ctk.CTk()
window.title("Dead Air Remove")
window.geometry("500x146")
window.config(padx=PADDING, pady=PADDING)

#Entry variables
input_var = ctk.StringVar()
output_var = ctk.StringVar()
file_type_var = ctk.StringVar()

#Input, select the directory that contains the files you wish to process
input_select_button = ctk.CTkButton(window, text="Input", command=select_input, width=BTN_WIDTH)
input_entry = ctk.CTkEntry(window, textvariable=input_var, width=360, state="readonly")

#Output, select a directory for your processed files to be placed in
output_select_button = ctk.CTkButton(window, text="Output", command=select_output, width=BTN_WIDTH)
output_entry = ctk.CTkEntry(window, textvariable=output_var, width=360, state="readonly")

#Filetype, select a file to use its file extension
file_type_button = ctk.CTkButton(window, text="Filetype", command=select_file_type, width=BTN_WIDTH)
file_type_entry = ctk.CTkEntry(window, textvariable=file_type_var, width=60, state="readonly", )

#Run button
run_button = ctk.CTkButton(window, text="Run", command=run_script, width= BTN_WIDTH)

#Grid
input_select_button.grid(row=0, column=0)
input_entry.grid(row=0, column=1)
output_select_button.grid(row=1, column=0)
output_entry.grid(row=1, column=1)
file_type_button.grid(row=2, column=0)
file_type_entry.grid(row=2, column=1, sticky="W")
run_button.grid(row=3, column=0)

window.mainloop()
