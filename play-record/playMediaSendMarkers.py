import time
from pylsl import StreamInfo, StreamOutlet
import subprocess
try:
    import biopac
    imported_biopac = True
except ImportError:
    print('Biopac will not work: No parallel port or pyparallel not installed')
    imported_biopac = False
    


def start_stream(filename, trigger_biopac=False):
    
    if trigger_biopac and not imported_biopac:
        raise('ValueError','Biopac cannot be triggered becasue import failed')
        
    info = StreamInfo('Muse', 'Markers', 1, 0.0, 'int32', 'marker')
    
    outlet = StreamOutlet(info)

    outlet.push_sample([-1], time.time())
    print("-1 Marker sent")

    time.sleep(4)

    outlet.push_sample([1], time.time()) #lsl trigger for on
    if trigger_biopac:
        biopac.start()
        
    subprocess.call(['mpv', "../videos/" + filename]) #what kind of lag does this introduce? Does the video start immediatly? 
    
    outlet.push_sample([2], time.time()) #lsl trigger for off
    if trigger_biopac:
        biopac.stop()

    time.sleep(6)

