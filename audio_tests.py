from numpy import random
from random import randint

from audio_functions import *


#Black Box/Unit Tests

"""Ensure that the length of the inputted audio sequence is equal to the lenght of the outputted audio sequence plus the outputted pause length"""
def findsilence_test(audio=random.normal(size=(randint(1, 200))), maxAmplitude=random.normal(), durations=random.normal(), sampleRate=random.normal(), pauseLength = 0):
    test = findsilence(audio, maxAmplitude, durations, sampleRate, pauseLength)
    assert len(test[0]) + test[1] == len(audio), f"Mismatched inputted and outputted lengths in findsilence_test. Inputting array of length {len(audio)} and getting outputted array of length {len(test[0])} and pauselength {test[1]}"
    return True

def retrievesilence_test(audio=random.normal(size=(randint(1, 200))), maxAmplitude=random.normal(), durations=random.normal(), sampleRate=random.normal(), stepSize = 10000):
    test = retrievesilence(audio, maxAmplitude, durations, sampleRate, stepSize)
    assert len(test) == len(audio), f"Mismatched inputted and outputted lengths in retrievesilence_test. Inputting array of length {len(audio)} and getting outputted array of length {len(test)}"
    return True

def predictpauses_test(audio=random.normal(size=(randint(1, 20000)))):
    test = predictpauses(audio)
    assert len(audio) == len(test), f"Mismatched inputted and outputted lengths in predictpauses_test. Inputting array of length {len(audio)} and getting outputted array of length {len(test)}"

#White Box/End to End Tests

#Adverserial Tests

for _ in range(1000):
    findsilence_test()
    retrievesilence_test()
    predictpauses_test(audio=random.normal(size=(randint(1, 19000))))