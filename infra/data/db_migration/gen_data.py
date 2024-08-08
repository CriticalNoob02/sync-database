import psycopg2
import random
import string


conn = psycopg2.connect(
    host="localhost",
    port="5434",
    user="postgres",
    password="2024",
    dbname="postgres"
)

cur = conn.cursor()


def gerar_nome(tamanho=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))


print('iniciando insert dados_enviar_ref')
for i in range(500000):
    nome = gerar_nome(200)
    cur.execute("INSERT INTO dados_enviar_ref (nome) VALUES (%s)", (nome,))

conn.commit()

cur.execute("SELECT nome FROM dados_enviar_ref")
nomes = cur.fetchall()

print('iniciando insert dados_enviar')
for nome in nomes:
    nu_aleatorio = random.randint(1, 500000)
    cur.execute("INSERT INTO dados_enviar (nome, nu_aleatorio) VALUES (%s, %s)", (nome[0], nu_aleatorio))

conn.commit()
