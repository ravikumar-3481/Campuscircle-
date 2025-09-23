from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for front-end fetch calls

# Database setup
DB_NAME = 'alumni.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if not all([name, email, password, phone]):
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, password, phone) VALUES (?, ?, ?, ?)',
                       (name, email, hashed_password, phone))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[3], password):
        return jsonify({'message': f'Welcome back, {user[1]}!'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
