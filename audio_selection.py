import audio_functions as af
import librosa
import soundfile as sf
import torch
from random import randint

import numpy as np


"""
FindTimestamps takes the output of the "retrievesilence" or "findsilence" function and creates a list of the starting and ending
times of silences
"""

def findTimestamps(silencearray, sampleRate):
  times = []

  if len(silencearray) == 0:
    return times

  currentsilence = []

  if silencearray[0] == 1:
    currentsilence.append(0)

  for i in range(1, len(silencearray)):
    if silencearray[i] == 1 and silencearray[i-1] == 0:
      currentsilence.append(i / sampleRate)

    elif silencearray[i] == 0 and silencearray[i-1] == 1:
      currentsilence.append(i / sampleRate)
      times.append(currentsilence)
      currentsilence = []

  if len(currentsilence) == 1:
    currentsilence.append(len(silencearray) / sampleRate)
    times.append(currentsilence)

  return times


"""
formatTimestamps takes the output of the "findTimestamps" and formats it to be printed
"""

def formatTimestamps(timestamps):
  output = "Pauses: \n"
  for silence in timestamps:
    output = output + 'Duration: ' + str(silence[1]-silence[0]) + 's    Start Time: ' + str(silence[0]) + 's    End Time: ' + str(silence[1]) + 's\n'

  return output

"""
export_silence_wav takes in the original audio and the timestamps of the silence and exports a wav file with only the silence.
This file will help the user quickly verify that this tool has removed nothing important.
"""

def export_silence_wav(audio, sr, timestamps):
  newaudio = []
  for silence in timestamps:
    newaudio += list(audio[round(silence[0]*sr):round(silence[1]*sr)])

  sf.write("exported_silence.wav", np.array(newaudio), sr)
  return True

def export_newaudio_wav(audio, sr, timestamps, ):
  newaudio = []
  cutoff = 0
  for silence in timestamps:
    newaudio += list(audio[cutoff:round(silence[0]*sr)])
    cutoff = round(silence[1]*sr)

  sf.write("exported_newaudio.wav", np.array(newaudio), sr)
  return True


def find_silence(filepath, maxamplitude, durations, length = 10000, debug = False):
  if debug == False:
    audio, sr = librosa.load(filepath)
  else:
    audio = filepath #if debug is true, a list of frequencies is passed into the function rather than a file path
    sr = randint(1, 24000)
  labels = af.retrievesilence(audio, maxamplitude, durations, sr, length)
  timestamps = af.findTimestamps(labels, sr)
  export_silence_wav(audio, sr, timestamps)
  export_newaudio_wav(audio, sr, timestamps)
  return formatTimestamps(timestamps)


def find_pauses(filepath, minprob, durations, debug = False):
    if debug == False:
      audio, sr = librosa.load(filepath)
    else:
      audio = filepath
      sr = randint(1, 24000)
    predictions = af.predictpauses(audio)
    predictions = torch.flatten(torch.cat(predictions))
    labels = af.labelpauses(predictions, minprob, durations, sr)
    timestamps = af.findTimestamps(labels, sr)
    export_silence_wav(audio, sr, timestamps)
    export_newaudio_wav(audio, sr, timestamps)
    return formatTimestamps(timestamps)