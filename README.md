# Pylsl Synchronized

This repository aims to synchronize two independent scripts where one plays a media file to a stream and the other script records the output of Muse headset based on that stream. The end goal is to have a command line script which can start the media playback and the recording simultaneously.

## Usage
```
(venv)> python record_EGG.py -h
usage: record_EGG.py [-h] input_filename output_filename

positional arguments:
  input_filename   Media file to play
  output_filename  Output csv file to save the recordings to

optional arguments:
  -h, --help       show this help message and exit
```