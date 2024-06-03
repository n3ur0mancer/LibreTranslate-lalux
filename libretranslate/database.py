import os
import re
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

def normalize_text(text):
    # Normalize text: lowercase and remove punctuation (simple example, can be enhanced)
    text = re.sub(r'[^\w\s/]', '', text)
    return text.lower()

class PostgresDB:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER_READER')
        self.password = os.getenv('DB_PASSWORD')
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            print("Connection successful")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
    
    def fetch_snippets(self, source_language, target_language):
        try:
            with self.connection.cursor() as cursor:
                query = sql.SQL("""
                    SELECT id, {source_field}, {target_field}
                    FROM translations
                """).format(
                    source_field=sql.Identifier(source_language),
                    target_field=sql.Identifier(target_language)
                )
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching snippets: {e}")
            return []
