from concurrent.futures import ThreadPoolExecutor, as_completed
from recordMuseOutputRecording import start_recording
from playMediaSendMarkers import start_stream
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("input_filename", help="Media file to play")
parser.add_argument("output_filename", help="Output csv file to save the recordings to")
args = parser.parse_args()

executor = ThreadPoolExecutor(max_workers=2)

a = executor.submit(start_stream, args.input_filename)
b = executor.submit(start_recording, args.output_filename)

for job in as_completed([a, b]):
    print(job.result())
