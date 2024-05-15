# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db
# from datetime import date

# DocumentRequestRouter = APIRouter(tags=["Document Request"])

# @DocumentRequestRouter.get("/document_requests/", response_model=list)
# async def read_document_requests(
#     db=Depends(get_db)
# ):
#     query = "SELECT request_id, user_id, request_date, status, id_link FROM document_request"
#     db[0].execute(query)
#     document_requests = [{
#         "request_id": request[0], "user_id": request[1], "request_date": request[2], 
#         "status": request[3], "id_link": request[4]
#     } for request in db[0].fetchall()]
#     return document_requests

# @DocumentRequestRouter.get("/document_requests/{request_id}", response_model=dict)
# async def read_document_request(
#     request_id: int, 
#     db=Depends(get_db)
# ):
#     query = "SELECT request_id, user_id, request_date, status, id_link FROM document_request WHERE request_id = %s"
#     db[0].execute(query, (request_id,))
#     document_request = db[0].fetchone()
#     if document_request:
#         return {
#             "request_id": document_request[0], "user_id": document_request[1], 
#             "request_date": document_request[2], "status": document_request[3], 
#             "id_link": document_request[4]
#         }
#     raise HTTPException(status_code=404, detail="Document request not found")

# @DocumentRequestRouter.post("/document_requests/", response_model=dict)
# async def create_document_request(
#     user_id: int, 
#     request_date: date,
#     status: str,
#     id_link: str,
#     db=Depends(get_db)
# ):
#     query = "INSERT INTO document_request (user_id, request_date, status, id_link) VALUES (%s, %s, %s, %s)"
#     db[0].execute(query, (user_id, request_date, status, id_link))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_request_id = db[0].fetchone()[0]
#     db[1].commit()

#     return {
#         "request_id": new_request_id, "user_id": user_id, 
#         "request_date": request_date, "status": status, "id_link": id_link
#     }

# @DocumentRequestRouter.put("/document_requests/{request_id}", response_model=dict)
# async def update_document_request(
#     request_id: int,
#     status: str,
#     id_link: str,
#     db=Depends(get_db)
# ):
#     query = "UPDATE document_request SET status = %s, id_link = %s WHERE request_id = %s"
#     db[0].execute(query, (status, id_link, request_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "Document request updated successfully"}
    
#     # If no rows were affected, document request not found
#     raise HTTPException(status_code=404, detail="Document request not found")

# @DocumentRequestRouter.delete("/document_requests/{request_id}", response_model=dict)
# async def delete_document_request(
#     request_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the document request exists
#         query_check_request = "SELECT request_id FROM document_request WHERE request_id = %s"
#         db[0].execute(query_check_request, (request_id,))
#         existing_request = db[0].fetchone()

#         if not existing_request:
#             raise HTTPException(status_code=404, detail="Document request not found")

#         # Delete the document request
#         query_delete_request = "DELETE FROM document_request WHERE request_id = %s"
#         db[0].execute(query_delete_request, (request_id,))
#         db[1].commit()

#         return {"message": "Document request deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()



# from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
# from db import get_db
# import jwt
# import datetime
# from pydantic import BaseModel
# from jwt import PyJWTError, decode
# from typing import List

# import os
# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env file

# SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
# ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

# # Create the DocumentRequestRouter instance
# DocumentRequestRouter = APIRouter(tags=["Document Requests"])

# # Define your models here
# class DocumentRequestItem(BaseModel):
#     document_type_id: int
#     quantity: int  # Enforce integer quantity

# class DocumentRequest(BaseModel):
#     items: List[DocumentRequestItem]


# def oauth2_scheme(request: Request):
#     token = request.cookies.get("access_token")
#     return token

# DocumentRequestRouter = APIRouter(tags=["Document Requests"])

# @DocumentRequestRouter.post("/auth/document_requests/", response_model=DocumentRequest)  # Adjust response model if needed
# async def create_document_request(items: DocumentRequest, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     """
#     Creates a new document request for the authenticated user.
#     """
#     try:
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")
#         print(f"Received request object: {items} from user {account_id}")

#         query = "INSERT INTO document_request (user_id) VALUES (%s)"
#         cursor = db[0].cursor()
#         cursor.execute(query, (account_id,))
#         request_id = cursor.lastrowid

#         for item in items.items:  # Access items using .items attribute
#             query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
#             cursor.execute(query, (request_id, item.document_type_id, item.quantity))

#         db[0].commit()
#         return {
#     "message": "Document request created successfully",
#     "request_id": request_id,
#     "items": [item.dict() for item in items.items]
# }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from db import get_db
import jwt
import datetime
from pydantic import BaseModel
from jwt import PyJWTError, decode
from typing import List

import os
# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

DocumentRequestRouter = APIRouter(tags=["Document Requests"])

class DocumentRequestItem(BaseModel):
    document_type_id: int
    quantity: int  # Enforce integer quantity

class DocumentRequest(BaseModel):
    items: List[DocumentRequestItem]

def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    return token

@DocumentRequestRouter.post("/auth/document_requests/", response_model=DocumentRequest)
async def create_document_request(items: DocumentRequest, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        if token.startswith('b\''):
          token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("account_id")
        print(f"Received request object: {items} from user {account_id}")

        query = "INSERT INTO document_request (user_id) VALUES (%s)"
        cursor = db[0].cursor()
        cursor.execute(query, (account_id,))
        request_id = cursor.lastrowid

        for item in items.items:  # Access items using .items attribute
            query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (request_id, item.document_type_id, item.quantity))

        db[0].commit()
        # Return a more structured response with a clear request_id
        return {
            "message": "Document request created successfully",
            "request_id": request_id,
            "items": [{"document_type_id": item.document_type_id, "quantity": item.quantity} for item in items.items]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))