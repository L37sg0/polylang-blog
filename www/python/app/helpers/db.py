import mysql.connector
from flask import current_app

def _get_connection():
    config = current_app.config['DB_CONFIG']
    return mysql.connector.connect(**config)

def fetch_all(query: str, params=None):
    conn = _get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

def fetch_one(query: str, params=None):
    conn = _get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return result

def insert(query: str, params=None) -> int:
    conn = _get_connection()
    cursor = conn.cursor()
    
    cursor.execute(query, params or ())
    conn.commit()
    last_id = cursor.lastrowid
        
    cursor.close()
    conn.close()
    
    return last_id