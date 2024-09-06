![badge-action](https://github.com/CriticalNoob02/sync-database/actions/workflows/continuous_integration.yaml/badge.svg)

# Sync-Databases ➤ 🐍 

Uma aplicação simples e intuitiva para transferir dados entre bancos.

### Indice:

* [Estrutura](#estrutura)
    * [Stack](#stack)
    * [Organização](#organização)
    * [Monitoramento](#monitoramento)
* [Projeto](#projeto)
    * [Pre-requisitos](#pré-requisitos)
    * [Como rodar](#como-rodar)
    * [Exemplo](#exemplo)
    * [Configurando modulos](#configurando-modulos)

## Estrutura

### Stack
```
Python 3.10
psycopg2
cx-Oracle
prometheus-client
```


### Organização
A estrutura do projeto foi separada em duas partes: [Infraestrutura](./infra/) e [Aplicação](./app/) para segmentar melhor o projeto, facilitando modificações futuras.

![Sync-data(1)](https://github.com/user-attachments/assets/58f5e024-2a6a-4009-a446-d422090d657f)

![Sync-data](https://github.com/user-attachments/assets/06f04079-3a1f-49f6-b0c1-87857c19b92a)


### Monitoramento
O código possui um sistema de monitoramento com Prometheus vinculado ao Grafana, ambos sobem no [docker-compose-example](./infra/dockerfiles/docker-compose-example.yaml).

> OBS: A raspagem do prometheus está com um tempo bem baixo por conta do alto desempenho de transição dos dados nos bancos de exemplo...


## Projeto

### Pre-requisitos
Existe apenas um pré requisito para o projeto:

- Possui python 3.10 na maquina

> OBS: É possivel subir o container com a imagem do python...


### Como rodar

<details>
<summary><b>Subir com container</b></summary>

- Para subir o compose de exemplo basta digitar no terminal `make compose-example`
- Aguarde pacificamente...

> OBS: Caso deseje criar um proprio compose basta criar no mesmo diretorio e mudar o nome do arquivo no [makefile](./makefile)

</details>

<details>
<summary><b>Subir com venv</b></summary>

- Crie uma venv usando o comando `make create-venv`;
- Entre na venv usando o comando `source .venv/bin/activate`;
- Instale as dependencias usando o comando `make install`;
- Copie o arquivo [.env.example](./infra/envs/.env.example) e remova o `.example`;
- Preencha suas variáveis de ambiente;
- Rode aplicação usando o comando `make run`;

</details>


### Configurando modulos
Cada módulo é referente a um banco de dados, você deve definir a ordem de qual módulo será o `source` e `final` usando as variáveis de [ambiente](./infra/envs/.env.example#L4).

Para realizar a configuração de um novo módulo, basta seguir estes passos.

1. Crie uma pasta com o nome do módulo dentro de [modules](./app/modules/).
2. Crie uma pasta com o nome composto por um índice numérico e o nome da tabela, `ex: 1-tabela_exemplo`
3. Crie um arquivo chamado `mapper.py`
```python
table_map = {
    "table": "dados_para_receber_testes",
    "schema": "public",
    "ref": "id",
    "limit": 100
}
```
> OBS: as chaves de ref e limit sao obrigatorias, porem caso sua tabela nao possua nenhum index de referencia ou deseje trazer todos os dados sem limite para a query basta deixar ambos sem dados seguindo o exemplo da tabela [envio_sem_ref](./app/modules/source_example/tables/2-envio_sem_ref/mapper.py);  

4. Opcionalmente, é possível adicionar um tratamento para os dados lidos do módulo `source`, basta adicionar um arquivo `processor.py` no mesmo nível do mapper da tabela seguindo o exemplo da tabela [dados_para_testes](./app/modules/source_example/tables/1-dados_para_testes/process.py). As únicas regras para a função são manter o nome `process`, RECEBER e DEVOLVER uma lista de tuplas.


### Exemplo
Foi criada uma base para testar a aplicação localmente, você pode seguir os seguintes passos para rodar os exemplos:

- Copie o arquivo [env.example](./infra/envs/.env.example) e renomeio para .env mantendo os mesmos dados;
- Rode o seguinte comando no terminal `make compose-example`;
- Certifique-se de que os bancos subiram;
- Rode o seguinte comando no terminal `make migration-example`;
- Certifique-se de que as tabelas foram criadas e populadas;
- Acesse a URL `http://localhost:3000/login` e use o e-mail `admin` e senha `admin` para o primeiro acesso.
- Vincular o prometheus no grafana, acesse o módulo de `Connections` do grafana e adicione um novo Data Source;
- Procure pelo core do Prometheus e configure a seguinte URL `http://prometheus:9090`
- Acesse o módulo de `Dashboards`, crie um dashboard usando este molde [json](./infra/data/grafana_example/dashboard.json)
- Para finalizar, inicie novamente o contêiner do sync-database que está caido no compose;

<p align="center">
  <a href="https://github.com/radarsaude/api-ia">
    <img src="https://4kwallpapers.com/images/walls/thumbs_3t/15294.png" width="100%" height="320" alt="Banner">
  </a>
<p/>
