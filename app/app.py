from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "securecicd"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "app_password"),
    )


@app.route("/")
def home():
    return "Secure CI/CD Pipeline Lab"


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return jsonify(
            status="healthy",
            database="connected"
        ), 200

    except Exception:
        return jsonify(
            status="unhealthy",
            database="disconnected"
        ), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)