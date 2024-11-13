import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from env import *

# Dicionário global para armazenar as cargas dos servidores
cargas_servidores = {}


# Função para obter a carga de CPU de um servidor
def obter_carga_servidor(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout ajustado para respostas mais rápidas
            s.connect((host, porta))
            carga = s.recv(1024).decode()
            return float(carga)
    except (socket.timeout, ConnectionRefusedError):
        return float('inf')
    except socket.error as e:
        return float('inf')
    except Exception as e:
        return float('inf')


# Função para atualizar as cargas dos servidores periodicamente
def atualizar_cargas():
    global cargas_servidores
    while True:
        # Atualiza cargas de forma assíncrona para não sobrecarregar com chamadas constantes
        for servidor in servidores:
            carga = obter_carga_servidor(servidor['host'], servidor['porta_status'])
            cargas_servidores[servidor['porta_status']] = carga
        time.sleep(0.5)  # Intervalo de atualização ajustado


# Função para escolher o servidor com a menor carga
def escolher_servidor():
    # Ordena servidores com base nas cargas armazenadas em `cargas_servidores`
    servidores_ordenados = sorted(
        servidores, key=lambda srv: cargas_servidores.get(srv['porta_status'], float('inf'))
    )
    return servidores_ordenados[0] if servidores_ordenados else servidores[0]


# Função para atender uma requisição do cliente
def atender_cliente(cliente_socket):
    try:
        operacao = cliente_socket.recv(1024).decode()
        if not operacao:
            raise ValueError("Operação vazia recebida.")
        
        # Seleciona o servidor com menor carga usando os dados atualizados
        servidor = escolher_servidor()

        # Conecta-se ao servidor selecionado e envia a operação
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((servidor['host'], servidor['porta_servico']))
            print(cargas_servidores)
            print(f"Conectado ao servidor {servidor['host']}:{servidor['porta_servico']}")
            s.sendall(operacao.encode())
            resultado = s.recv(1024).decode()
            print(f"Resultado a ser enviado: {resultado}")
        cliente_socket.sendall(resultado.encode())
    except Exception as e:
        cliente_socket.sendall(f"Erro interno: {e}".encode())
    finally:
        cliente_socket.close()


# Função para iniciar o proxy e gerenciar requisições de clientes
def iniciar_proxy():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, porta_proxy))
            s.listen()
            print("Proxy Reverso aguardando conexões...")

            # Usando ThreadPoolExecutor para gerenciar as requisições de forma eficiente
            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    cliente_socket, _ = s.accept()
                    print("Cliente Conectado!")
                    executor.submit(atender_cliente, cliente_socket)
    except Exception as e:
        print(f"Erro no Proxy: {e}")


if __name__ == "__main__":
    # Inicia a thread para atualização das cargas dos servidores
    thread_carga = threading.Thread(target=atualizar_cargas)
    thread_carga.daemon = True
    thread_carga.start()

    # Inicia o proxy
    iniciar_proxy()
