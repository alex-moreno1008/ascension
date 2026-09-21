from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Ascension")


class Exercise(BaseModel):
    name: str
    muscle_group: str
    equipment: Optional[str] = None


exercises = []


@app.get("/")
def read_root():
    return {"message": "Welcome to Ascension"}


@app.post("/exercises")
def create_exercise(exercise: Exercise):
    new_exercise = {
        "id": len(exercises) + 1,
        **exercise.model_dump(),
    }

    exercises.append(new_exercise)

    return new_exercise


@app.get("/exercises")
def get_exercises():
    return exercises

@app.get("/exercises/{exercise_id}")
def get_exercise(exercise_id: int):
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise

    raise HTTPException(
        status_code=404,
        detail="Exercise not found",
    )