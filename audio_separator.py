from pydub import AudioSegment
from pydub import silence
import requests
import json
import sys


def export_sample(audio_segment, filename=None):
    if filename:
        audio_segment.export(
            f"{filename}.wav", format="wav", parameters=["-c:a", "pcm_s16le"]
        )
    else:
        audio_segment.export(
            "output.wav", format="wav", parameters=["-c:a", "pcm_s16le"]
        )


audio = AudioSegment.from_file(
    "audio_files/20200307_online_worship.m4a", format="m4a"
)

audio = audio.set_channels(1)
audio = audio.set_frame_rate(16000)


sample = audio[970000:2945000]

splitted = silence.split_on_silence(
    sample, min_silence_len=350, silence_thresh=-65
)

export_sample(sample, "total_sample")

headers = {
    "Content-Type": "application/octet-stream",
    "X-DSS-Service": "DICTATION",
    "Authorization": "KakaoAK c7bd2893f811dbbbce6fa118d4348e14",
}

text = ""
recog_list = []
for audio in splitted:
    export_sample(audio, "sample")
    data = open("sample.wav", "rb").read()
    response = requests.post(
        "https://kakaoi-newtone-openapi.kakao.com/v1/recognize",
        headers=headers,
        data=data,
    )

    result = response.text.split("\r\n")
    for line in result:
        try:
            parsed = json.loads(line)
            if parsed.get("type") == "finalResult":
                text += parsed.get("value") + " "
                recog_list.append(
                    [r.get("value") for r in parsed.get("nBest")]
                )
                print(parsed.get("value"))
        except json.decoder.JSONDecodeError:
            pass


def print_recog_list(l, file=sys.stdout):
    for chunk in l:
        for line in chunk:
            print(line, file=file)
        print(file=file)


with open("recog_list.txt", "w") as f:
    print_recog_list(recog_list, f)

with open("text.txt", "w") as f:
    print(text, file=f)
