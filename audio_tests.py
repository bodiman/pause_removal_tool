from numpy import random
from random import randint

from audio_functions import *

from handleargs import handleargs


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
class TestObject():
    def __init__(self, Path=random.normal(size=(randint(1, 200))), Discrimination=random.normal(), Duration=randint(1, 1000), silence=True, pause=False):
        self.Path = Path
        self.Discrimination = Discrimination
        self.Duration = Duration
        self.silence = silence
        self.pause = pause

def fulltest(args = TestObject()):
    handleargs(args, debug=True) #has built in tests

#Adverserial Tests

#running all tests

# for _ in range(1000):
#     findsilence_test()
#     retrievesilence_test()
#     predictpauses_test(audio=random.normal(size=(randint(1, 20000))))
#     fulltest()