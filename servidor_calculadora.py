import socket
import psutil
from concurrent.futures import ThreadPoolExecutor

from env import *

# Função para calcular a operação
def calcular_operacao(operacao):
    try:
        # Validar e processar a operação com segurança (evitar o uso de eval)
        if not operacao:
            raise ValueError("Operação inválida.")
        
        # Simples parser de operações matemáticas
        parts = operacao.split()
        if len(parts) != 3:
            raise ValueError("Formato inválido de operação.")
        
        num1, operador, num2 = parts
        num1, num2 = float(num1), float(num2)

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
        carga = psutil.cpu_percent(interval=1)
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

# Função principal para iniciar os servidores
def iniciar_servidor(host, porta_status, porta_servico):
    # Inicia os dois servidores em uma única execução
    # Um servidor para a porta de status
    servidor_status(host, porta_status)
    
    # Um servidor para a porta de cálculo (usando o pool de threads para processar as requisições)
    servidor_servico(host, porta_servico)

# Inicia dois servidores de cálculo para testes (no mesmo host, com diferentes portas)
if __name__ == "__main__":
    # Iniciando servidores para duas portas de cálculo diferentes
    for servidor in servidores:
        iniciar_servidor(servidor)

    # Para manter os servidores rodando, você pode adicionar um loop infinito ou um controle de encerramento.
    while True:
        pass  # Servidores continuam funcionando em segundo plano
