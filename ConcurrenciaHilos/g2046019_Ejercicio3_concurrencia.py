import threading
import time
import logging

def demonio():
    logging.debug('Starting')
    time.sleep(0.2)
    logging.debug('Exiting')


def no_demonio():
    logging.debug('Starting')
    logging.debug('Exiting')



logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

d = threading.Thread(name='daemon', target=demonio)
d.daemon = True
h = threading.Thread(name='non-daemon', target=no_demonio)

d.start()
h.start()

d.join(0.1)
print('d.isAlive()', d.is_alive())
h.join()
