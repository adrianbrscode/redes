
# Calculadora TCP — Explicación del funcionamiento

## Qué es
Una calculadora remota **cliente/servidor** sobre **TCP**. El **cliente** envía una operación en texto; el **servidor** la calcula y responde con una línea de texto.

---

## Cómo funciona (resumen claro)

1. **Servidor** (Ubuntu) queda escuchando en `HOST:PORT` (por defecto `0.0.0.0:5000`).
2. **Cliente** (Windows) pide al usuario: número A, número B y operador (`+ - * /`).
3. El cliente arma **una línea** y la envía:

4. El servidor recibe la línea, la interpreta y:
- Valida formato (`OP ...` con 4 partes).
- Valida operador permitido.
- Convierte A y B a número (usa **punto** como decimal).
- Bloquea división por cero.
- Calcula y formatea el resultado.
5. El servidor responde **una línea**:
- Éxito: `OK <resultado>\n`
- Error: `ERR <código> <mensaje>\n`
6. El cliente muestra la respuesta y **cierra** la conexión.

> También existe un chequeo rápido de vida (client_ping.py):
> - Cliente: `PING\n` → Servidor: `PONG\n`.

---

## Protocolo (texto línea a línea)

- **Petición de operación**
- **Respuestas**
- `OK <resultado>\n`
- `ERR BAD_OP Operador no permitido: x\n`
- `ERR BAD_NUM Operandos deben ser números (usa punto decimal).\n`
- `ERR DIV_ZERO División por cero.\n`
- `ERR BAD_FORMAT Usa: OP <+|-|*|/> <num1> <num2> o PING\n`

**Ejemplos**
- OP + 3 4 → OK 7
- OP * 2 2.5 → OK 5
- OP / 10 4 → OK 2.5
- OP / 3 0 → ERR DIV_ZERO División por cero.
- OP x 1 2 → ERR BAD_OP Operador no permitido: x
- OP + a 2 → ERR BAD_NUM Operandos deben ser números (usa punto decimal).