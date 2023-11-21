import os

from pydub import AudioSegment


class Segment:
    def __init__(self):
        pass

    def segment(self, output_file_path, output_path, sec=10):
        audio = AudioSegment.from_file(output_file_path)
        audio_duration = len(audio)

        segments = []

        segment_duration = sec * 1000

        for start in range(0, audio_duration, segment_duration):
            end = start + segment_duration
            if end > audio_duration:
                end = audio_duration
            segment = audio[start:end]
            segments.append(segment)

        for i, segment in enumerate(segments):
            segment.export(os.path.join(output_path, f"{os.path.basename(output_file_path)}_{i + 1}"), format="wav")
