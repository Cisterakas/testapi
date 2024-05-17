from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import jwt
from db import get_db
import datetime
from pydantic import BaseModel
from jwt import PyJWTError, decode
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

import os
# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env file

AuthRouter = APIRouter(tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    return token

class User(BaseModel):
    username: str
    password: str
    
class AccountNotApprovedError(Exception):
    pass

@AuthRouter.post("/login")
async def login(user: User, response: Response, db=Depends(get_db)):
    query = "SELECT user_id, first_name FROM user WHERE email = %s AND password = %s"
    cursor = db[0].cursor()
    cursor.execute(query, (user.username, user.password))
    account = cursor.fetchone()

    if account:
        user_id = account[0]
        # Check account approval status (handle missing data)
        approval_query = "SELECT approved FROM account_approval WHERE user_id = %s"
        cursor.execute(approval_query, (user_id,))
        approval_status = cursor.fetchone()

        if approval_status and approval_status[0] == "TRUE":
            # Check if the user is an administrator
            admin_query = "SELECT role FROM administrator WHERE user_id = %s"
            cursor.execute(admin_query, (user_id,))
            admin_role = cursor.fetchone()

            # Check if the user is a student
            student_query = "SELECT user_id FROM student WHERE user_id = %s"
            cursor.execute(student_query, (user_id,))
            student_role = cursor.fetchone()

            # Proceed with token generation and login (approved account)
            token_data = {
                "username": user.username,
                "account_id": account[0],
                "first_name": account[1],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(
                key="access_token", value=token, httponly=True, samesite="None", secure=True
            )
            print("Cookie set successfully")

            if admin_role:
                if admin_role[0] == "Super Admin":
                    return {"message": "Logged in", "role": "super_admin"}
                else:
                    return {"message": "Logged in", "role": "admin"}
            elif student_role:
                return {"message": "Logged in", "role": "student"}
            else:
                return {"message": "Logged in"}
        else:
            # Account not approved
            print(f"Account not approved for user {user.username}")  # Added for debugging
            raise HTTPException(status_code=403, detail="Account not approved")
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

@AuthRouter.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", samesite="None", secure=True)
    return {"message": "Logged out"}

@AuthRouter.get("/auth/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        if token.startswith('b\''):
            token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        accountid: int = payload.get("account_id")
        first_name: str = payload.get("first_name")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "accountid": accountid, "first_name": first_name}
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

@AuthRouter.get("/authenticate")
async def authenticate(token: str = Depends(oauth2_scheme)):
    if token:
        return {"message": "Authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Unauthenticated")

# @AuthRouter.post("/login")
# async def login(user: User, response: Response, db=Depends(get_db)):
#     query = "SELECT user_id, first_name FROM user WHERE email = %s AND password = %s"
#     cursor = db[0].cursor()
#     cursor.execute(query, (user.username, user.password))
#     account = cursor.fetchone()

#     if account:
#         user_id = account[0]
#         # Check account approval status (handle missing data)
#         approval_query = "SELECT approved FROM account_approval WHERE user_id = %s"
#         cursor.execute(approval_query, (user_id,))
#         approval_status = cursor.fetchone()

#         if approval_status:  # Check if data exists
#             if approval_status[0] == "TRUE":
#                 # Check if the user is an administrator
#                 admin_query = "SELECT role FROM administrator WHERE user_id = %s"
#                 cursor.execute(admin_query, (user_id,))
#                 admin_role = cursor.fetchone()

#                 # Check if the user is a student
#                 student_query = "SELECT user_id FROM student WHERE user_id = %s"
#                 cursor.execute(student_query, (user_id,))
#                 student_role = cursor.fetchone()

#                 # Proceed with token generation and login (approved account)
#                 token_data = {
#                     "username": user.username,
#                     "account_id": account[0],
#                     "first_name": account[1],
#                     "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
#                 }
#                 token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
#                 response.set_cookie(
#                     key="access_token", value=token, httponly=True, samesite="none", secure=True
#                 )
#                 print("Cookie set successfully")

#                 if admin_role:
#                     return {"message": "Logged in", "role": "admin"}
#                 elif student_role:
#                     return {"message": "Logged in", "role": "student"}
#                 else:
#                     return {"message": "Logged in"}

#             else:
#                 # Account not approved
#                 print(f"Account not approved for user {user.username}")  # Added for debugging
#                 raise HTTPException(status_code=403, detail="Account not approved")
#         else:
#             # Account data not found in approval table (likely not approved yet)
#             print(f"Account approval data not found for user {user.username}")  # Added for debugging
#             raise HTTPException(status_code=403, detail="Account not approved")
#     else:
#         raise HTTPException(status_code=400, detail="Invalid credentials")


# @AuthRouter.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("access_token")
#     return {"message": "Logged out"}

# @AuthRouter.get("/auth/me")
# async def read_users_me(token: str = Depends(oauth2_scheme)):
#     try:
#         if token.startswith('b\''):
#           token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("username")
#         accountid: int = payload.get("account_id")
#         first_name: str = payload.get("first_name")
#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         return {"username": username, "accountid": accountid, "first_name": first_name}
#     except PyJWTError as exc:   
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         ) from exc


# @AuthRouter.get("/authenticate")
# async def authenticate(token: str = Depends(oauth2_scheme)):
    if token:
        return {"message": "Authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Unauthenticated")