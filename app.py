from flask import Flask, request, jsonify
import os

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")  # opcional

def is_valid_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    s = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (s * 10) % 11
    d1 = 0 if d1 == 10 else d1
    s = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (s * 10) % 11
    d2 = 0 if d2 == 10 else d2
    return d1 == int(cpf[9]) and d2 == int(cpf[10])

@app.get("/validate")
def validate():
    if API_KEY and request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "unauthorized"}), 401
    cpf = request.args.get("cpf", "")
    return jsonify({"cpf": cpf, "valid": is_valid_cpf(cpf)})

@app.get("/")
def health():
    return jsonify({"status": "ok"})
