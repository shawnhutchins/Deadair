import ffmpeg
import os

#add filtering of file types.
#make into command line app and accept input of directory paths
#make into tkinter app with folder selection

def remove_dead_air(input_mp3, output_mp3, silence_threshold=-30, min_silence_duration=0.5):
    """
    Removes dead air from an MP3 file using ffmpeg-python.

    Args:
        input_mp3 (str): Path to the input MP3 file.
        output_mp3 (str): Path for the output MP3 file with silence removed.
        silence_threshold (int): The volume level in dB below which audio is considered silence.
                                 Default is -30 dB.
        min_silence_duration (float): The minimum duration of silence (in seconds) to be removed.
                                      Default is 0.5 seconds.
    """
    try:
        (
            ffmpeg
            .input(input_mp3)
            .filter('silenceremove',
                    start_periods='0',  # Remove silence at the beginning
                    stop_periods='-1',  # Remove silence throughout the file
                    stop_duration=str(min_silence_duration),
                    detection='peak',
                    stop_threshold=str(silence_threshold) + 'dB')
            .output(output_mp3)
            .run(overwrite_output=True)
        )
        print(f"Dead air removed successfully. Output saved to: {output_mp3}")
    except ffmpeg.Error as e:
        print(f"Error removing dead air: {e.stderr.decode()}")

# Edit here to change input and output paths
directory_path = "S:/audio_recordings/"
output = "S:/silence_removed/"

try:
    for index, filename in enumerate(os.listdir(directory_path)):
        remove_dead_air(os.path.join(directory_path, filename), os.path.join(output, filename))
except OSError as e:
    print(f"OS Error")
