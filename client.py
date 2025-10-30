# client.py
import socket, sys

def ask_float(prompt):
    while True:
        txt = input(prompt).strip().replace(",", ".")
        try:
            return float(txt)
        except ValueError:
            print("Valor inválido. Usa números y punto decimal (ej: 3.5).")

def ask_op():
    while True:
        op = input("Operación (+, -, *, /): ").strip()
        if op in {"+", "-", "*", "/"}:
            return op
        print("Operación inválida.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python client.py <IP_SERVIDOR> [PUERTO]")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) >= 3 else 5000

    a = ask_float("Primer número: ")
    b = ask_float("Segundo número: ")
    op = ask_op()

    msg = f"OP {op} {a} {b}\n"
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(msg.encode("utf-8"))
            data = s.recv(1024).decode("utf-8", errors="replace").strip()
            if data.startswith("OK "):
                print("Resultado:", data[3:].strip())
            elif data.startswith("ERR "):
                print("Error del servidor:", data[4:].strip())
            else:
                print("Respuesta desconocida:", data)
    except TimeoutError:
        print("Tiempo de conexión agotado.")
    except OSError as e:
        print("Error de conexión:", e)

if __name__ == "__main__":
    main()
