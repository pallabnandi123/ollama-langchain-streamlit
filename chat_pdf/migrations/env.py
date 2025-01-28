from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from models import Base
from config import settings
import psycopg2

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Add this function to create the database if it doesn't exist
def create_database_if_not_exists(db_url):
    """
    Create the database if it does not already exist.
    """
    # Extract the database URL without the database name
    if db_url.startswith("postgresql://"):
        db_url = db_url[len("postgresql://") :]
    else:
        raise ValueError("DATABASE_URL must start with 'postgresql://'")

    db_url_parts = db_url.split("/", 1)
    if len(db_url_parts) == 1:
        raise ValueError("DATABASE_URL must include a database name")

    base_url = f"postgresql://{db_url_parts[0]}"
    database_name = db_url_parts[1]

    conn = None  # Initialize the connection variable

    # Connect to the PostgreSQL server
    try:
        conn = psycopg2.connect(base_url)
        conn.autocommit = True  # Allow creation of databases
        cursor = conn.cursor()

        # Create the database if it does not exist
        try:
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{database_name}' already exists.")
        finally:
            cursor.close()
    except Exception as e:
        print(f"Error connecting to PostgreSQL server: {e}")
    finally:
        if (
            conn
        ):  # Only attempt to close the connection if it was successfully established
            conn.close()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.SQLALCHEMY_DATABASE_URI or config.get_main_option("sqlalchemy.url")

    # This ensures the database is created if it doesn't exist
    create_database_if_not_exists(url)

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = settings.SQLALCHEMY_DATABASE_URI or config.get_main_option("sqlalchemy.url")
    
    # This ensures the database is created if it doesn't exist
    create_database_if_not_exists(url)
    
    # Get the current config section and overwrite the sqlalchemy.url
    config_section = config.get_section(config.config_ini_section, {})
    config_section['sqlalchemy.url'] = url  # Overwrite the URL

    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
