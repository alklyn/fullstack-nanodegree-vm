"""
stuff
"""
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id')) # The user that added it
    user = relationship(User)

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format.
        """
        data = {
            "id": self.id,
            "name": self.name
        }
        return data


class MenuItem(Base):
    __tablename__ = 'menu_item' # Table information

    # mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.id')) # The user that added it
    user = relationship(User)

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format.
        """
        data = {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "price": self.price,
            "course": self.course
        }
        return data


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street = Column(String(80), nullable=False)
    zip_code = Column(String(5), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship(Employee)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
