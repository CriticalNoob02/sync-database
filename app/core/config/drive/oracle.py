import cx_Oracle
import os

TEST_QUERY = "SELECT * FROM V$VERSION"


def connect_oracle(isSource: bool):
    if isSource:
        connection_details = {
            "user": os.environ["USERNAME_SOURCE"],
            "password": os.environ["PASSWORD_SOURCE"],
            "dsn": cx_Oracle.makedsn(
                os.environ["HOST_SOURCE"],
                os.environ["PORT_SOURCE"],
                service_name=f"{os.environ['DSN_SOURCE']}/{os.environ['SERVICE_NAME_SOURCE']}"
            ),
            "encoding": "UTF-8"
        }
        return cx_Oracle.connect(**connection_details)
    else:
        connection_details = {
            "user": os.environ["USERNAME_FINAL"],
            "password": os.environ["PASSWORD_FINAL"],
            "dsn": cx_Oracle.makedsn(
                os.environ["HOST_FINAL"],
                os.environ["PORT_FINAL"],
                service_name=f"{os.environ['DSN_FINAL']}/{os.environ['SERVICE_NAME_FINAL']}"
            ),
            "encoding": "UTF-8"
        }
        return cx_Oracle.connect(**connection_details)
