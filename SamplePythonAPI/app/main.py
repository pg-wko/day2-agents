"""Runtime entry point for the SamplePythonAPI ticketing system.

The application assembles the FastAPI service, binds it to a repository-backed
REST API, mounts the NiceGUI dashboard, and exposes a health endpoint used by
monitoring and local development.
"""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from nicegui import app as nicegui_app, ui
import uvicorn

from app.api import create_api_router
from app.database import TicketRepository
from app.ui import mount_ui


def create_app(database_path: str | None = None, seed: bool = True) -> FastAPI:
    """Build the FastAPI app and attach the repository-backed dashboard and routes.

    Args:
        database_path: Optional database path override. Defaults to the environment
            value ``TICKET_DB_PATH`` or ``data/tickets.duckdb``.
        seed: Whether to populate the database with default demo tickets.

    Returns:
        A configured FastAPI application with the JSON API and NiceGUI UI mounted.
    """
    repository = TicketRepository(database_path or os.getenv("TICKET_DB_PATH", "data/tickets.duckdb"))
    if seed:
        repository.seed_defaults()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        """Ensure the repository closes cleanly when the application shuts down."""
        try:
            yield
        finally:
            repository.close()

    app = FastAPI(title="Ticketing System", version="0.1.0", lifespan=lifespan)
    app.include_router(create_api_router(repository))

    @app.get("/health")
    def health() -> dict[str, str]:
        """Return the service health payload used by health-check systems."""
        return {"status": "ok"}

    mount_ui(repository)
    ui.run_with(app, title="Ticketing System", favicon="T", storage_secret=os.getenv("NICEGUI_SECRET", "dev-secret"))
    return app


app = create_app()


if __name__ in {"__main__", "__mp_main__"}:
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT", "8000")))
