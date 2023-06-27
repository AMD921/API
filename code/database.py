from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine('postgresql://postgres:1887@localhost/pashmak',
    echo=True
)
"""
Create a SQLAlchemy engine object for connecting to the PostgreSQL database.

The engine object represents the database connection and is created using the `create_engine` function.
The connection string specifies the database dialect, username, password, host, and database name.
In this case, it connects to a PostgreSQL database running on the localhost with the specified credentials.
The `echo=True` parameter enables verbose logging of database interactions for debugging purposes.
Make sure to modify the connection string with the appropriate values for your database setup.
"""

Base = declarative_base()
"""
Create a declarative base class for defining SQLAlchemy models.

The `declarative_base` function returns a base class from which all declarative models inherit.
This base class provides a set of common functionality and features required for SQLAlchemy models.
By assigning the returned base class to the `Base` variable, it becomes the base class for all models in the application.
"""

Session = sessionmaker() 
"""
Create a session factory for creating database sessions.

The `sessionmaker` function returns a session class that acts as a factory for creating individual sessions.
By assigning the returned session class to the `Session` variable, it becomes the session factory for the application.
The session factory can be used to create sessions for database interactions.
"""
