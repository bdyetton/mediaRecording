from multiprocessing import Process
from recordMuseOutputRecording import start_recording
from playMediaSendMarkers import start_stream
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename", help="Media file to play")
    parser.add_argument("output_filename", help="Output csv file to save the recordings too")
    args = parser.parse_args()

    Process(target=start_stream, args=(args.input_filename,)).start()
    Process(target=start_recording, args=(args.output_filename,)).start()
