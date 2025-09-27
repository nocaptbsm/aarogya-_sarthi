import os
import psycopg2
import json # Needed for storing chat history
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

# --- User Management Functions ---

def add_user(mobile, name, age, gender, state, district, language):
    """Adds a new user to the database and returns the new user's ID."""
    conn = get_db_connection()
    user_id = None
    with conn.cursor() as cur:
        # The SQL command now includes the correct columns
        cur.execute(
            """
            INSERT INTO users (mobile_number, name, age, gender, state, district, language) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
            (mobile, name, age, gender, state, district, language)
        )
        user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    print(f"User {name} with ID {user_id} added successfully.")
    return user_id

def get_user(mobile):
    """Gets a user by their mobile number."""
    conn = get_db_connection()
    user = None
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE mobile_number = %s", (mobile,))
        user = cur.fetchone()
    conn.close()
    return user

def delete_user(mobile):
    """Deletes a user by their mobile number."""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE mobile_number = %s", (mobile,))
    conn.commit()
    conn.close()
    print(f"User with mobile number {mobile} deleted.")


# --- Symptom Checker Functions ---

def get_chat_history(user_id):
    """Retrieves or creates a chat history for a user."""
    conn = get_db_connection()
    history = None
    with conn.cursor() as cur:
        cur.execute("SELECT chat_history FROM symptom_chats WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        if result:
            history = result[0]
        else:
            # If no history exists, create a new entry
            cur.execute("INSERT INTO symptom_chats (user_id, chat_history) VALUES (%s, %s)", (user_id, json.dumps([])))
            history = []
    conn.commit()
    conn.close()
    return history

def save_chat_history(user_id, chat_history):
    """Saves the updated chat history to the database."""
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Use json.dumps to convert the Python list to a JSON string for the DB
        cur.execute(
            "UPDATE symptom_chats SET chat_history = %s WHERE user_id = %s",
            (json.dumps(chat_history), user_id)
        )
    conn.commit()
    conn.close()

# --- Outbreak Alert Functions ---

def has_user_seen_alert(user_id, alert_id):
    """Checks if a user has already been shown a specific alert."""
    conn = get_db_connection()
    seen = False
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM user_alerts_seen WHERE user_id = %s AND alert_id = %s", (user_id, alert_id))
        if cur.fetchone():
            seen = True
    conn.close()
    return seen

def mark_alert_as_seen(user_id, alert_id):
    """Records that a user has been shown a specific alert."""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO user_alerts_seen (user_id, alert_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (user_id, alert_id)
        )
    conn.commit()
    conn.close()

