# Calculadora Distribuída com Proxy Reverso

Este projeto implementa uma calculadora distribuída que utiliza sockets para comunicação entre **clientes**, **proxy reverso** e **servidores de cálculo**. O proxy gerencia o tráfego de requisições e encaminha cada operação para o servidor com menor carga no momento da requisição, otimizando o uso de recursos e o tempo de resposta.

## Arquitetura

A estrutura principal é dividida em três componentes:

### Proxy Reverso:
- Recebe operações dos clientes e consulta a carga dos servidores disponíveis.
- Escolhe o servidor com menor carga e redireciona a requisição de cálculo.
- Envia o resultado do cálculo de volta ao cliente.

### Servidores de Cálculo:
- Cada servidor expõe duas portas:
  - **Porta de status**: indica a carga de CPU ao proxy.
  - **Porta de serviço**: recebe e processa operações matemáticas.
- Processam operações enviadas pelo proxy e devolvem o resultado.

### Clientes:
- Conectam-se ao proxy reverso e enviam uma operação matemática (ex.: "5 + 3").
- Recebem o resultado do proxy, calculado por um dos servidores disponíveis.

## Pré-requisitos

- Python 3.6+ instalado.

## Estrutura do Código

- **proxy_reverso.py**: Implementa o servidor proxy reverso que balanceia as requisições entre servidores de cálculo.
- **cliente.py**: Envia uma operação ao proxy e recebe o resultado.
- **clientes_multiplos_teste.py**: Simula múltiplos clientes para testes de concorrência.
- **servidor_calculo.py**: Implementa um servidor de cálculo que responde com sua carga e executa operações.

## Como Executar

1. **Iniciar Servidores de Cálculo**: Em terminais separados, execute `servidor_calculo.py` para cada servidor desejado.

    ```bash
    python servidor_calculo.py
    ```

2. **Iniciar o Proxy Reverso**: Em outro terminal, execute `proxy_reverso.py`.

    ```bash
    python proxy_reverso.py
    ```

3. **Iniciar Clientes**:
   - Para iniciar um cliente:

      ```bash
      python cliente.py
      ```

   - Para simular múltiplos clientes:

      ```bash
      python clientes_multiplos_teste.py
      ```

## Testes e Simulações

Para simular uma carga maior, use `clientes_multiplos_teste.py`, que cria várias threads de clientes enviando requisições simultâneas. O proxy gerenciará o balanceamento entre os servidores disponíveis.

## Exemplo de Uso

Com o proxy e os servidores de cálculo iniciados, o cliente pode enviar operações como `5 + 3` ou `10 / 2`. O proxy delega essas operações para um dos servidores, e o resultado é retornado ao cliente.
