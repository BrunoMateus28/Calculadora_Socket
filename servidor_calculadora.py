import socket
import psutil
import re
from concurrent.futures import ThreadPoolExecutor
import threading
from env import *

# Função para calcular a operação
def calcular_operacao(operacao):
    try:
        # Remove espaços em branco da operação para garantir compatibilidade
        operacao = operacao.replace(" ", "")
        
        # Usa regex para separar os números e o operador, funcionando com ou sem espaços
        match = re.match(r"(\d+\.?\d*)([+\-*/])(\d+\.?\d*)", operacao)
        if not match:
            raise ValueError("Formato inválido de operação.")
        
        # Extrai os números e o operador da operação
        num1, operador, num2 = match.groups()
        num1, num2 = float(num1), float(num2)

        # Realiza a operação com base no operador
        if operador == "+":
            return str(num1 + num2)
        elif operador == "-":
            return str(num1 - num2)
        elif operador == "*":
            return str(num1 * num2)
        elif operador == "/":
            if num2 == 0:
                return "Erro: Divisão por zero."
            return str(num1 / num2)
        else:
            return "Erro: Operador inválido."
    except Exception as e:
        return f"Erro: {e}"
    
# Função para atender um cliente
def atender_cliente(cliente_socket):
    try:
        operacao = cliente_socket.recv(1024).decode()
        if not operacao:
            raise ValueError("Operação vazia recebida.")
        print(f"realizando a operação: {operacao}")
        resultado = calcular_operacao(operacao)
        print(f"O Resultado foi: {resultado}")
        cliente_socket.sendall(resultado.encode())  # Envia o resultado para o cliente
    except Exception as e:
        cliente_socket.sendall("Erro interno no servidor.".encode())  # Envia erro caso ocorra algum problema
    finally:
        cliente_socket.close()  # Fecha a conexão com o cliente

# Função para reportar carga de CPU do servidor
def reportar_carga():
    try:
        carga = psutil.cpu_percent(interval=0.1)  # Tempo de cálculo reduzido para respostas rápidas
        return str(carga)
    except Exception as e:
        return "Erro ao acessar CPU."

# Função do servidor para status de carga
def servidor_status(host, porta_status):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, porta_status))
            s.listen()
            print(f"Servidor de Carga em {host}:{porta_status} aguardando requisições...")
            while True:
                status_socket, _ = s.accept()
                carga = reportar_carga()  # Obtém a carga de CPU
                status_socket.sendall(carga.encode())  # Envia a carga de volta para o proxy
                status_socket.close()
    except Exception as e:
        print(f"Erro no servidor de carga: {e}")

# Função do servidor para processamento de cálculos
def servidor_servico(host, porta_servico):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, porta_servico))
            s.listen()
            print(f"Servidor de Serviço em {host}:{porta_servico} aguardando requisições...")
            with ThreadPoolExecutor(max_workers=10) as executor:  # Usando um pool de threads
                while True:
                    cliente_socket, _ = s.accept()
                    executor.submit(atender_cliente, cliente_socket)  # Submete a requisição ao pool de threads
    except Exception as e:
        print(f"Erro no servidor de cálculos: {e}")

# Função principal para iniciar os servidores em threads
def iniciar_servidor(host, porta_status, porta_servico):
    # Inicia o servidor de status em uma thread separada
    status_thread = threading.Thread(target=servidor_status, args=(host, porta_status))
    status_thread.start()
    
    # Inicia o servidor de serviço em uma thread separada
    servico_thread = threading.Thread(target=servidor_servico, args=(host, porta_servico))
    servico_thread.start()

# Inicia dois servidores de cálculo para testes (no mesmo host, com diferentes portas)
if __name__ == "__main__":
    # Iniciando servidores para duas portas de cálculo diferentes
    for servidor in servidores:
        iniciar_servidor(servidor['host'], servidor['porta_status'], servidor['porta_servico'])
    
    # Mantém o programa ativo enquanto os servidores rodam em segundo plano
    while True:
        pass  # Os servidores continuam funcionando em segundo plano
