import threading

def trabajador(num):
    """Funcion del hilo"""
    print("Trabajador: %s" %num)

hilos = []
for i in range(5):
    h = threading.Thread(target=trabajador, args=(i,))
    hilos.append(h)
    h.start()

