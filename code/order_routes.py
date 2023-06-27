from fastapi import APIRouter, Depends, status
"""
Importing APIRouter class from FastAPI for creating a router to group related endpoints.
Importing Depends function from FastAPI to declare dependencies for an endpoint.
Importing status module from FastAPI for providing HTTP status codes for responses.
"""
from fastapi_jwt_auth import AuthJWT
"""
Importing AuthJWT class from the fastapi_jwt_auth package to provide JWT authentication support for FastAPI.
"""
from models import User, Order
"""
Importing User and Order classes from the models module.
These classes represent the data models for users and orders in the application.
"""
from schemas import OrderModel, OrderStatusModel #12
"""
Importing OrderModel and OrderStatusModel classes from the schemas module.
These classes define the schemas for the request and response data structures related to orders.
"""
from fastapi.exceptions import HTTPException
"""
Importing HTTPException class from FastAPI for raising HTTP exceptions with specific status codes and error messages.
"""
from database import Session, engine
"""
Importing Session class and engine object from the database module.
These are used for managing the database session and connecting to the database.
"""
from fastapi.encoders import jsonable_encoder
"""
Importing jsonable_encoder function from FastAPI for converting complex objects into JSON-compatible data.
"""

order_router=APIRouter(
    prefix='/orders',
    tags=['order']
)

session=Session(bind=engine)

@order_router.get('/')
async def hello(Authourize:AuthJWT=Depends()):
    """
    Endpoint: /orders/
    Method: GET
    Description: Returns a greeting message.
    Requires authentication.
    """
    
    try:
        Authourize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return {"message":"Hello World"}

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel, Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/order
    Method: POST
    Description: Places an order.
    Requires authentication.
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()


    new_order=Order(
        bag_size=order.bag_size,
        quantity=order.quantity
    )

    new_order.user=user

    session.add(new_order)

    session.commit()



    response={
        "bag_size":new_order.bag_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)



#7 fr
@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/orders
    Method: GET
    Description: Lists all orders.
    Requires authentication and staff privileges.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders=session.query(Order).all()

        return jsonable_encoder(orders)
   
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )


#8

@order_router.get('/orders/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/orders/{id}
    Method: GET
    Description: Retrieves an order by ID.
    Requires authentication and staff privileges.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request"
        )

#9

@order_router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/user/orders
    Method: GET
    Description: Retrieves orders of the authenticated user.
    Requires authentication.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)

#10

@order_router.get('/user/order/{id}/',)
async def get_specific_order(id:int,Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/user/order/{id}
    Method: GET
    Description: Retrieves a specific order of the authenticated user by ID.
    Requires authentication.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    subject=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject).first()

    orders=current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )
    

#11
@order_router.put('/order/update/{id}/')
async def update_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/order/update/{id}
    Method: PUT
    Description: Updates an order by ID.
    Requires authentication.
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    order_to_update=session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity=order.quantity
    order_to_update.bag_size=order.bag_size

    session.commit()

    response={
            "id":order_to_update.id,
            "quantity":order_to_update.quantity,
            "bag_size":order_to_update.bag_size,
            "order_status":order_to_update.order_status,
        }

    return jsonable_encoder(order_to_update)

#12
@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int, order:OrderStatusModel, Authorize:AuthJWT=Depends()):
    """
    Endpoint: /orders/order/update/{id}
    Method: PATCH
    Description: Updates the order status by ID.
    Requires authentication and staff privileges.
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    username=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order.order_status

        session.commit()

        response={
            "id":order_to_update.id,
            "quantity":order_to_update.quantity,
            "bag_size":order_to_update.bag_size,
            "order_status":order_to_update.order_status,
        }

        return jsonable_encoder(response)
    

#13 
@order_router.delete('/order/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int, Authorize: AuthJWT=Depends()):
    """
    Endpoint: /orders/order/delete/{id}
    Method: DELETE
    Description: Deletes an order by ID.
    Requires authentication.
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    order_to_delete=session.query(Order).filter(Order.id==id).first()

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete