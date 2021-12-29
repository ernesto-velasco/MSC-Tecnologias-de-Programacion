import logging
import random
import threading
import time


class Contador:
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.valor = start

    def incrementar(self):
        logging.debug('Esperando por lock')
        self.lock.acquire()

        try:
            logging.debug('Lock adquirido')
            self.valor = self.valor + 1
        finally:
            logging.debug('Lock liberado')
            self.lock.release()


def trabajador(c):
    for i in range(2):
        pausa = random.random()
        logging.debug('Durmiendo %0.02f', pausa)
        time.sleep(pausa)
        c.incrementar()
    logging.debug('Done')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

contador = Contador()
for i in range(2):
    t = threading.Thread(target=trabajador, args=(contador,))
    t.start()

logging.debug('Esperando por hilos trabajador ')
main_thread = threading.main_thread()

for t in threading.enumerate():
    if t is not main_thread:
        t.join()
logging.debug('Contador: %d', contador.valor)
