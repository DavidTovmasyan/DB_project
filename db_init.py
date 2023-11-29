import psycopg2
from psycopg2 import sql

def initialize_database(db_name, db_owner, db_host, db_user, db_password):
    try:
        # Connect to the default PostgreSQL database (usually 'postgres')
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )

        # Set autocommit to True to execute CREATE DATABASE and ALTER DATABASE
        conn.autocommit = True
        cursor = conn.cursor()

        # Create a new database with a specific name
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_name)
        ))

        # Set the owner of the database
        cursor.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
            sql.Identifier(db_name),
            sql.Identifier(db_owner)
        ))

        # Connect to the newly created database
        conn.close()
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        # Create tables for vacation_place, person, and tour
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE vacation_place (
                id SERIAL PRIMARY KEY,
                country VARCHAR(255),
                place VARCHAR(255),
                hotel VARCHAR(255),
                main_speciality TEXT,
                sea VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE person (
                id SERIAL PRIMARY KEY,
                passport VARCHAR(255),
                foreign_passport VARCHAR(255),
                country VARCHAR(255),
                contacts VARCHAR(255),
                name VARCHAR(255),
                surname VARCHAR(255),
                second_name VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE tour (
                id SERIAL PRIMARY KEY,
                price DECIMAL(10, 2),
                discount DECIMAL(10, 2),
                start_date DATE,
                end_date DATE,
                vacation_place_id INT REFERENCES vacation_place(id),
                person_id INT REFERENCES person(id)
            )
        """)

        print("Database initialization successful!")

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

# Replace these values with your actual database details
db_name = 'travel_agency'
db_owner = 'ubmaster'
db_host = 'localhost'
db_user = 'postgres'
db_password = '12345678'

# Call the function to initialize the database
initialize_database(db_name, db_owner, db_host, db_user, db_password)
