import time
from pylsl import StreamInfo, StreamOutlet
import subprocess


def start_stream(filename):
    info = StreamInfo('Muse', 'Markers', 1, 0.0, 'int32', 'marker')
    outlet = StreamOutlet(info)

    outlet.push_sample([-1], time.time())
    print("-1 Marker sent")

    time.sleep(4)

    outlet.push_sample([1], time.time())
    subprocess.call(['mpv', "../videos/" + filename])
    outlet.push_sample([2], time.time())

    time.sleep(6)

