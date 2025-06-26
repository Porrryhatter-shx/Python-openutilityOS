import socket
import threading

# 服务器地址和端口
host = '127.0.0.1'
port = 65535

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print(f"服务器启动，监听 {host}:{port}")

# 客户端列表
clients = []

def handle_client(client_socket, client_address):
    print(f"新连接来自 {client_address}")
    clients.append(client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"来自 {client_address}: {message}")
                # 广播消息给所有客户端
                broadcast(message, client_socket)
            else:
                break
        except Exception as e:
            print(f"连接错误: {e}")
            break
    clients.remove(client_socket)
    client_socket.close()
    print(f"客户端 {client_address} 断开连接")

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"广播失败: {e}")
                clients.remove(client)
                client.close()

def main():
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
