import os
from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func
from sqlmodel import Session, select
from server.db_session import get_session
from .models import (
    EventCreateSchema,
    EventListSchema,
    EventModel,
    EventUpdateSchema,
    get_utc_now,
)

router = APIRouter()


# SEND DATA HERE
# create view
# POST /api/events/
@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()  # convert payload to dictionary
    obj = EventModel.model_validate(data)  # validate the dictionary
    session.add(obj)  # add the object to the session
    session.commit()  # commit the session
    session.refresh(obj)  # refresh the object
    return obj


# GET /api/events/12
@router.get("/", response_model=EventListSchema)
def get_events(session: Session = Depends(get_session)):
    query = select(EventModel).order_by(EventModel.updated_at.desc()).limit(10)
    # results = session.exec(query).all()
    results = session.exec(query).fetchall()  # fetch all the results
    return {
        "results": results,
        "count": len(results),
    }


# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: UUID, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)  # select the event
    result = session.exec(query).first()  # get the first result
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


# UPDATE /api/events/12
@router.put("/{event_id}", response_model=EventModel)
def update_event(
    event_id: UUID, payload: EventUpdateSchema, session: Session = Depends(get_session)
):

    result = get_event(event_id, session) # Get the event to update

    data = payload.model_dump(exclude_unset=True)  # only update provided fields
    for key, value in data.items():
        setattr(result, key, value)  # set the attribute
    result.updated_at = get_utc_now()
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


# DELETE /api/events/12
@router.delete("/{event_id}", response_model=EventModel)
def delete_event(event_id: UUID, session: Session = Depends(get_session)):

    result = get_event(event_id, session)  # get the event to delete
    session.delete(result)
    session.commit()
    return result
