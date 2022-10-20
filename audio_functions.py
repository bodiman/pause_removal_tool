import numpy as np
import math
import model
import torch

"""

Find Silence takes in an audio clip and separates it by pauses into different segments

Find Silence takes the parameters of

  audio: a wav file loaded by librosa

  maxamplitude: a maximum amplitude for the algorithm to consider a part of the audio silent. About 0.02 is good.

  durations: the minimum time of silence (in milliseconds) that can be considered a pause

  sr: the sample rate of the wav file loaded by librosa


It returns an array of labels indicating wheather a pause is occuring at that time


Notes:

This function has a quadratic time complexity, so don't use it on clips any longer than 1 or 2 seconds.
The "retirevesilence" function is a workaround to this that scales linearly.

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



"""
Retrieve Silence gets around the issue of findsilence having a quadratic time complexity by calling it at an interval
and concatenating the results. It is called with the same parameters as the above function, plus "length", the length
of the audio clip passed into the "findsilence" function
"""


def retrievesilence(audio, maxamplitude, durations, sr, length = 10000):
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


"""
The predictpauses function simply estimates the probability that a given moment in the audio is a part of a pause
for the entire audio sample. The labelpauses function simply repurposes the functions above to find pauses that meet 
certain criteria. Currently, this is not really functional for two reasons. One, the model hasn't been trained. In fact,
the weights haven't even been saved. Two, predictpauses can miss up to 9999 samples depending on the size of the clip. 
For now, this model serves as a placeholder for the trained model in the future.
"""

def predictpauses(audio):
  fullpauses = []
  pl = 0

  for i in range(10000, len(audio), 10000):
    x = torch.tensor([[audio[(i-10000):i]]])
    y = model.predict(x)
    fullpauses = list(fullpauses) + list(y)

    if i + 10000 > len(audio):
      break
  
  return fullpauses

def labelpauses(predictions, minprob, minlength, sr):
  inversepredictions = -1 * predictions #the findsilence takes a maximum argument, not a minimum argument, so this is the workaround
  inverseminprob = -minprob

  return retrievesilence(inversepredictions, inverseminprob, minlength, sr)
    


"""
FindTimestamps takes the output of the "retrievesilence" or "findsilence" function and creates a list of the starting and ending
times of silences
"""

def findTimestamps(silencearray, sr):
  times = []

  if len(silencearray) == 0:
    return times

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


"""
formatTimestamps takes the output of the "findTimestamps" and formats it to be printed
"""

def formatTimestamps(timestamps):
  output = "Pauses: \n"
  for silence in timestamps:
    output = output + 'Duration: ' + str(silence[1]-silence[0]) + 's    Start Time: ' + str(silence[0]) + 's    End Time: ' + str(silence[1]) + 's\n'

  return output