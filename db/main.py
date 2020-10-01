from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status, Query, Body
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .constants import Positions
from .database import SessionLocal
from .models import Player, PlayerSchema, BestTeamInputSchema

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['localhost:3000', 'localhost:8000', '*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', response_model=List[PlayerSchema])
async def players(db: Session = Depends(get_db),
                  q: Optional[str] = Query(None,
                                           description='Searchable keyword'),
                  skip: Optional[int] = Query(0),
                  limit: Optional[int] = Query(100)):
    data = db.query(Player)
    if q is not None:
        data = data.filter(
            or_(Player.name.contains(q), Player.nationality.contains(q),
                Player.club.contains(q)))
    return data.all()[skip:limit + skip]


@app.post('/')
async def best_team(data: BestTeamInputSchema, db: Session = Depends(get_db)):
    avg = data.ammount / 11

    best_players = []

    for position in Positions.INFO:
        seen = []
        for i in range(Positions.INFO[position]):
            players = db.query(Player).filter(
                Player.value <= avg, Player.id.notin_(seen),
                Player.position.in_(getattr(Positions, position))).order_by(
                    Player.overall.desc()).all()

            if len(players) == 0:
                return JSONResponse({'detail': 'Not found'},
                                    status_code=status.HTTP_404_NOT_FOUND)
            best_players.append(players[0])
            seen.append(players[0].id)
    return best_players
