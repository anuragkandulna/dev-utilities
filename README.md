# dev-utilities

A collection of automation scripts and utilities for database management, environment setup, and development workflows.

## Overview

This repository contains reusable utilities and automation scripts that can be integrated into other applications for common development tasks like database setup, seeding, and environment configuration.

## Available Scripts & Utilities

### Database Management

-   **`bootstrap_database.sh`** - PostgreSQL database and user setup script
    -   Creates database users and databases
    -   Handles both local and container environments
    -   Supports dry-run mode for testing
-   **`seed.py`** - Database seeding utility
    -   Seeds initial data from JSON files
    -   Environment-aware (local vs container)
    -   Supports role seeding and other core system tables

### Environment Setup

-   **`setup_python_venv.sh`** - Python virtual environment setup
    -   Creates and configures Python virtual environments
    -   Installs dependencies from requirements.txt
    -   Cross-platform compatible

### Utility Modules (`utils/`)

-   **`psql_database.py`** - PostgreSQL connection and session management
-   **`db_operations.py`** - Database operation utilities
-   **`my_logger.py`** - Custom logging configuration
-   **`timezone_utils.py`** - Timezone handling utilities
-   **`timezone_verification.py`** - Timezone validation tools

## Quick Start

1. **Setup Environment:**

    ```bash
    ./setup_python_venv.sh
    ```

2. **Configure Database:**

    ```bash
    # Create .env file with database credentials
    cp .env.example .env

    # Bootstrap database (local environment)
    ./bootstrap_database.sh

    # Or run in dry-run mode
    ./bootstrap_database.sh --dry-run
    ```

3. **Seed Database:**
    ```bash
    python seed.py
    ```

## Requirements

-   Python 3.x
-   PostgreSQL
-   Bash shell (for shell scripts)

## Integration

These utilities can be imported and used in other Python applications:

```python
from utils.psql_database import get_database_session
from utils.my_logger import CustomLogger
from utils.db_operations import seed_roles_sql
```

## License

See [LICENSE](LICENSE) file for details.
