import socket
import threading
import datetime
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from env import *

log_queue = Queue()

def obter_carga_servidor(host, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((host, porta))
            carga = s.recv(1024).decode()
            return float(carga)
    except Exception:
        return float('inf')

def escolher_servidor():
    cargas = [(srv, obter_carga_servidor(srv['host'], srv['porta_status'])) for srv in servidores]
    cargas.sort(key=lambda x: x[1])
    log_queue.put(f"[{datetime.datetime.now()}] Servidores ordenados: {[(srv['porta_servico'], carga) for srv, carga in cargas]}")
    return cargas[0][0]

def atender_cliente(cliente_socket):
    try:
        operacao = cliente_socket.recv(1024).decode()
        if not operacao:
            cliente_socket.sendall("Erro: Operação vazia.".encode())
            return
        
        log_queue.put(f"[{datetime.datetime.now()}] Cliente: Conectado, operação recebida: {operacao}")
        
        servidor = escolher_servidor()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((servidor['host'], servidor['porta_servico']))
            log_queue.put(f"[{datetime.datetime.now()}] Encaminhando para servidor {servidor['host']}:{servidor['porta_servico']}")
            s.sendall(operacao.encode())
            resultado = s.recv(1024).decode()
            log_queue.put(f"[{datetime.datetime.now()}] Resultado recebido do servidor: {resultado}")
        
        cliente_socket.sendall(resultado.encode())
    except Exception as e:
        cliente_socket.sendall(f"Erro interno no proxy: {e}".encode())
    finally:
        log_queue.put(f"[{datetime.datetime.now()}] Conexão com o cliente encerrada.")
        cliente_socket.close()

def iniciar_proxy():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, porta_proxy))
            s.listen()
            log_queue.put(f"[{datetime.datetime.now()}] Proxy Reverso aguardando conexões...")

            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    cliente_socket, _ = s.accept()
                    log_queue.put(f"[{datetime.datetime.now()}] Nova conexão com cliente.")
                    executor.submit(atender_cliente, cliente_socket)
    except Exception as e:
        log_queue.put(f"[{datetime.datetime.now()}] Erro no Proxy: {e}")

def processar_logs():
    while True:
        mensagem = log_queue.get()
        print(mensagem)
        log_queue.task_done()

if __name__ == "__main__":
    log_thread = threading.Thread(target=processar_logs, daemon=True)
    log_thread.start()
    iniciar_proxy()
