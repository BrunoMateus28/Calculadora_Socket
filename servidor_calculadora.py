import socket
import psutil
import re
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from env import *
import uuid

def calcular_operacao(operacao, cliente_id):
    try:
        operacao = operacao.replace(" ", "")
        match = re.match(r"(\d+\.?\d*)([+\-*/])(\d+\.?\d*)", operacao)
        if not match:
            return f"Cliente {cliente_id}: Erro: Formato inválido."

        num1, operador, num2 = match.groups()
        num1, num2 = float(num1), float(num2)

        if operador == "+":
            return str(num1 + num2)
        elif operador == "-":
            return str(num1 - num2)
        elif operador == "*":
            return str(num1 * num2)
        elif operador == "/":
            return "Erro: Divisão por zero." if num2 == 0 else str(num1 / num2)
        else:
            return "Erro: Operador inválido."
    except Exception as e:
        return f"Cliente {cliente_id}: Erro: {e}"

def atender_cliente(cliente_socket):
    cliente_id = str(uuid.uuid4())
    try:
        operacao = cliente_socket.recv(1024).decode()
        if not operacao:
            cliente_socket.sendall(f"Cliente {cliente_id}: Erro: Operação vazia recebida.".encode())
            return
        print(f"Cliente {cliente_id}: Realizando operação: {operacao}")
        resultado = calcular_operacao(operacao, cliente_id)
        print(f"Cliente {cliente_id}: Resultado: {resultado}")
        cliente_socket.sendall(resultado.encode())
    finally:
        print(f"Cliente {cliente_id}: Conexão encerrada.")
        cliente_socket.close()

def reportar_carga():
    try:
        return str(psutil.cpu_percent(interval=0.1))
    except Exception:
        return "Erro ao acessar CPU."

def servidor_status(host, porta_status):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, porta_status))
            s.listen()
            print(f"Servidor de Carga em {host}:{porta_status} aguardando requisições...")
            while True:
                status_socket, _ = s.accept()
                carga = reportar_carga()
                status_socket.sendall(carga.encode())
                status_socket.close()
    except Exception as e:
        print(f"Erro no servidor de carga: {e}")

def servidor_servico(host, porta_servico):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, porta_servico))
            s.listen()
            print(f"Servidor de Serviço em {host}:{porta_servico} aguardando requisições...")
            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    cliente_socket, _ = s.accept()
                    executor.submit(atender_cliente, cliente_socket)
    except Exception as e:
        print(f"Erro no servidor de cálculos: {e}")

def iniciar_servidor(host, porta_status, porta_servico):
    status_thread = threading.Thread(target=servidor_status, args=(host, porta_status))
    status_thread.start()
    servico_thread = threading.Thread(target=servidor_servico, args=(host, porta_servico))
    servico_thread.start()

if __name__ == "__main__":
    for servidor in servidores:
        iniciar_servidor(servidor['host'], servidor['porta_status'], servidor['porta_servico'])
    while True:
        time.sleep(1)
