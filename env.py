host = "192.168.0.15" #Endereço do Host
porta_proxy = 50000         # Porta de Proxy
porta_servico1 = 50001      # Porta de serviço do Servidor Nº 1
porta_status1 = 50002       # Porta de status do Servidor Nº 1
porta_servico2 = 50003      # Porta de serviço do Servidor Nº 2
porta_status2 = 50004       # Porta de status do Servidor Nº 2

#Lista de servidores
servidores = [
    {'host': host, 'porta_status': porta_status1, 'porta_servico': porta_servico1},
    {'host': host, 'porta_status': porta_status2, 'porta_servico': porta_servico2},
]
