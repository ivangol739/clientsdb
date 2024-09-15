import psycopg2
from dotenv import load_dotenv
import os


def create_db(conn):
	with conn.cursor() as cur:
		cur.execute("""
			DROP TABLE phones;
			DROP TABLE clients;
		""")
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

def add_client(conn, first_name, last_name, email, phones=None):
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO clients (first_name, last_name, email)
			VALUES (%s, %s, %s) RETURNING id, first_name;
		""", (first_name, last_name, email))
		client_id = cur.fetchone()[0]
		if phones:
			for phone in phones:
				cur.execute("""
					INSERT INTO phones (phone, client_id)
					VALUES (%s, %s);
				""", (phone, client_id))
		conn.commit()

if __name__ == "__main__":
	load_dotenv()
	with psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password')) as conn:
		create_db(conn)
		add_client(conn, "Иван", "Головачев", "ivangol@gmail.com", [8789878997, 434654655])
	conn.close()
