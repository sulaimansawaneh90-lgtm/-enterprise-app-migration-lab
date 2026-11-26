import os
from functools import wraps

import jwt
import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def get_db_connection():
    return psycopg.connect(DATABASE_URL)


def require_authentication(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")

        scheme, separator, token = authorization.partition(" ")

        if not separator or scheme.lower() != "bearer" or not token:
            return jsonify({"error": "Bearer token required"}), 401

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"],
                options={"require": ["exp", "sub"]}
            )

            request.user_id = int(payload["sub"])

        except (jwt.InvalidTokenError, ValueError, TypeError):
            return jsonify({"error": "Invalid or expired token"}), 401

        return function(*args, **kwargs)

    return wrapper


@app.get("/health")
def health():
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1")

        return jsonify({
            "status": "healthy",
            "service": "backend-api"
        }), 200

    except Exception:
        app.logger.exception("Backend health check failed")
        return jsonify({
            "status": "unhealthy",
            "service": "backend-api"
        }), 503


@app.get("/api/profile")
@require_authentication
def profile():
    try:
        with get_db_connection() as conn:
            user = conn.execute(
                """
                SELECT id, username, email, created_at
                FROM users
                WHERE id = %s
                """,
                (request.user_id,)
            ).fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "created_at": user[3].isoformat()
        }), 200

    except Exception:
        app.logger.exception("Profile retrieval failed")
        return jsonify({"error": "Unable to retrieve profile"}), 500


if __name__ == "__main__":
    app.run(port=5002)
