from pydub import AudioSegment
from pydub import silence


def export_sample(audio_segment, filename=None):
    if filename:
        audio_segment.export(f"{filename}.wav", format="wav")
    else:
        audio_segment.export("output.wav", format="wav")


audio = AudioSegment.from_file(
    "audio_files/20200307_online_worship.m4a", format="m4a"
)
audio.set_channels(1)
audio.set_frame_rate(16000)


sample = audio[1279000:1299000]

splitted = silence.split_on_silence(
    sample, min_silence_len=350, silence_thresh=-80
)

len_sum = 0
export_audio = AudioSegment.empty()
for a in splitted:
    export_audio = export_audio + a + AudioSegment.silent(duration=1000)
    len_sum += a.duration_seconds

export_sample(export_audio)
