import mysql.connector
from mysql.connector import Error
from config import Config
import os


def get_db_connection():
    try:
        print(f"Connecting to MySQL at: {Config.MYSQL_HOST}")
        print(f"Using user: {Config.MYSQL_USER}")
        print(f"Using database: {Config.MYSQL_DB}")

        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
        )

        connection.autocommit = False

        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def execute_query(query, params=None, fetch=False, many=False):
    connection = get_db_connection()
    if not connection:
        raise Exception("No se pudo conectar a la base de datos")

    cursor = connection.cursor(dictionary=True)
    result = None

    try:
        print(f"Executing query: {query}")
        print(f"With params: {params}")

        if params:
            if many:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)
        else:
            cursor.execute(query)

        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            connection.commit()
            print(f"Transaction committed. Last row ID: {cursor.lastrowid}")
            result = cursor.lastrowid

        if fetch:
            result = cursor.fetchall()
            print(f"Query returned {len(result)} rows")

        return result

    except Error as e:
        connection.rollback()
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        raise

    finally:
        cursor.close()
        connection.close()
        print("Database connection closed")


def init_db():
    print("Database initialization started")
    print(f"MYSQL_HOST from ENV: {os.environ.get('MYSQL_HOST')}")
    print(f"MYSQL_HOST from Config: {Config.MYSQL_HOST}")

    import time

    time.sleep(10)

    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
        )

        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        cursor.execute(f"USE {Config.MYSQL_DB}")

        try:
            with open("schema.sql", "r") as f:
                sql_commands = f.read().split(";")

                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)

            connection.commit()
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error connecting to MySQL for initialization: {e}")
        time.sleep(20)
        try:
            connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
            )
            print("Connection successful on retry")
        except Error as e2:
            print(f"Error on second attempt: {e2}")
