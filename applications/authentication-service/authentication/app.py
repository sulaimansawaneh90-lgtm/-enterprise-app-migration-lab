import os
from datetime import datetime, timedelta, timezone

import jwt
import psycopg
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def get_db_connection():
    return psycopg.connect(DATABASE_URL)


@app.get("/health")
def health():
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1")

        return jsonify({
            "status": "healthy",
            "service": "authentication-service"
        }), 200

    except Exception:
        app.logger.exception("Database health check failed")
        return jsonify({
            "status": "unhealthy",
            "service": "authentication-service"
        }), 503


@app.post("/auth/register")
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({
            "error": "Username, email and password are required"
        }), 400

    if len(password) < 12:
        return jsonify({
            "error": "Password must contain at least 12 characters"
        }), 400

    password_hash = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                """,
                (username, email, password_hash)
            )

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except psycopg.errors.UniqueViolation:
        return jsonify({
            "error": "Username or email already exists"
        }), 409

    except Exception:
        app.logger.exception("Registration failed")
        return jsonify({
            "error": "Registration failed"
        }), 500


@app.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    try:
        with get_db_connection() as conn:
            user = conn.execute(
                """
                SELECT id, username, password_hash
                FROM users
                WHERE username = %s
                """,
                (username,)
            ).fetchone()

        if not user or not check_password_hash(user[2], password):
            return jsonify({
                "error": "Invalid username or password"
            }), 401

        token = jwt.encode(
            {
                "sub": str(user[0]),
                "username": user[1],
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 1800
        }), 200

    except Exception:
        app.logger.exception("Login failed")
        return jsonify({
            "error": "Login failed"
        }), 500
