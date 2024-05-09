

import json
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from db import get_db
# from websocket import manager

AllUsersRouter = APIRouter(tags=["All Users"])

@AllUsersRouter.get("/all/users")
async def read_users(db=Depends(get_db)):
    query = "SELECT user_id, first_name, last_name FROM user"
    cursor = db[0].cursor()
    cursor.execute(query)
    accounts = [{
                    "AccountID": accounts[0],
                    "FirstName": accounts[1],
                    "LastName": accounts[2],
                } for accounts in cursor.fetchall()
                ]
    return accounts

# @AllUsersRouter.post("/register")
# async def create_user(
#     Email: str = Body(...),
#     FirstName: str = Body(...),
#     LastName: str = Body(...),
#     password: str = Body(...),
#     db=Depends(get_db),
# ):

#     query = "INSERT INTO user (first_name, last_name, password, email) VALUES (%s, %s, %s, %s)"
#     cursor = db[0].cursor()
#     cursor.execute(
#         query, (FirstName, LastName, password, Email)
#     )

#     cursor.execute("SELECT LAST_INSERT_ID()")
#     cursor.fetchone()[0]
#     cursor.execute("COMMIT")
    
#     new_user = {
#         "FirstName": FirstName,
#         "LastName": LastName,
#         "Password": password, 
#         "Email": Email,
#     }

#     await manager.broadcast(json.dumps(new_user))
    
#     return new_user
