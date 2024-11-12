host = "192.168.0.15"  # Endereço do Host
porta_proxy = 50000    # Porta de Proxy

# Definição das portas para cada servidor
porta_servico1 = 50001      # Porta de serviço do Servidor Nº 1
porta_status1 = 50002       # Porta de status do Servidor Nº 1
porta_servico2 = 50003      # Porta de serviço do Servidor Nº 2
porta_status2 = 50004       # Porta de status do Servidor Nº 2
porta_servico3 = 50005      # Porta de serviço do Servidor Nº 3
porta_status3 = 50006       # Porta de status do Servidor Nº 3
porta_servico4 = 50007      # Porta de serviço do Servidor Nº 4
porta_status4 = 50008       # Porta de status do Servidor Nº 4
porta_servico5 = 50009      # Porta de serviço do Servidor Nº 5
porta_status5 = 50010       # Porta de status do Servidor Nº 5

# Lista de servidores com seus respectivos hosts, portas de serviço e de status
servidores = [
    {'host': host, 'porta_status': porta_status1, 'porta_servico': porta_servico1},
    {'host': host, 'porta_status': porta_status2, 'porta_servico': porta_servico2},
    {'host': host, 'porta_status': porta_status3, 'porta_servico': porta_servico3},
    {'host': host, 'porta_status': porta_status4, 'porta_servico': porta_servico4},
    {'host': host, 'porta_status': porta_status5, 'porta_servico': porta_servico5},
]
