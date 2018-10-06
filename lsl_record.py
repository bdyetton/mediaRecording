#!/usr/bin/env python
# code by Alexandre Barachant
import numpy as np
import pandas as pd
import time
from pylsl import StreamInlet, resolve_byprop

def output_recording(res, timestamps, markers, ch_names, output_filename):
    res = np.concatenate(res, axis=0)
    timestamps = np.array(timestamps)

    res = np.c_[timestamps, res]
    data = pd.DataFrame(data=res, columns=['timestamps'] + ch_names)

    data['Marker'] = 0

    for marker in markers:
        ix = np.argmin(np.abs(marker[1] - timestamps))
        data.loc[ix, 'Marker'] = marker[0][0]

    data.to_csv(output_filename, float_format='%.3f', index=False)

    print('Done !')


def start_recording(output_filename):
    time.sleep(1)

    print("Looking for a Markers stream...")
    marker_streams = resolve_byprop('type', 'Markers', timeout=2)

    if marker_streams:
        inlet_marker = StreamInlet(marker_streams[0])
        print("Found Markers stream")
    else:
        inlet_marker = False
        print("Cant find Markers stream")

    print("Looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG', timeout=2)

    if len(streams) == 0:
        raise (RuntimeError, "Cant find EEG stream")

    print("Start aquiring data")
    inlets = list()
    for i in range(len(streams)):
        inlets[i] = StreamInlet(streams[i], max_chunklen=12)

    inlet = inlets[0]
    info = inlet.info()
    description = info.desc()

    print(description)
    print(info)

    nchan = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, nchan):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    results = [[] for _ in range(len(streams))]
    timestamps = [[] for _ in range(len(streams))]
    markers = []
    t_init = time.time()
    print('Start recording at time t=%.3f' % t_init)
    while True:
        for i in range(len(streams)):
            data, timestamp = inlets[i].pull_chunk(timeout=1.0, max_samples=12)

            results[i].append(data)
            timestamps[i].extend(timestamp)

        if inlet_marker:
            marker, timestamp = inlet_marker.pull_sample(timeout=0.0)

            if marker == [2]:
                markers.append([marker, timestamp])
                print("Marker 2 append")
                break
            elif timestamp:
                markers.append([marker, timestamp])
                print("Marker 1 append")

    for i in range(len(streams)):
        output_recording(results[i], timestamps[i], markers, ch_names, output_filename.replace('.', f'_{i}.'))