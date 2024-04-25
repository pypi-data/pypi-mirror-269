import os
from contextlib import ExitStack

import pytest
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from package.app.models import Base, get_db_session
from package.app.models.base import DatabaseSessionManager
from package.app.main import app as actual_app
from psycopg.connection_async import AsyncConnection as Connection

from fastapi.testclient import TestClient
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from sqlalchemy import text

DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_HOST"),
    os.getenv("POSTGRES_PORT"),
    "test_db",
)


@pytest.fixture(autouse=True)
def app(event_loop):
    with ExitStack():
        yield actual_app


@pytest.fixture
def client(event_loop, app):
    with TestClient(app) as c:
        yield c


def run_migrations(connection: Connection):
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


@pytest.fixture(scope="function")
async def sessionmanager():
    yield DatabaseSessionManager(DB_URL, {"poolclass": NullPool})


@pytest.fixture(scope="function", autouse=True)
async def setup_database(sessionmanager):
    # Run alembic migrations on test DB
    ROOT_DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_PORT"),
        "postgres",
    )
    my_engine = create_async_engine(
        ROOT_DB_URL,
        echo=True,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )  # connect to server
    async with my_engine.connect() as conn:
        await conn.execute(text("DROP DATABASE IF EXISTS test_db;"))  # create db
        await conn.execute(text("CREATE DATABASE test_db;"))  # create db
    async with sessionmanager.connect() as connection:
        await connection.run_sync(run_migrations)

    yield

    # Teardown
    await sessionmanager.close()


# Each test function is a clean slate
@pytest.fixture(scope="function", autouse=True)
async def transactional_session(sessionmanager):
    async with sessionmanager.session() as session:
        try:
            session.autoflush = True
            yield session
        finally:
            await session.rollback()  # Rolls back the outer transaction


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, sessionmanager):
    async def get_db_session_override():
        async with sessionmanager.session() as session:
            try:
                session.autoflush = True
                yield session
            finally:
                await session.rollback()  # Rolls back the outer transaction

    app.dependency_overrides[get_db_session] = get_db_session_override
