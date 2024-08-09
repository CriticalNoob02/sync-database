import psycopg2
import random
import string
from typing import Literal


conn_source = psycopg2.connect(
    host="localhost",
    port="5434",
    user="postgres",
    password="2024",
    dbname="postgres"
)
cur_source = conn_source.cursor()

conn_final = psycopg2.connect(
    host="localhost",
    port="5433",
    user="postgres",
    password="2024",
    dbname="postgres"
)
cur_final = conn_final.cursor()


def gen_tables(type: Literal["final", "source"]) -> str:
    match type:
        case "final":
            return """
drop table if exists dados_receber_ref;
create table dados_receber_ref (
id SERIAL PRIMARY key,
id_origem int8 NOT NULL,
nome varchar(500) NOT NULL
);

drop table if exists dados_receber;
create table dados_receber (
id SERIAL PRIMARY key,
nome varchar(500) NOT null,
nu_aleatorio integer
);
        """
        case "source":
            return """
DROP TABLE IF EXISTS dados_enviar_ref;
CREATE TABLE dados_enviar_ref (
id SERIAL PRIMARY key,
nome varchar(500) NOT NULL
);

DROP TABLE IF EXISTS dados_enviar;
CREATE TABLE dados_enviar (
nome varchar(500) NOT null,
nu_aleatorio integer
);
        """


def gen_names(tamanho=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))


print('Iniciando estrutura dos bancos...')
query = gen_tables('final')
cur_final.execute(query)
conn_final.commit()

query = gen_tables('source')
cur_source.execute(query)
conn_source.commit()

print('Iniciando insert dados_enviar_ref...')
for i in range(500000):
    nome = gen_names(200)
    cur_source.execute("INSERT INTO dados_enviar_ref (nome) VALUES (%s)", (nome,))
conn_source.commit()

print('iniciando insert dados_enviar')
cur_source.execute("SELECT nome FROM dados_enviar_ref")
nomes = cur_source.fetchall()

for nome in nomes:
    nu_aleatorio = random.randint(1, 500000)
    cur_source.execute("INSERT INTO dados_enviar (nome, nu_aleatorio) VALUES (%s, %s)", (nome[0], nu_aleatorio))

conn_source.commit()
