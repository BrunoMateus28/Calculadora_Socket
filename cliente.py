import socket
from env import *
import re

def enviar_operacao(operacao):
    proxy_host = host
    try:
        # Cria o socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((proxy_host, porta_proxy))
            s.sendall(operacao.encode())  # Envia a operação para o proxy reverso
            
            resultado = s.recv(1024).decode()  # Recebe o resultado
            print(f"Resultado da operação: {resultado}")
    except (ConnectionRefusedError, socket.error):
        print("Erro: Não foi possível conectar ao proxy reverso.")

if __name__ == "__main__":
    while True:
        operacao = input("Digite a operação matemática (ex: 5+3): ")
        if not re.match(r"^\s*\d+(\.\d+)?\s*[-+*/]\s*\d+(\.\d+)?\s*$", operacao):
            print("Erro: Operação inválida. Use o formato 'num1 operador num2' (ex: 5+3).")
            continue
        enviar_operacao(operacao)
