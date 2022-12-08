# myls.py
# Import the argparse library
import argparse

import os
import sys

import audio_selection as asel

# Create the parser
my_parser = argparse.ArgumentParser(
    prog='Pause Selection',
    usage='%(prog)s path duration descrimination [pausetype]',
    description='List the timestamps of pauses in a wav file'
)

# Add the arguments

my_parser.add_argument('Path',
    metavar='path',
    type=str,
    help='Path of wav file'
)

my_parser.add_argument('Discrimination',
    metavar='descrimination',
    type=str,
    help='The maximum amplitude to be considered silence or maximum probability to be identified as a pause'
)

my_parser.add_argument('Duration',
    metavar='duration',
    type=str,
    help='The duration in milliseconds to be considered'
)

my_parser.add_argument(
    '-s',
    '--silence', 
    help='silent pause, descriminate below a certain amplitude in wav file',
    action="store_true"
)

my_parser.add_argument(
    '-p',
    '--pause', 
    help='audible pause, descriminate above confidence of pause prediction',
    action="store_true"
)

# Execute the parse_args() method
args = my_parser.parse_args()

assert os.path.isfile(args.Path), 'File path "' + args.Path + '" does not exist.'

assert (args.pause or args.silence) and not (args.pause and args.silence), "You must specify either silence (-s) or pause (-p) selection"

try:
    float(args.Discrimination)
except:
    raise 'Argument "discrimination" must be a number'

if args.pause:
    assert 0 <= float(args.Discrimination) <= 1, 'Argument "discrimination" must be between 0 and 1 for pause selection'

try:
    float(args.Duration)
except:
    raise 'Argument "duration" must be a number'


if args.silence:
    print(asel.find_silence(args.Path, float(args.Discrimination), float(args.Duration)))

elif args.pause:
     print(asel.find_pauses(args.Path, float(args.Discrimination), float(args.Duration)))
    
#print('\n'.join(os.listdir(input_path)))