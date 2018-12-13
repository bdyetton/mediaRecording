import parallel
p = parallel.Parallel()

def start():
    biopac_on_trigger = 128
    p.setData(value=biopac_on_trigger)
    print('Biopac Trigger On')
    
def stop():
    biopac_off_trigger = 0
    p.setData(value=biopac_off_trigger)
    print('Biopac Trigger Off')
