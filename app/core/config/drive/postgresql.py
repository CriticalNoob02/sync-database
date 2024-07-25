import psycopg2
import os

TEST_QUERY = "SELECT version()"


def connect_ps(isSource: bool):
    if isSource:
        return psycopg2.connect(
                dbname=os.environ["DB_NAME_SOURCE"],
                host=os.environ["DB_HOST_SOURCE"],
                port=os.environ["DB_PORT_SOURCE"],
                user=os.environ["DB_USERNAME_SOURCE"],
                password=os.environ["DB_PASSWORD_SOURCE"]
            )
    else:
        return psycopg2.connect(
                dbname=os.environ["DB_NAME_FINAL"],
                host=os.environ["DB_HOST_FINAL"],
                port=os.environ["DB_PORT_FINAL"],
                user=os.environ["DB_USERNAME_FINAL"],
                password=os.environ["DB_PASSWORD_FINAL"]
            )
