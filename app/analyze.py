from pydub import AudioSegment
from pydub.silence import split_on_silence


class Analysis:
    def __init__(self, min_silence_len_in_msec, silence_thresh_in_dB):
        self.min_silence_len = min_silence_len_in_msec
        self.silence_thresh = silence_thresh_in_dB

    def analyse_audio(self, output_file_path):
        audio = AudioSegment.from_file(output_file_path)

        chunks = split_on_silence(audio, min_silence_len=self.min_silence_len, silence_thresh=self.silence_thresh,
                                  keep_silence=False, seek_step=1)

        output = sum(chunks)
        output.export(output_file_path, format="wav")


