import os

import mysql.connector
from flask import Flask, jsonify, render_template

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "securecicd"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "app_password"),
    )


@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )
    return response


@app.route("/")
def home():
    return render_template(
        "index.html",
        image_tag=os.getenv("IMAGE_TAG", "local"),
        docker_username=os.getenv("DOCKER_USERNAME", "local"),
    )


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return jsonify(
            status="healthy",
            database="connected",
        ), 200

    except mysql.connector.Error:
        return jsonify(
            status="unhealthy",
            database="disconnected",
        ), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
