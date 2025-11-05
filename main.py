import tkinter as tk
import ffmpeg
import os

#make into command line app and accept input of directory paths
#make into tkinter app with folder selection

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

directory_path = "input/"
output = "output/"
target_file_extension = ".m4a"

window = tk.Tk()
window.title("Dead Air Remove")

#Trying to run with the console inputs
try:
    for index, filename in enumerate(os.listdir(directory_path)):
        f_name, f_extension = os.path.splitext(filename)
        if f_extension == target_file_extension:
            remove_dead_air(os.path.join(directory_path, filename), os.path.join(output, filename))
except OSError as e:
    print(f"OS Error")
