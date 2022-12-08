# pause_removal_tool


Documentation:
    Default Parameters:
        * M5 model in model.py has a default of n_input=1, n_output=35, stride=16, n_channel=32.
        * find silence in audio_functions.py has a default of pauseLength=0
        * retrieve silence has a default of stepSize=10000
        

Purpose:
    The purpose of the pause removal tool is to automate pause removal process for long audio clips.
    Given a wav file, it should identify pauses or silence in the audio.


How to Run:
    To remove silent pauses, run
        python tool.py [discrimination] [minlength] -s

        The descrimination argument is the minimum amplitude for audio that can be considered a silence, typically around 0.02

        The minlength argument is the minimum length in milliseconds of a segment below the descrimination amplitude that can be considered a silent pause

    To remove audible pauses ("umm"s and "uhh"s), run
        python tool.py [minprob] [minlength] -p

        The minprob argument is the minimum confidence of the model for something to be considered a part of an audible pause

        The minlength argument is the minimum length of a segment above the minprob argument that can be considered an audible pause


Current Functionality:
    The pause removal tool can currently remove silent pauses using the retrieve_silence function.

    Using the predictpauses function, it can use an untrained model to predict audible pauses (When I say untrained, I mean completely untrained, literally random)

    Outputs a list of timestamps and durations of pauses


Data Generation:
    data_generation.ipynb provides a set of functions that allow you to generate data to train the model on. Given a Wav file (I've downloaded and converted like 100 Khan Academy history videos for this purpose), it can insert pauses (prerecorded, just 6 different samples of me going "uhh" and "umm") into the video and return labels for the newly generated audio time series. This can be used to train the model.


Future Tasks:
    1. Train model.
    2. Implement a function which splits a .wav file into a bunch of smaller 3 seconds audio snippits so that the model can interpert it.
    3. Test dataset with model, and check if the model works well. If not, go back and edit model architecture.
    
BUGS:
    1. Model loader function probably doesn't work, given the amount of assumptions I (Livi) made about the inputs. Thus, an audio processing function must be made.