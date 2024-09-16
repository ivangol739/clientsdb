import psycopg2
from dotenv import load_dotenv
import os


def create_db(conn):
	with conn.cursor() as cur:
		# cur.execute("""
		# 	DROP TABLE phones;
		# 	DROP TABLE clients;
		# """)
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

def add_phone(conn, phone, client_id):
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO phones (phone, client_id)
			VALUES (%s, %s);
		""", (phone, client_id))
		conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
	with conn.cursor() as cur:
		if first_name:
			cur.execute("""
				UPDATE clients SET first_name = %s WHERE id = %s;
			""", (first_name, client_id))

		if last_name:
			cur.execute("""
				UPDATE clients SET last_name = %s WHERE id = %s;
			""", (last_name, client_id))

		if email:
			cur.execute("""
				UPDATE clients SET email = %s WHERE id = %s;
			""", (email, client_id))

		if first_name is not None:
			cur.execute("""
				DELETE FROM phones WHERE client_id = %s;
			""", (client_id,))

			for phone in phones:
				cur.execute("""
					INSERT INTO phones (phone, client_id)
					VALUES (%s, %s);
				""", (phone, client_id))
		conn.commit()

def delete_phone(conn, client_id, phone):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM phones WHERE client_id = %s AND phone = %s;
		""", (client_id, phone))
		conn.commit()

def delete_client(conn, client_id):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM clients WHERE id = %s;
		""", (client_id,))
		conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
	with conn.cursor() as cur:
		query = """
			SELECT c.id, c.first_name, c.last_name, c.email, p.phone
			FROM clients c
			LEFT JOIN phones p ON p.client_id = c.id
			WHERE 1=1
		"""
		params = []
		if first_name:
			query += "AND c.first_name = %s"
			params.append(first_name)

		if last_name:
			query += "AND c.last_name = %s"
			params.append(last_name)

		if email:
			query += "AND c.email = %s"
			params.append(email)

		if phone:
			query += "AND p.phone = %s"
			params.append(phone)

		cur.execute(query, tuple(params))
		res = cur.fetchall()
		print(res)
		for i in res:
			print(f"id: {i[0]}, first_name: {i[1]}, last_name: {i[2]}, email: {i[3]}, phone: {i[4]}")


if __name__ == "__main__":
	load_dotenv()
	with psycopg2.connect(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password')) as conn:
		create_db(conn)
		# add_client(conn, "Иван", "Головачев", "ivangol@gmail.com", ['8789878997', '434654655'])
		# add_phone(conn, "1212123423", 1)
		# change_client(conn, 1, "Петр", "Петров", "fgdbbdb@gmail.com", [1111111111])
		# delete_phone(conn, 1, "1111111111")
		# delete_client(conn, 1)
		# add_client(conn, "Николай", "Николаев", "niknik@gmail.com", ['232523423', '2345757'])
		# add_client(conn, "Сергей", "Сергеев", "serser@gmail.com", ['764345t32', '6567657'])
		find_client(conn, None, None, None, "2345757")
	conn.close()
