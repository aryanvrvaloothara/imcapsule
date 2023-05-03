from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base


class Wishlist(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))

    recipe = relationship('Recipe', backref=backref('wishlists'))
    user = relationship('User', backref=backref('wishlists'))
