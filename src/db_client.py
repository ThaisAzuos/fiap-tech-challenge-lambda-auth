import psycopg2

class DBClient:
    def __init__(self, host, dbname, user, password):
        self.connection = psycopg2.connect(host=host, database=dbname, user=user, password=password)

    def check_cpf(self, cpf):
        # Query DB
        pass
