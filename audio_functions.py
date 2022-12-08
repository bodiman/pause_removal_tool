import numpy as np
import math
import model
import torch
import time

"""

Find Silence takes in an audio clip and separates it by pauses into different segments

Find Silence takes the parameters of

  audio: a wav file loaded by librosa

  maxAmplitude: a maximum amplitude for the algorithm to consider a part of the audio silent. About 0.02 is good.

  durations: the minimum time of silence (in milliseconds) that can be considered a pause

  sampleRate: the sample rate of the wav file loaded by librosa


It returns an array of labels indicating wheather a pause is occuring at that time


Notes:

This function has a quadratic time complexity, so don't use it on clips any longer than 1 or 2 seconds.
The "retirevesilence" function is a workaround to this that scales linearly.

"""

def findsilence(audio, maxAmplitude, durations, sampleRate, pauseLength = 0): #what is the difference between durations and duration?
    duration = durations * sampleRate / 1000

    silence = []

    for ms in audio: #what is ms in this context?
      if ms < maxAmplitude:
        pauseLength += 1 #what's the point of this?
      else:
        if pauseLength > duration:
          silence = silence + [1 for i in range(int(pauseLength))] + [0]
        else:
          silence = silence + [0 for i in range(int((pauseLength + 1)))]
        pauseLength = 0
    
    silence = [float(c) for c in silence] #what does float(i) do? #changed for i to c, for code clarity.
    return np.array(silence), pauseLength #what is pause length?

"""
Retrieve Silence gets around the issue of findsilence having a quadratic time complexity by calling it at an interval
and concatenating the results. It is called with the same parameters as the above function, plus "length", the length
of the audio clip passed into the "findsilence" function
"""


def retrievesilence(audio, maxAmplitude, durations, sampleRate, stepSize = 10000):
  #stepSize size of steps forward.
  # starttime = time.time() #timer
  fullsilence = []
  pauseLength = 0

  for i in range(0, len(audio), stepSize): #why do you need to input length if you grab length? Renameing for clarity
    if i + stepSize > len(audio): #if the given step is less than the length of the audio, then grab the given range.
      x = audio[i:] #this is slightly miss leading, because this is saying, grab everythign after this particular time stamp, rather than this range.
    else:
      x = audio[i:(i+stepSize)] #a little less missleading.
    
    silence, pauseLength = findsilence(x, maxAmplitude, durations, sampleRate, pauseLength) #what does sampleRate and pauseLength stand for?

    fullsilence = list(fullsilence) + list(silence) #what is going on here?

  if pauseLength > durations * sampleRate / 1000: #again what is pauseLength and sampleRate here?
    fullsilence = fullsilence + [1 for i in range(pauseLength)]
  else:
    fullsilence = fullsilence + [0 for i in range(pauseLength)]
  
  # print(f'Time to run retrievesilence: {time.time() - starttime}')
  return fullsilence #what is full silence?


"""
The predictpauses function simply estimates the probability that a given moment in the audio is a part of a pause
for the entire audio sample. The labelpauses function simply repurposes the functions above to find pauses that meet 
certain criteria. Currently, this is not really functional for two reasons. One, the model hasn't been trained. In fact,
the weights haven't even been saved. Two, predictpauses can miss up to 9999 samples depending on the size of the clip. 
For now, this model serves as a placeholder for the trained model in the future.
"""

def predictpauses(audio):
  fullpauses = []
  pauseLength = 0

  for i in range(10000, len(audio), 10000):
    x = torch.tensor(np.array([[audio[(i-10000):i]]]))
    y = model.predict(x)
    fullpauses = list(fullpauses) + list(y)

    if i + 10000 > len(audio):
      break
  
  return fullpauses

def labelpauses(predictions, minprob, minlength, sampleRate):
  inversepredictions = -1 * predictions #the findsilence takes a maximum argument, not a minimum argument, so this is the workaround
  inverseminprob = -minprob

  return retrievesilence(inversepredictions, inverseminprob, minlength, sampleRate) #what exactly is this retrieving, is this returning the silences that are applicable?
    


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