# pause_removal_tool

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
    1. Generate data and train the model.
    2. Increase diversity in pauses, there are currently only 6 different samples, so the model will definitely overfit
        a. get people to read a speach or something, then provide a few pause samples and insert.
    3. Rewrite the predictpauses function. At the moment it's pretty much the same function that identifies silent pauses, which most likely isn't the most effective solution
    4. Parallelize the retrieve_silence and predictpauses functions