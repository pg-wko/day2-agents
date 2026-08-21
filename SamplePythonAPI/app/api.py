"""FastAPI routes for the SamplePythonAPI ticketing service.

The router exposes the REST endpoints used to create, list, query, update, and
remove support tickets. All handlers depend on a shared repository instance that
persists data in the configured DuckDB database.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.database import TicketNotFoundError, TicketRepository
from app.models import Ticket, TicketCreate, TicketFilters, TicketPriority, TicketStatus, TicketUpdate


def create_api_router(repository: TicketRepository) -> APIRouter:
    """Create and configure the application router for ticket operations.

    Args:
        repository: Shared repository instance used by the HTTP handlers.

    Returns:
        An APIRouter mounted at the ``/api`` prefix with ticket endpoints.
    """
    router = APIRouter(prefix="/api", tags=["tickets"])

    def get_repository() -> TicketRepository:
        """Return the repository bound to the current application instance."""
        return repository

    @router.get("/tickets", response_model=list[Ticket])
    def list_tickets(
        status_filter: TicketStatus | None = Query(default=None, alias="status"),
        priority: TicketPriority | None = None,
        search: str | None = None,
        tickets: TicketRepository = Depends(get_repository),
    ) -> list[Ticket]:
        """Return all tickets that match the optional status, priority, and search filters."""
        return tickets.list(TicketFilters(status=status_filter, priority=priority, search=search))

    @router.post("/tickets", response_model=Ticket, status_code=status.HTTP_201_CREATED)
    def create_ticket(ticket: TicketCreate, tickets: TicketRepository = Depends(get_repository)) -> Ticket:
        """Create a new ticket and return the stored record."""
        return tickets.create(ticket)

    @router.get("/tickets/{ticket_id}", response_model=Ticket)
    def get_ticket(ticket_id: int, tickets: TicketRepository = Depends(get_repository)) -> Ticket:
        """Return a single ticket by identifier or raise a 404 error when it is absent."""
        try:
            return tickets.get(ticket_id)
        except TicketNotFoundError as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    @router.patch("/tickets/{ticket_id}", response_model=Ticket)
    def update_ticket(
        ticket_id: int,
        update: TicketUpdate,
        tickets: TicketRepository = Depends(get_repository),
    ) -> Ticket:
        """Apply a partial update to an existing ticket and return the refreshed record."""
        try:
            return tickets.update(ticket_id, update)
        except TicketNotFoundError as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    @router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_ticket(ticket_id: int, tickets: TicketRepository = Depends(get_repository)) -> Response:
        """Delete a ticket by id and return an empty 204 response when the delete succeeds."""
        try:
            tickets.delete(ticket_id)
        except TicketNotFoundError as error:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
