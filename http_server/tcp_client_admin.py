import socket
import json

HOST = "host.docker.internal"
PORT = 65432

def send_tcp_request(data: dict):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(data).encode())
            response = s.recv(4096)
            return json.loads(response.decode())
    except Exception as e:
        return {"status": "error", "message": str(e)}
