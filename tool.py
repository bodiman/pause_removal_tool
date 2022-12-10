# myls.py
# Import the argparse library
import argparse

import os
import sys

import audio_selection as asel

from handleargs import handleargs

# Create the parser
my_parser = argparse.ArgumentParser(
    prog='Pause Selection',
    usage='%(prog)s path descrimination duration [pausetype]',
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
    help='The maximum amplitude (typically around 0.02) to be considered silence or maximum probability to be identified as a pause'
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

handleargs(args)
    
#print('\n'.join(os.listdir(input_path)))