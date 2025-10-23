from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Ticket Management API",
    description="A sample REST API to manage support tickets",
    version="1.0.0",
)

# ---- Data Models ----
class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: str

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

# ---- In-memory storage ----
tickets = [
    Ticket(id=1, title="Sample ticket", description="This is a test ticket", status="open")
]

# ---- Endpoints ----
@app.get("/tickets", response_model=List[Ticket])
def get_tickets():
    """Get all tickets"""
    return tickets

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    """Get a ticket by ID"""
    ticket = next((t for t in tickets if t.id == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate):
    """Create a new ticket"""
    new_ticket = Ticket(
        id=len(tickets) + 1,
        title=ticket.title,
        description=ticket.description,
        status="open"
    )
    tickets.append(new_ticket)
    return new_ticket

@app.put("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket_data: TicketUpdate):
    """Update a ticket"""
    ticket = next((t for t in tickets if t.id == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket_data.title:
        ticket.title = ticket_data.title
    if ticket_data.description:
        ticket.description = ticket_data.description
    if ticket_data.status:
        ticket.status = ticket_data.status

    return ticket
