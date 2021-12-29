import socket
from datetime import datetime

server_config = ("localhost", 10000)
buffer_size = 1024
cliente = None

def get_current_datetime():
    return datetime.now().strftime("%m/%d %H:%M")

def start_connection():
    global cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(server_config)
    print("[{}] Conexión establecida".format(
        get_current_datetime()))

def close_connection():
    global cliente
    cliente.close()

def wait_message():
    while True:
        print("[{}] Escribe tu mensaje (-1 para salir)".format(
            get_current_datetime()))
        out_data = input()
        cliente.sendall(bytes(out_data,'UTF-8'))
        if out_data=='-1':
            break

def main():
    start_connection()
    wait_message()
    close_connection()

if __name__ == '__main__':
    main()