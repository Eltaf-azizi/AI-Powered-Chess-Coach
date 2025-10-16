# backend/database/models.py
"""
Simple DB helper module. Provides init_db() to ensure schema exists.
Used at app startup.
"""
import os
from ..services.database_service import DatabaseService



def init_db():
    # instantiate service to ensure schema created
    base = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base, "db.sqlite3")
    DatabaseService(db_path)
