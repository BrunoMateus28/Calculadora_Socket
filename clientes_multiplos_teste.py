import socket
import threading
import random
import time
from env import *

# Função para enviar uma operação de cálculo para o servidor e receber o resultado
def enviar_requisicao(servico_host, servico_porta):
    try:
        # Criar o socket para o servidor
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((servico_host, servico_porta))
        
        # Gerar uma operação matemática aleatória
        operacao = f"{random.randint(1, 10)} {random.choice(['+', '-', '*', '/'])} {random.randint(1, 10)}"
        
        # Enviar a operação para o servidor
        cliente_socket.sendall(operacao.encode())
        
        # Receber e exibir o resultado do servidor
        resultado = cliente_socket.recv(1024).decode()
        print(f"Operação: {operacao} = {resultado}")
        
    except Exception as e:
        print(f"Erro ao comunicar com o servidor: {e}")
    finally:
        cliente_socket.close()

# Função para simular múltiplos clientes
def testar_concorrencia(servico_host, servico_porta, num_clientes=10):
    threads = []
    
    # Criar e iniciar várias threads para enviar requisições simultâneas
    for _ in range(num_clientes):
        thread = threading.Thread(target=enviar_requisicao, args=(servico_host, servico_porta))
        thread.start()
        threads.append(thread)
    
    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

def testar_tempo_resposta(servico_host, servico_porta, num_clientes=10):
    # Iniciar o contador de tempo
    tempo_inicio = time.time()
    
    # Testar concorrência com múltiplos clientes
    testar_concorrencia(servico_host, servico_porta, num_clientes)
    
    # Calcular o tempo total
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio
    print(f"Tempo total para {num_clientes} requisições: {tempo_total:.2f} segundos.")
    
# Enviar uma operação inválida para testar o erro
def enviar_requisicao_invalida(servico_host, servico_porta):
    try:
        # Criar o socket para o servidor
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((servico_host, servico_porta))
        
        # Operação inválida (divisão por zero)
        operacao = "5 / 0"
        
        # Enviar a operação para o servidor
        cliente_socket.sendall(operacao.encode())
        
        # Receber e exibir o resultado do servidor
        resultado = cliente_socket.recv(1024).decode()
        print(f"Operação: {operacao} = {resultado}")
        
    except Exception as e:
        print(f"Erro ao comunicar com o servidor: {e}")
    finally:
        cliente_socket.close()

# if __name__ == "__main__":
#     enviar_requisicao_invalida(host, porta_proxy) # Teste com requisição invalida

# if __name__ == "__main__":
#     testar_tempo_resposta(host, porta_proxy, 10)  # Teste com 10 requisições


if __name__ == "__main__":
    testar_concorrencia(host, porta_proxy, 10)  # Teste com 10 clientes simulados
