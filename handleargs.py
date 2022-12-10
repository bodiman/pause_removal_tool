import os
import audio_selection as asel

def handleargs(args, debug = False):

    if debug == False:
        assert os.path.isfile(args.Path), 'File path "' + args.Path + '" does not exist.'

    assert (args.pause or args.silence) and not (args.pause and args.silence), "You must specify either silence (-s) or pause (-p) selection"

    try:
        float(args.Discrimination)
    except:
        raise 'Argument "descrimination" must be a number'

    if args.pause:
        assert 0 <= float(args.Discrimination) <= 1, 'Argument "discrimination" must be between 0 and 1 for pause selection'

    try:
        float(args.Duration)
    except:
        raise 'Argument "duration" must be a number'

    if debug:
        if args.silence:
            asel.find_silence(args.Path, float(args.Discrimination), float(args.Duration), length = 10000, debug = True)

        elif args.pause:
            asel.find_pauses(args.Path, float(args.Discrimination), float(args.Duration))
        
        return

    if args.silence:
        print(asel.find_silence(args.Path, float(args.Discrimination), float(args.Duration)))

    elif args.pause:
        print(asel.find_pauses(args.Path, float(args.Discrimination), float(args.Duration)))