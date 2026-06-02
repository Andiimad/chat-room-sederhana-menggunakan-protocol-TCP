import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

print(f"Server berjalan di port {PORT}")

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            # Tampilkan chat di terminal server
            print(message.decode())

            # Kirim ke semua client
            broadcast(message)

        except:
            break

    if client in clients:
        index = clients.index(client)

        clients.remove(client)
        client.close()

        name = names[index]
        names.remove(name)

        keluar = f"{name} keluar dari chat"
        print(keluar)

        broadcast(keluar.encode())

def receive():
    while True:
        client, address = server.accept()

        print(f"\nClient terhubung:")

        client.send("NAME".encode())

        name = client.recv(1024).decode()

        names.append(name)
        clients.append(client)

        masuk = f"{name} masuk ke chat"
        print(masuk)

        broadcast(masuk.encode())

        client.send("Terhubung ke server!".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()