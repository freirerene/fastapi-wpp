from __future__ import annotations
import uvicorn
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import os

from etl import ETL

import crud
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Profile(BaseModel):
    name: str


class Contact(BaseModel):
    profile: Profile
    wa_id: str


class Text(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(..., alias='from')
    id: str
    timestamp: str
    text: Text
    type: str


class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: List[Contact]
    messages: List[Message]


class Change(BaseModel):
    value: Value
    field: str


class EntryItem(BaseModel):
    id: str
    changes: List[Change]


class Model(BaseModel):
    object: str
    entry: List[EntryItem]


@app.get("/webhook")
async def verify_token(
        verify_token: Optional[str] = Query(
            None, alias="hub.verify_token"),
        challenge: Optional[str] = Query(
            None, alias="hub.challenge"),
        mode: Optional[str] = Query(
            "subscribe", alias="hub.mode"),
) -> Optional[str]:
    token = os.environ['TOKEN']

    if verify_token == token and mode == "subscribe":
        return JSONResponse(content=int(challenge))
    else:
        raise HTTPException(status_code=403, detail='Token invalid')


@app.post("/webhook")
async def get_body(model: Model, db: Session = Depends(get_db)):
    contact = model.entry[0].changes[0].value.contacts[0].wa_id
    msg = model.entry[0].changes[0].value.messages[0].text.body
    time = model.entry[0].changes[0].value.messages[0].timestamp

    time = int(time)

    x = ETL(contact, msg, time)
    x.proccess()

    if x.type == 'fixo':
        return crud.create_fixed(db=db,
                                 owner=x.contact,
                                 where=x.where,
                                 value=x.val,
                                 category=x.categoria
                                 )

    else:
        today = datetime.fromtimestamp(time).strftime('%F')

        return crud.create_var(db=db,
                               owner=x.contact,
                               date=today,
                               value=x.val,
                               category=x.categoria
                               )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=443,
                ssl_keyfile=os.environ['PATH_PRIVATKEY'],
                ssl_certfile=os.environ['PATH_CERTFILE'])
