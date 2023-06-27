from database import Base
"""
Import the `Base` object from the `database` module.

The `Base` object serves as the base class for all declarative SQLAlchemy models in the application.
"""
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey #CheckConstraint, BigInteger
"""
Import specific objects (`Column`, `Integer`, `Boolean`, `Text`, `String`, `ForeignKey`) from the `sqlalchemy` module.
- `ForeignKey` represents a foreign key constraint.
"""
from sqlalchemy.orm import relationship
"""
Import the `relationship` object from the `sqlalchemy.orm` module.

The `relationship` object is used to define relationships between SQLAlchemy models.
"""
from sqlalchemy_utils.types import ChoiceType
"""
Import the `ChoiceType` object from the `sqlalchemy_utils.types` module.

The `ChoiceType` object provides a way to store choices as string values in the database.
"""

class User(Base):
    """
    Represents a user in the system.
    """

    __tablename__='user'
    id=Column(Integer, primary_key=True)
    username=Column(String(20), unique=True)
    email=Column(String(50), unique=True)
    password=Column(Text, nullable=True)
    first_name=Column(String(20), nullable=True)
    last_name=Column(String(20), nullable=True)
    address=Column(String(300))
    phone=Column(String(30), unique=True)
    is_staff=Column(Boolean, default=False)
    is_active=Column(Boolean, default=False)
    orders=relationship('Order',back_populates='user')

    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f"<User {self.username}"
    

class Order(Base):
    """
    Represents an order in the system.
    """

    ORDER_STATUS=(
        ('PENDING','pending'),
        ('IN-TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered')
    )

    BAG_SIZES=(
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('GIGANTIC','gigantic')
    )

    __tablename__='orders'
    id=Column(Integer, primary_key=True)
    quantity=Column(Integer, nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUS),default="PENDING")
    bag_size=Column(ChoiceType(choices=BAG_SIZES),default="SMALL")
    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('User', back_populates='orders')

    def __repr__(self):
        """
        Returns a string representation of the Order object.
        """
        return f"<Order {self.id}>"
    
