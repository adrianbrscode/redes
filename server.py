# server.py
import socket, threading

HOST = "0.0.0.0"
PORT = 5000
BACKLOG = 100
TIMEOUT_S = 30

ALLOWED_OPS = {"+", "-", "*", "/"}

def compute(op, a, b):
    if op not in ALLOWED_OPS:
        return None, ("BAD_OP", f"Operador no permitido: {op}")
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return None, ("BAD_NUM", "Operandos deben ser números (usa punto decimal).")
    if op == "/" and b == 0.0:
        return None, ("DIV_ZERO", "División por cero.")
    if op == "+":  res = a + b
    elif op == "-": res = a - b
    elif op == "*": res = a * b
    else:           res = a / b
    # Limita decimales para legibilidad
    return (f"{res:.10g}"), None

def process_line(msg: str) -> str:
    if msg == "PING":
        return "PONG"
    parts = msg.split()
    if len(parts) == 4 and parts[0] == "OP":
        _, op, op1, op2 = parts
        result, err = compute(op, op1, op2)
        if err:
            code, text = err
            return f"ERR {code} {text}"
        return f"OK {result}"
    return "ERR BAD_FORMAT Usa: OP <+|-|*|/> <num1> <num2> o PING"

def handle_client(conn, addr):
    conn.settimeout(TIMEOUT_S)
    with conn:
        try:
            buf = b""
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                buf += chunk
                while b"\n" in buf:
                    raw, buf = buf.split(b"\n", 1)
                    msg = raw.decode("utf-8", errors="replace").strip()
                    if not msg:
                        continue
                    print(f"[RX {addr}] {msg}")
                    reply = process_line(msg)
                    print(f"[TX {addr}] {reply}")
                    conn.sendall((reply + "\n").encode("utf-8"))
        except socket.timeout:
            print(f"[TIMEOUT] {addr}")
        except Exception as e:
            print(f"[ERROR {addr}] {e}")

def main():
    print(f"[BOOT] Calculadora TCP en {HOST}:{PORT} (F2+)")
    with socket.create_server((HOST, PORT), backlog=BACKLOG, reuse_port=True) as srv:
        while True:
            conn, addr = srv.accept()
            print(f"[ACCEPT] {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
