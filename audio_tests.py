import audio_functions as audio
import numpy as np
import librosa

from pydub import AudioSegment

"""

The segment audio test verifies that the outputted segments contain the same information as the inputed audio

"""

def segment_audio_test(audio, maxamplitude, durations, sr):
  video_segments = audio.segment_audio(audio, maxamplitude, durations, sr)
  test_list = []
  for segment in video_segments:
    test_list += list(segment)
  
  assert (np.array(test_list) == audio).all()
  return True


def retrieve_segments_test(length, starttime, stoptime, audiofile):
    t1 = starttime
    t2 = stoptime

    samplelecture = AudioSegment.from_wav(audiofile)
    testclip = samplelecture[1000*t1:1000*t2]
    testclip.export("sample.wav", format="wav")

    audio_sample, sr_sample = librosa.load("sample.wav") #audio sample for testing, actual sound that should be generated

    segmented_audio = audio.retrieve_segments(length, starttime, stoptime, audiofile)
    fullaudio = audio.insert_pauses(segmented_audio, True)

    assert (fullaudio == audio_sample).all(), "The values are not equal"