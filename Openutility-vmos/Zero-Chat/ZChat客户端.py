import socket
import threading

# 服务器地址和端口
host = '127.0.0.1'
port = 65535

# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("已连接到服务器")

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"接收错误: {e}")
            client_socket.close()
            break

def send():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def main():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()

if __name__ == "__main__":
    main()
