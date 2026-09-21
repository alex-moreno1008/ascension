from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from .database import Base

from datetime import date


class ExerciseDB(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    muscle_group = Column(String, nullable=False)
    equipment = Column(String, nullable=True)

class WorkoutDB(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    workout_date = Column(
        Date,
        default=date.today,
        nullable=False,
    )
    

class WorkoutSetDB(Base):
    __tablename__ = "workout_sets"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)