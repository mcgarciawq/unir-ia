#!/usr/bin/env python3
"""Initialize database tables using SQLAlchemy."""
import sys
from src.core.database import engine, Base
from src.models.task import TaskORM
from src.models.user_story import UserStory


def init_db():
    """Create all tables in the database."""
    try:
        print("🔍 Initializing database tables...")
        
        # Import models to register them with Base
        _ = [TaskORM, UserStory]
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully")
        print("   - user_stories")
        print("   - tasks")
        return 0
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(init_db())
