# client_ping.py
import socket, sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else None
PORT = 5000

if not SERVER_IP:
    print("Uso: python client_ping.py <IP_SERVIDOR>")
    raise SystemExit(1)

with socket.create_connection((SERVER_IP, PORT), timeout=5) as s:
    s.sendall(b"PING\n")
    data = s.recv(1024).decode("utf-8", errors="replace").strip()
    print("[RESP]", data)
