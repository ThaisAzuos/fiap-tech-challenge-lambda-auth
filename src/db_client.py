import psycopg2
import os

class DBClient:
    def __init__(self, host=None, dbname=None, user=None, password=None):
        self.host = host or os.environ.get('DB_HOST')
        self.dbname = dbname or os.environ.get('DB_NAME')
        self.user = user or os.environ.get('DB_USER')
        self.password = password or os.environ.get('DB_PASSWORD')
        self.connection = None

    def _get_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.dbname,
                user=self.user,
                password=self.password
            )
        return self.connection

    def check_cpf(self, cpf):
        """
        Check if CPF exists in the database and return customer info.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            query = "SELECT id, nome FROM cliente WHERE cpf = %s"
            cursor.execute(query, (cpf,))
            result = cursor.fetchone()

            cursor.close()

            if result:
                return {'id': result[0], 'nome': result[1]}
            return None

        except Exception as e:
            print(f"Database error: {e}")
            return None
