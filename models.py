from sqlalchemy import Column, Integer, String, Float, DateTime

from database import Base


class Fixed(Base):
    __tablename__ = "fixed"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String)
    value_first = Column(Float)
    value_second = Column(Float)
    category = Column(String)


class Var(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String)
    month = Column(DateTime)
    val_first = Column(Float)
    val_second = Column(Float)


class VarDetailed(Base):
    __tablename__ = "variable_detailed"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String)
    date = Column(DateTime)
    val = Column(Float)
    category = Column(String)

