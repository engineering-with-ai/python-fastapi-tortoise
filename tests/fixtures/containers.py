"""Testcontainer fixtures with dynamic port allocation."""

import os
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass

from testcontainers.postgres import PostgresContainer


@dataclass(frozen=True)
class Container:
    """Connection info for a running testcontainer.

    Attributes:
        host: Container host (always localhost)
        port: Dynamic mapped port
        url: Pre-built connection URL
    """

    host: str
    port: int
    url: str


@contextmanager
def start_postgres(
    image: str = "postgres:15",
    password: str | None = None,
    username: str = "postgres",
    dbname: str = "postgres",
) -> Generator[Container]:
    """Start a Postgres container with dynamic port.

    Args:
        image: Docker image (postgres:15, timescale/timescaledb:latest-pg15, pgvector/pgvector:pg16)
        password: DB password. Defaults to POSTGRES_PASSWORD env var.
        username: Database username
        dbname: Database name

    Yields:
        Container with postgresql:// URL and dynamic port
    """
    password = password or os.environ["POSTGRES_PASSWORD"]
    with PostgresContainer(
        image, username=username, password=password, dbname=dbname
    ) as c:
        port = int(c.get_exposed_port(5432))
        yield Container(
            host="localhost",
            port=port,
            url=f"postgres://{username}:{password}@localhost:{port}/{dbname}",
        )
