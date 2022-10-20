import numpy as np
import math

"""

Segment Audio takes in an audio clip and separates it by pauses into different segments

Segment Audio takes the parameters of

  audio: a wav file loaded by librosa

  maxamplitude: a maximum amplitude for the algorithm to consider a part of the audio silent. About 0.02 is good.

  durations: the minimum time of silence (in milliseconds) that can be considered a pause

  sr: the sample rate of the wav file loaded by librosa


It returns an array of "audio segments" separated by pauses


Notes:

This function has a quadratic time complexity, so don't use it on clips any longer than 1 or 2 seconds.
The "retireve_segments" function is a workaround to this that scales linearly.

"""

def findsilence(audio, maxamplitude, durations, sr, pl = 0):
    duration = durations * sr / 1000

    silence = []
    pauselength = pl
    for ms in audio:
      if ms < maxamplitude:
        pauselength += 1
      else:
        if pauselength > duration:
          silence = silence + [1 for i in range(int(pauselength))] + [0]
        else:
          silence = silence + [0 for i in range(int((pauselength + 1)))]
        pauselength = 0
    
    silence = [float(i) for i in silence]
    return np.array(silence), pauselength


def retrievesilence(length, audio, maxamplitude, durations, sr):
  fullsilence = []
  pl = 0

  for i in range(0, len(audio), length):
    if i + length > len(audio):
      x = audio[i:]
    else:
      x = audio[i:(i+length)]
    
    silence, pl = findsilence(x, maxamplitude, durations, sr, pl)

    fullsilence = list(fullsilence) + list(silence)

  if pl > durations * sr / 1000:
    fullsilence = fullsilence + [1 for i in range(pl)]
  else:
    fullsilence = fullsilence + [0 for i in range(pl)]
  return fullsilence


def findTimestamps(silencearray, sr):
  times = []

  currentsilence = []

  if silencearray[0] == 1:
    currentsilence.append(0)

  for i in range(1, len(silencearray)):
    if silencearray[i] == 1 and silencearray[i-1] == 0:
      currentsilence.append(i / sr)

    elif silencearray[i] == 0 and silencearray[i-1] == 1:
      currentsilence.append(i / sr)
      times.append(currentsilence)
      currentsilence = []

  if len(currentsilence) == 1:
    currentsilence.append(len(silencearray) / sr)
    times.append(currentsilence)

  return times

def formatTimestamps(timestamps):
  output = "Pauses: \n"
  for silence in timestamps:
    output = output + 'Duration: ' + str(silence[1]-silence[0]) + 'ms    Start Time: ' + str(silence[0]) + 'ms    End Time: ' + str(silence[1]) + 'ms\n'

  return output