"""
Create database tables based on the models defined in the application.

This code snippet creates the necessary database tables based on the models defined in the application.
The `engine` object represents the database connection, and the `Base` object serves as the declarative base for the models.
By calling the `create_all()` method on the `metadata` attribute of the `Base` class and passing the `engine` as the binding,
the database tables specified in the models (`User` and `Order`) are created.

Note: Make sure the database connection (`engine`) is properly configured and accessible before running this code.
"""



from database import engine, Base
from models import User, Order


Base.metadata.create_all(bind=engine)