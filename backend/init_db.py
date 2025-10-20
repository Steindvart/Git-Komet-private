#!/usr/bin/env python3
"""Initialize the database with tables."""

from app.db.session import init_db, engine
from app.models.models import Base

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
