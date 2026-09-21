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

class WorkoutCreate(BaseModel):
    name: str

class WorkoutSetCreate(BaseModel):
    exercise_id: int
    set_number: int
    reps: int
    weight: float



@app.get("/")
def read_root():
    return {"message": "Welcome to Ascension"}

@app.post("/workouts")
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
):
    db_workout = models.WorkoutDB(
        name=workout.name,
    )

    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    return {
        "id": db_workout.id,
        "name": db_workout.name,
        "workout_date": db_workout.workout_date,
    }

@app.get("/workouts")
def get_workouts(db: Session = Depends(get_db)):
    workouts = db.query(models.WorkoutDB).all()

    return[{
        "id": workout.id,
        "name": workout.name,
        "workoutdate": workout.workout_date,
    }
    for workout in workouts
]

@app.get("/workouts/{workout_id}")
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
):
    workout = (
        db.query(models.WorkoutDB)
        .filter(models.WorkoutDB.id == workout_id)
        .first()
    )

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found",
        )

    return {
        "id": workout.id,
        "name": workout.name,
        "workout_date": workout.workout_date,
    }

@app.post("/workouts/{workout_id}/sets")
def create_workout_set(
    workout_id: int,
    workout_set: WorkoutSetCreate,
    db: Session = Depends(get_db),
):
    db_workout_set = models.WorkoutSetDB(
        workout_id=workout_id,
        exercise_id=workout_set.exercise_id,
        set_number=workout_set.set_number,
        reps=workout_set.reps,
        weight=workout_set.weight,
    )

    db.add(db_workout_set)
    db.commit()
    db.refresh(db_workout_set)

    return {
        "id": db_workout_set.id,
        "workout_id": db_workout_set.workout_id,
        "exercise_id": db_workout_set.exercise_id,
        "set_number": db_workout_set.set_number,
        "reps": db_workout_set.reps,
        "weight": db_workout_set.weight,
    }


@app.get("/workouts/{workout_id}/sets")
def get_workout_sets(
    workout_id: int,
    db: Session = Depends(get_db),
):
    workout_sets = (
        db.query(models.WorkoutSetDB)
        .filter(models.WorkoutSetDB.workout_id == workout_id)
        .all()
    )

    return [
        {
            "id": workout_set.id,
            "workout_id": workout_set.workout_id,
            "exercise_id": workout_set.exercise_id,
            "set_number": workout_set.set_number,
            "reps": workout_set.reps,
            "weight": workout_set.weight,
        }
        for workout_set in workout_sets
    ]


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