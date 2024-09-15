import psycopg2
from dotenv import load_dotenv
import os


def create_db(conn):
	with conn.cursor() as cur:
		cur.execute("""
			CREATE TABLE IF NOT EXISTS clients (
				id SERIAL PRIMARY KEY,
				first_name VARCHAR(100),
				last_name VARCHAR(100),
				email VARCHAR(50) UNIQUE);
		""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS phones (
				id SERIAL PRIMARY KEY,
				phone VARCHAR(15),
				client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE);
		""")
		conn.commit()


if __name__ == "__main__":
	load_dotenv()
	with psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password')) as conn:
		create_db(conn)
	conn.close()
