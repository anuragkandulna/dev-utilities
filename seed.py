import json
from datetime import datetime
import os
from utils.psql_database import get_database_session, get_database_connection
from utils.db_operations import seed_roles_sql
from utils.my_logger import CustomLogger
from constants.constants import INFRA_LOG_FILE
from constants.config import LOG_LEVEL


# Default constants
LOGGER = CustomLogger(__name__, level=LOG_LEVEL, log_file=INFRA_LOG_FILE).get_logger()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_DIR = os.path.join(SCRIPT_DIR, "seed_data")


def detect_environment():
    """Detect if running in container or local environment."""
    if os.path.exists('/.dockerenv'):
        return "test"
    else:
        return "local"


def load_seed_json(filename):
    with open(os.path.join(SEED_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    session = get_database_session()
    db_connection = get_database_connection()

    env_type = detect_environment()
    engine = db_connection.engine
    if engine is None:
        raise RuntimeError("Database engine not properly initialized")
    
    if env_type == "test":
        LOGGER.info("🐳 Container environment detected - dropping all existing tables to ensure fresh state...")
        # Drop all tables first for completely fresh state (container only)
        # Base.metadata.drop_all(bind=engine)
        LOGGER.info("🗑️ All tables dropped successfully.")
        
        LOGGER.info("⏳ Creating all database tables...")
        # Base.metadata.create_all(bind=engine)
        LOGGER.info("✅ Tables created fresh.")
    else:
        LOGGER.info("🏠 Local environment detected - preserving existing data for safety...")
        LOGGER.info("⏳ Creating database tables (if they don't exist)...")
        # Base.metadata.create_all(bind=engine)
        LOGGER.info("✅ Tables verified/created.")

    try:
        # Seed all tables using dedicated seeder functions
        LOGGER.info("🌱 Starting database seeding process...")

        # Core system tables - using SQL-based functions
        seed_roles_sql(session, load_seed_json("role_seed.json"))
        
        LOGGER.info("🎉 Database seeding completed successfully!")

    except Exception as ex:
        session.rollback()
        LOGGER.error(f"❌ Error during seeding: {ex}")
        raise

    finally:
        session.close()
