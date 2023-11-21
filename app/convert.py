from moviepy.audio.io.AudioFileClip import AudioFileClip
import os


class Conversion:
    def __init__(self):
        pass

    def convert_to_audio(self, input_path, output_path, file_name, audio_format='wav'):
        print(fr"{output_path}.{audio_format}")
        audio_clip = AudioFileClip(input_path)
        audio_clip.write_audiofile(fr"{output_path}\{file_name}.{audio_format}")

    def get_output_file_path(self, output_path, file_name, audio_format='wav'):
        return os.path.join(output_path, f"{file_name}.{audio_format}")
