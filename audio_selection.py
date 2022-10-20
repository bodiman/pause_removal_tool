import audio_functions as af
import librosa
import torch


def find_silence(filepath, maxamplitude, durations, length = 10000):
  audio, sr = librosa.load(filepath)
  labels = af.retrievesilence(audio, maxamplitude, durations, sr, length)
  timestamps = af.findTimestamps(labels, sr)
  return af.formatTimestamps(timestamps)


def find_pauses(filepath, minprob, durations):
    audio, sr = librosa.load(filepath)
    predictions = af.predictpauses(audio)
    predictions = torch.flatten(torch.cat(predictions))
    labels = af.labelpauses(predictions, minprob, durations, sr)
    timestamps = af.findTimestamps(labels, sr)
    return af.formatTimestamps(timestamps)