import socket
import threading
from datetime import datetime

server_config = ("localhost", 10000)
server = None

def get_current_datetime():
    return datetime.now().strftime("%m/%d/%Y %H:%M")

def wait_conecctions():
    print("[{}] Esperando peticiones de cliente..".format(
        get_current_datetime()
    ))
    while True:
        server.listen(1)
        client_socket, client_address = server.accept()
        new_thread = threading.Thread(target=client_thread, args=(client_address, client_socket))
        new_thread.start()

def client_thread(client_address, client_socket):
    print ("[{}] Nueva conexión: {}".format(
            get_current_datetime(), 
            client_address))
    message = ''
    while True:
            data = client_socket.recv(2048)
            message = data.decode()
            if message=='-1':
                break
            print ("[{}] {}: {}".format(
                get_current_datetime(),
                client_address,
                message))
            client_socket.send(bytes(message,'UTF-8'))
    print(threading.current_thread().name)
    print ("[{}] El cliente {} se desconecto...".format(
        get_current_datetime(),
        client_address))

def start_connection():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(server_config)
    print("[{}] Conexión establecida".format(
        get_current_datetime()))

def main():
    start_connection()
    wait_conecctions()

if __name__ == "__main__":
    main()