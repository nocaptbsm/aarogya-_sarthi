import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    return conn

# UPDATED: Now includes a 'language' parameter
def add_user(mobile, name, age, gender, state, district, language):
    conn = get_db_connection()
    with conn.cursor() as cur:
        # UPDATED: The SQL command now includes the language column
        cur.execute(
            "INSERT INTO users (mobile_number, name, age, gender, state, district, language) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (mobile, name, age, gender, state, district, language)
        )
    conn.commit()
    conn.close()
    print(f"User {name} added successfully.")

# Function to get a user by their mobile number
def get_user(mobile):
    conn = get_db_connection()
    user = None
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE mobile_number = %s", (mobile,))
        user = cur.fetchone()
    conn.close()
    return user
# Function to delete a user by their mobile number
def delete_user(mobile):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE mobile_number = %s", (mobile,))
    conn.commit()
    conn.close()
    print(f"User with mobile number {mobile} deleted.")