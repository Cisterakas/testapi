from fastapi import Depends, HTTPException, APIRouter, Form
import bcrypt
from .db import get_db


UserRouter = APIRouter(tags=["Users"])

# CRUD operations

@UserRouter.get("/users/", response_model=list)
async def read_users(
    db=Depends(get_db)
):
    query = "SELECT user_id, first_name, middle_name, last_name, suffix, email, password FROM user"
    db[0].execute(query)
    users = [{"user_id": user[0], "first_name": user[1], "middle_name": user[2], "last_name": user[3], "suffix": user[4], "email": user[5], "password":user[6]} for user in db[0].fetchall()]
    return users

@UserRouter.get("/users/{user_id}", response_model=dict)
async def read_user(
    user_id: int, 
    db=Depends(get_db)
):
    query = "SELECT user_id, first_name, middle_name, last_name, suffix, email FROM user WHERE user_id = %s"
    db[0].execute(query, (user_id,))
    user = db[0].fetchone()
    if user:
        return {"user_id": user[0], "first_name": user[1], "middle_name": user[2], "last_name": user[3], "suffix": user[4], "email": user[5]}
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.post("/users/", response_model=dict)
async def create_user(
    first_name: str = Form(...), 
    middle_name: str = Form(None), 
    last_name: str = Form(...), 
    suffix: str = Form(None), 
    email: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(password)

    query = "INSERT INTO user (first_name, middle_name, last_name, suffix, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    db[0].execute(query, (first_name, middle_name, last_name, suffix, email, hashed_password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"user_id": new_user_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, "suffix": suffix, "email": email}

@UserRouter.put("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    first_name: str = Form(...),
    middle_name: str = Form(None),
    last_name: str = Form(...),
    suffix: str = Form(None),
    email: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(password)

    # Update user information in the database 
    query = "UPDATE user SET first_name = %s, middle_name = %s, last_name = %s, suffix = %s, email = %s, password = %s WHERE user_id = %s"
    db[0].execute(query, (first_name, middle_name, last_name, suffix, email, hashed_password, user_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT user_id FROM user WHERE user_id = %s"
        db[0].execute(query_check_user, (user_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM user WHERE user_id = %s"
        db[0].execute(query_delete_user, (user_id,))
        db[1].commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") from e
    finally:
        # Close the database cursor
        db[0].close()

# Password hashing function using bcrypt
def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string for storage
