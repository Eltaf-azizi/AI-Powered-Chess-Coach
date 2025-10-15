# backend/services/database_service.py
import sqlite3
import os
from typing import Optional, List, Dict

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "..", "database", "db.sqlite3")

class DatabaseService:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._ensure_schema()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _ensure_schema(self):
        conn = self._get_conn()
        cur = conn.cursor()
        # users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # games
        cur.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id TEXT PRIMARY KEY,
                fen TEXT,
                mode TEXT,
                white TEXT,
                black TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # moves
        cur.execute("""
            CREATE TABLE IF NOT EXISTS moves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id TEXT,
                move_uci TEXT,
                fen TEXT,
                move_no INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games(id)
            );
        """)
        conn.commit()
        conn.close()

    # Users
    def create_user(self, username: str) -> int:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return uid
