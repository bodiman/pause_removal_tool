import audio_functions as af
import librosa


def find_silence(filepath, maxamplitude, durations, length = 10000):
  audio, sr = librosa.load(filepath)
  labels = af.retrievesilence(length, audio, maxamplitude, durations, sr)
  timestamps = af.findTimestamps(labels, sr)
  return af.formatTimestamps(timestamps)


def find_pauses(filepath, minprob, durations):
    return