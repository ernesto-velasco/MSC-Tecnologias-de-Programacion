import logging
import threading
import time


def espera_por_evento(e):
    """Wait for the event to be set before doing anything"""
    logging.debug('espera_por_evento iniciando')
    estableciendo_evento = e.wait()
    logging.debug('estableciendo evento: %s', estableciendo_evento)


def espera_por_evento_timeout(e, t):
    """Wait t seconds and then timeout"""
    while not e.is_set():
        logging.debug('espera_por_evento_timeout iniciando')
        estableciendo_evento = e.wait(t)
        logging.debug('estableciendo evento: %s', estableciendo_evento)
        if estableciendo_evento:
            logging.debug('procesando evento')
        else:
            logging.debug('haciendo otro trabajo')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

e = threading.Event()

t1 = threading.Thread(name='block',target=espera_por_evento,args=(e,),)
t1.start()

t2 = threading.Thread(name='nonblock',target=espera_por_evento_timeout,args=(e, 2),)
t2.start()

logging.debug('Eperando antes de llamar el Event.set()')
time.sleep(0.3)
e.set()
logging.debug('El evento es establecido')
