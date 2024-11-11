import socket
from env import *

def enviar_operacao(operacao):
    # Configura o endereço e a porta do proxy reverso
    proxy_host = host

    # Cria o socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((proxy_host, porta_proxy))
        
        # Envia a operação para o proxy reverso
        s.sendall(operacao.encode())
        
        # Recebe o resultado do cálculo
        resultado = s.recv(1024).decode()
        print(f"Resultado da operação: {resultado}")

if __name__ == "__main__":
    operacao = input("Digite a operação matemática (ex: 5+3): ")
    enviar_operacao(operacao)
