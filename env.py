host = "127.0.0.1" #Endereço do Host
porta_proxy = 65432 #Porta de Proxy
porta_servico1 = 65433 #Porta de serviço do Servidor Nº 1
porta_status1 = 65434 #Porta de status do Servidor Nº 1
porta_servico2 = 65435 #Porta de serviço do Servidor Nº 2
porta_status2 = 654336 #Porta de status do Servidor Nº 2

#Lista de servidores
servidores = [
    {'host': host, 'porta_status': porta_status1, 'porta_servico': porta_servico1},
    {'host': host, 'porta_status': porta_status2, 'porta_servico': porta_servico2},
]