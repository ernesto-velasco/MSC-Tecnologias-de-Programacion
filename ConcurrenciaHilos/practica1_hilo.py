from threading import Thread
import random
import time

class MiHilo(Thread):
    def __init__(self, value):
        '''Constructor'''
        Thread.__init__(self)
        self.value = value

    def run(self):
        sleep = random.randint(1,5)
        print("%s durmiendo por %d segundos..." % (self.getName(), sleep))
        time.sleep(sleep)

def main():
    '''Principal'''
    hilo1 = MiHilo(2)
    hilo1.setName("Hilo 1")
    hilo2 = MiHilo(4)
    hilo2.setName("Hilo 2")

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()


if __name__ == '__main__':
    main()