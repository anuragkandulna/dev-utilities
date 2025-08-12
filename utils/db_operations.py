### utils/db_operations.py

from sqlalchemy.orm import Session
from sqlalchemy import text
from utils.my_logger import CustomLogger
from utils.timezone_utils import utc_now
from constants.constants import INFRA_LOG_FILE
from constants.config import LOG_LEVEL
import json


LOGGER = CustomLogger(__name__, level=LOG_LEVEL, log_file=INFRA_LOG_FILE).get_logger()


# SQL-based seeding functions
def seed_roles_sql(session: Session, predefined_roles: dict) -> None:
    """
    SQL-based seeding for user_roles table.
    """
    inserted_count = 0
    for rank, (role_name, permissions) in predefined_roles.items():
        rank = int(rank)
        
        # Check if role exists
        check_sql = text("SELECT 1 FROM user_roles WHERE rank = :rank")
        existing = session.execute(check_sql, {"rank": rank}).scalar()
        if existing:
            LOGGER.info(f"ℹ️ Role '{role_name}' already exists, skipping.")
            continue
        
        # Insert new role
        insert_sql = text("""
            INSERT INTO user_roles (rank, role, permissions) 
            VALUES (:rank, :role, :permissions)
        """)
        session.execute(insert_sql, {
            "rank": rank,
            "role": role_name,
            "permissions": json.dumps(permissions)
        })
        inserted_count += 1
    
    if inserted_count > 0:
        session.commit()
        LOGGER.info(f"✅ Seeded {inserted_count} new role(s) via SQL.")
    else:
        LOGGER.info("✅ No new roles inserted via SQL. All roles already exist.")
