import os
import pytest
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory

from sqlalchemy.pool import NullPool
from sqlalchemy import text, create_engine
from package.app.models import Base
from package.app.models.base import DB_URL


def run_migrations(connection):
    config = Config("package/alembic.ini")
    config.set_main_option("script_location", "package/app/alembic")
    config.set_main_option("sqlalchemy.url", DB_URL)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(
        connection, opts={"target_metadata": Base.metadata, "fn": upgrade}
    )

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Run alembic migrations on test DB
    ROOT_DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_PORT"),
        "postgres",
    )
    my_engine = create_engine(
        ROOT_DB_URL,
        echo=True,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )  # connect to server
    with my_engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS test_db;"))  # create db
        conn.execute(text("CREATE DATABASE test_db;"))  # create db
    test_engine = create_engine(
        DB_URL,
        echo=True,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )
    with test_engine.connect() as conn:
        run_migrations(connection=conn)
    yield
