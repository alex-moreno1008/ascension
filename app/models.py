from sqlalchemy import Column, Integer, String

from .database import Base


class ExerciseDB(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    muscle_group = Column(String, nullable=False)
    equipment = Column(String, nullable=True)