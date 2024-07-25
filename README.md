![badge-action](https://github.com/CriticalNoob02/sync-database/actions/workflows/continuous_deployment.yaml/badge.svg)

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
    * [Scripts](#scripts)
    * [Exemplo](#exemplo)
    * [Testes](#testes)
    * [Configurando modulos](#configurando-modulos)

---
---

<p align="center">
  <a href="https://github.com/radarsaude/api-ia">
    <img src="https://4kwallpapers.com/images/walls/thumbs_3t/15294.png" width="80%" height="350" alt="Banner">
  </a>
<p/>

---
---

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

> OBS: A pasta [db](./infra/db) contem os volumes para subir os bancos de exemplo juntamente com a stack de monitoramento.


### Monitoramento
O código possui um sistema de monitoramento com Prometheus vinculado ao Grafana, ambos sobem no [docker-compose-example](./infra/dockerfiles/docker-compose-example.yaml), existe alguns passos a fazer para configurar o grafana com o prometheus;

1. Acesse a url `http://localhost:3000/login` e use o email `admin` e senha `admin` para  o primeiro acesso
2. Vicular o prometheus no grafana, acesse o modulo de `Connections` do grafana e adicione um novo Data Source;
3. Procure pelo core do Prometheus e configure a seguinte url `http://prometheus:9090`
4. Acesse o modulo de `Dashboards`, crie um dashboard usando este molde [json](./infra/data/grafana_example/dashboard.json)

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


### Scripts
Foi criado alguns scripts para facilitar mais o trabalho com o sync-database;

... Aguarde ...


### Testes
O servico possui alguns testes das [tasks](./app/core/tasks/__init__.py) usando o [docker-compose-tests](./infra/dockerfiles/docker-compose-tests.yaml)

... Aguarde ...
