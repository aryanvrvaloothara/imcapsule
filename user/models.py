from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    # recipe = relationship("Recipe", backref="user")
