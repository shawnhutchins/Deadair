from tkinter import filedialog
import tkinter as tk
import ffmpeg
import os


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

def select_input():
    input_label.config(text=select_folder())

def select_output():
    output_label.config(text=select_folder())

#control variables
directory_path = "input/"
output = "output/"
target_file_extension = ".m4a"

#test using entry elements in place of the labels for sizing and manual editing
#UI elements
PADDING = 16

window = tk.Tk()
window.title("Dead Air Remove")
window.config(padx=PADDING, pady=PADDING)

#Input
input_select_button = tk.Button(text="Input", command=select_input)
input_select_button.grid(row=0, column=0)

input_label = tk.Label(text="")
input_label.grid(row=0, column=1)

#Output
output_select_button = tk.Button(text="Output", command=select_output)
output_select_button.grid(row=1, column=0)

output_label = tk.Label(text="")
output_label.grid(row=1, column=1)

window.mainloop()

#Trying to run with the console inputs
run = False
if run:
    try:
        for index, filename in enumerate(os.listdir(directory_path)):
            f_name, f_extension = os.path.splitext(filename)
            if f_extension == target_file_extension:
                remove_dead_air(os.path.join(directory_path, filename), os.path.join(output, filename))
    except OSError as e:
        print(f"OS Error")
