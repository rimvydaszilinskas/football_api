import pulp
from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status, Query, Body, HTTPException

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .constants import Positions
from .database import SessionLocal
from .models import Player, PlayerSchema, BestTeamInputSchema

app = FastAPI()

# Allow CORS
app.add_middleware(CORSMiddleware,
                   allow_origins=['localhost:3000', 'localhost:8000', '*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


def get_db():
    """
    Return a database connection
    """
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
    """
    Return a list of players

    Add q as query string to filter by name, nationality or club
    """
    data = db.query(Player)
    if q is not None:
        data = data.filter(
            or_(Player.name.contains(q), Player.nationality.contains(q),
                Player.club.contains(q)))
    return data.all()[skip:limit + skip]


@app.post('/', response_model=List[PlayerSchema])
async def testplayers(body: BestTeamInputSchema, db: Session = Depends(get_db)):
    """
    Return a list of best players up to an ammount

    Pass ammount inside request body
    """
    query = db.query(Player)
    all_players = query.all()

    players = [str(i.id) for i in all_players]
    points = {str(i.id): i.overall for i in all_players}
    cost = {str(i.id): i.value for i in all_players}

    # Setup data for each position
    gk = {str(i.id): 1 if i.position in Positions.Goalkeeper else 0 for i in all_players}
    hb = {str(i.id): 1 if i.position in Positions.Halfback else 0 for i in all_players}
    fb = {str(i.id): 1 if i.position in Positions.Fullback else 0 for i in all_players}
    fw = {str(i.id): 1 if i.position in Positions.Forward else 0 for i in all_players}

    prob = pulp.LpProblem('Football', pulp.LpMaximize)
    pvars = pulp.LpVariable.dicts("Players", players, 0, 1, pulp.LpBinary)
    
    # Define goal
    prob += pulp.lpSum([points[i] * pvars[i] for i in players]), 'Total cost'

    # Define constraints
    prob += pulp.lpSum([pvars[i] for i in players]) == 11, 'Total 11 players'
    prob += pulp.lpSum([cost[i] * pvars[i] for i in players]) <= body.ammount, 'Total cost'
    prob += pulp.lpSum([gk[i] * pvars[i] for i in players]) == 1, '1 GK'
    prob += pulp.lpSum([hb[i] * pvars[i] for i in players]) == 3, '2 HB'
    prob += pulp.lpSum([fb[i] * pvars[i] for i in players]) == 2, '3 FB'
    prob += pulp.lpSum([fw[i] * pvars[i] for i in players]) == 5, '3 FW'

    prob.solve()

    # If problem was not solved, return a 404
    if prob.status != 1:
        raise HTTPException(status_code=404, detail='Cannot form a team')
    
    # Only take IDs that are set to 1
    ids = [int(i.name.split('_')[1]) for i in prob.variables() if i.varValue == 1]
        
    return query.filter(Player.id.in_(ids)).all()
