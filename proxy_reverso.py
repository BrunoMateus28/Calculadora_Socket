import socket
from concurrent.futures import ThreadPoolExecutor
from env import *


# Função para obter a carga de CPU de um servidor
def obter_carga_servidor(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Timeout de 5 segundos
            s.connect((host, porta))
            carga = s.recv(1024).decode()
            return float(carga)
    except (socket.timeout, ConnectionRefusedError):
        return float('inf')
    except socket.error as e:
        return float('inf')
    except Exception as e:
        return float('inf')

def escolher_servidor():
    cargas = []
    for servidor in servidores:
        carga = obter_carga_servidor(servidor['host'], servidor['porta_status'])
        cargas.append((servidor, carga))
    cargas.sort(key=lambda x: x[1])
    return cargas[0][0]

def atender_cliente(cliente_socket):
    try:
        operacao = cliente_socket.recv(1024).decode()
        if not operacao:
            raise ValueError("Operação vazia recebida.")
        
        servidor = escolher_servidor()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((servidor['host'], servidor['porta_servico']))
            s.sendall(operacao.encode())
            resultado = s.recv(1024).decode()

        cliente_socket.sendall(resultado.encode())
    except Exception as e:
        cliente_socket.sendall("Erro interno".encode())
    finally:
        cliente_socket.close()

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
                    executor.submit(atender_cliente, cliente_socket)
    except Exception as e:
        print(f"Erro no Proxy: {e}")

if __name__ == "__main__":
    iniciar_proxy()
