from threading import Thread
import random
import time

valor = 0
cuadrado = 0
ban = True

class MiHilo1(Thread):
    def __init__(self):
        '''Constructor'''
        Thread.__init__(self)

    def run(self):
        global ban
        print("Escribe cualquier texto...")
        texto = input()
        ban = False
        print(f"Mienras escribias \"{texto}\" se calculó el cuadrado de {valor} resultando en {cuadrado}")

class MiHilo2(Thread):
    def __init__(self):
        '''Constructor'''
        Thread.__init__(self)

    def run(self):
        while ban:
            global valor
            global cuadrado
            valor = valor + 1
            cuadrado = valor * valor
            time.sleep(1)

def main():
    '''Principal'''
    hilo1 = MiHilo1()
    hilo1.setName("Hilo 1")
    hilo2 = MiHilo2()
    hilo2.setName("Hilo 2")

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

if __name__ == '__main__':
    main()