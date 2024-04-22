# Script de Teste de Velocidade e Latência

## Visão Geral


Este script Python permite testar a velocidade da conexão entre pontos específicos da rede, bem como a latência e a perda de pacotes para esses destinos. Utiliza as bibliotecas `iperf3` para medir a velocidade da conexão, `ping3` para testar a latência e `matplotlib` para gerar gráficos dos resultados.

## Requisitos

- Python 3.x instalado no sistema
- Bibliotecas Python `speedtest-cli`, `ping3` e `matplotlib`

## Instalação das Dependências

Você pode instalar as dependências utilizando o `pip`. Execute o seguinte comando no terminal ou prompt de comando:

```bash
    pip install speedtest-cli ping3 matplotlib
```


## Uso

1. Clone ou baixe este repositório para o seu sistema.
2. Navegue até o diretório onde o script está localizado.
3. Execute o script usando Python:


```bash
    python speed_test.py
```

## Funcionalidades

O script realiza as seguintes tarefas:

- Testa a velocidade da conexão com a internet, medindo a velocidade de upload e download.
- Testa a latência e a perda de pacotes para um determinado destino.
- Gera gráficos com os resultados dos testes de velocidade, latência e perda de pacotes.

## Saída

Após a execução do script, ele produzirá a seguinte saída:

- Velocidade de upload e download em Mbps.
- Latência média em milissegundos (ms).
- Taxa de perda de pacotes em porcentagem (%).
- Gráficos representando os resultados dos testes de velocidade, latência e perda de pacotes.

## Exemplo de Saída

Velocidade de Upload: 10.23 Mbps
Velocidade de Download: 50.65 Mbps
Latência Média: 25.34 ms
Taxa de Perda de Pacotes: 2.5 %

## Observações

- Este script realiza testes reais de velocidade e latência. Os resultados podem variar dependendo das condições da rede e da conexão com a internet.
- Certifique-se de ter uma conexão de internet estável ao executar o script.
- Os resultados dos testes podem ser afetados por fatores externos, como congestionamento de rede e distância do servidor de teste.