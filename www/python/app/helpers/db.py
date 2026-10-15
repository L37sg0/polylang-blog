import mysql.connector
from flask import current_app

def _get_connection():
    config = current_app.config['DB_CONFIG']
    return mysql.connector.connect(**config)

def fetch_all(query, params=None):
    conn = _get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

def fetch_one(query, params=None):
    conn = _get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return result