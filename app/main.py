from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import Base, engine, get_db

app = FastAPI(title="Ascension")
Base.metadata.create_all(bind=engine)


class Exercise(BaseModel):
    name: str
    muscle_group: str
    equipment: Optional[str] = None




@app.get("/")
def read_root():
    return {"message": "Welcome to Ascension"}


@app.post("/exercises")
def create_exercise(
    exercise: Exercise,
    db: Session = Depends(get_db),
):
    db_exercise = models.ExerciseDB(
        name=exercise.name,
        muscle_group=exercise.muscle_group,
        equipment=exercise.equipment,
    )

    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    return {
        "id": db_exercise.id,
        "name": db_exercise.name,
        "muscle_group": db_exercise.muscle_group,
        "equipment": db_exercise.equipment,
    }


@app.get("/exercises")
def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(models.ExerciseDB).all()

    return [
        {
            "id": exercise.id,
            "name": exercise.name,
            "muscle_group": exercise.muscle_group,
            "equipment": exercise.equipment,
        }
        for exercise in exercises
    ]


@app.get("/exercises/{exercise_id}")
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
):
    exercise = (
        db.query(models.ExerciseDB)
        .filter(models.ExerciseDB.id == exercise_id)
        .first()
    )

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found",
        )

    return {
        "id": exercise.id,
        "name": exercise.name,
        "muscle_group": exercise.muscle_group,
        "equipment": exercise.equipment,
    }