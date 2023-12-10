import psycopg2

def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        isbn VARCHAR(13) PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255) NOT NULL,
                        year VARCHAR(255) NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR NOT NULL,
                        password VARCHAR NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_books (
                        user_id INTEGER REFERENCES users(id),
                        book_isbn VARCHAR(13) REFERENCES books(isbn),
                        PRIMARY KEY (user_id, book_isbn)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                        id SERIAL PRIMARY KEY,
                        comment VARCHAR NOT NULL,
                        rating INTEGER NOT NULL,
                        time TIMESTAMP WITH TIME ZONE NULL,
                        user_id INTEGER NULL,
                        book_id VARCHAR(255) NULL
                    )''')

    connection.commit()

def check_duplicate_queries(connection):
    cursor = connection.cursor()

    example_query = "SELECT * FROM books"

    cursor.execute(example_query)
    results = cursor.fetchall()

    cursor.execute(example_query)
    results_duplicate = cursor.fetchall()

    if len(results_duplicate) >= 2:
        print("La consulta se ha realizado dos veces.")
    else:
        print("La consulta no se ha realizado dos veces.")

try:
    connection = psycopg2.connect(
        dbname="nombre_basedatos",
        user="nombre_usuario",
        password="contraseña",
        host="localhost",
        port="5432"
    )

    create_tables(connection)

    check_duplicate_queries(connection)

except psycopg2.Error as e:
    print("Error al conectarse a la base de datos:", e)

finally:
    if 'connection' in locals() and connection is not None:
        connection.close()
