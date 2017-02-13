"""
stuff
"""
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    restaurant_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item' # Table information

    # mapper
    menu_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
    restaurant = relationship(Restaurant)


class Employee(Base):
    __tablename__ = 'employee'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    address_id = Column(Integer, primary_key=True)
    street = Column(String(80), nullable=False)
    zip_code = Column(String(5), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    employee = relationship(Employee)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
