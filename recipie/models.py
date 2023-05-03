from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(200))
    user_id = Column(Integer, ForeignKey('user.id'))

    # user = relationship("User", backref="recipe")
