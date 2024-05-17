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




# from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
# from db import get_db
# import jwt
# import datetime
# from pydantic import BaseModel
# from jwt import PyJWTError, decode
# from typing import List, Optional

# import os

# SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
# ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

# DocumentRequestRouter = APIRouter(tags=["Document Requests"])


# class DocumentRequestItem(BaseModel):
#     document_type_id: int
#     quantity: int  # Enforce integer quantity
#     mode_of_claiming: Optional[str] = None
    
# class DocumentRequest(BaseModel):
#     items: List[DocumentRequestItem]

# def oauth2_scheme(request: Request):
#     token = request.cookies.get("access_token")
#     return token

# latest_request_id = None

# @DocumentRequestRouter.post("/auth/document_requests/", response_model=DocumentRequest)
# async def create_document_request(items: DocumentRequest, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     global latest_request_id  # Access the global variable
#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")
#         print(f"Received request object: {items} from user {account_id}")

#         cursor = db[0].cursor()

#         # Insert into document_request table
#         query = "INSERT INTO document_request (user_id) VALUES (%s)"
#         cursor.execute(query, (account_id,))
#         request_id = cursor.lastrowid
#         latest_request_id = cursor.lastrowid  # Store the latest request ID

#         # Insert into document_request_item table
#         for item in items.items:
#             query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
#             cursor.execute(query, (request_id, item.document_type_id, item.quantity))

#             # Insert into claiming_information table
#         query = "INSERT INTO claiming_information (request_id, mode_of_claiming) VALUES (%s, %s)"
#         cursor.execute(query, (request_id, item.mode_of_claiming))

#         # Insert into document_transaction table
#         query = "INSERT INTO document_transaction (request_id) VALUES (%s)"
#         cursor.execute(query, (request_id,))

#         # Insert into user_feedback table
#         query = "INSERT INTO user_feedback (user_id, request_id, feedback_text, feedback_rating, feedback_date) VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(query, (account_id, request_id, None, None, None))

#         # Insert into user_transaction_history table
#         query = "INSERT INTO user_transaction_history (user_id, request_id, total_amount_paid, receipt_link) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (account_id, request_id, 0.00, None))
        
#         db[0].commit()

#         return {"request_id": latest_request_id, "items": [], "message": "Document request created successfully"}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @DocumentRequestRouter.put("/auth/document_requests/claiming_information", response_model=dict)
# async def update_claiming_info(claiming_info: dict, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     global latest_request_id  # Access the global variable
#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")

#         cursor = db[0].cursor()

#         # Check if the request ID exists and belongs to the current user
#         request_id = claiming_info.get('request_id')
#         mode_of_claiming = claiming_info.get('mode_of_claiming')
#         if not request_id or not mode_of_claiming:
#             raise HTTPException(status_code=422, detail="Missing request_id or mode_of_claiming")

#         query = "SELECT user_id FROM document_request WHERE request_id = %s"
#         cursor.execute(query, (request_id,))
#         result = cursor.fetchone()
#         if not result:
#             raise HTTPException(status_code=404, detail="Document request not found")
#         if result[0] != account_id:
#             raise HTTPException(status_code=403, detail="Unauthorized access")

#         # Update mode of claiming in claiming_information table
#         query = "UPDATE claiming_information SET mode_of_claiming = %s WHERE request_id = %s"
#         cursor.execute(query, (mode_of_claiming, request_id))

#         db[0].commit()

#         return {"message": "Claiming information updated successfully"}
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @DocumentRequestRouter.post("/auth/courier_information/", response_model=dict)
# async def create_courier_information(
#     request_id: int,
#     province: str,
#     municipality: str,
#     barangay: str,
#     present_address: str,
#     delivery_contact: str,
#     email: str,
#     token: str = Depends(oauth2_scheme),
#     db=Depends(get_db)
# ):
#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")

#         cursor = db[0].cursor()

#         # Check if the request ID exists and belongs to the current user
#         query = "SELECT user_id FROM document_request WHERE request_id = %s"
#         cursor.execute(query, (request_id,))
#         result = cursor.fetchone()
#         if not result:
#             raise HTTPException(status_code=404, detail="Document request not found")
#         if result[0] != account_id:
#             raise HTTPException(status_code=403, detail="Unauthorized access")

#         # Save courier information to courier_information table
#         query = """
#             INSERT INTO courier_information (
#                 request_id,
#                 user_id,
#                 province,
#                 municipality,
#                 barangay,
#                 present_address,
#                 delivery_contact,
#                 email
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(query, (request_id, account_id, province, municipality, barangay, present_address, delivery_contact, email))

#         db[0].commit()

#         return {"message": "Courier information saved successfully"}
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @DocumentRequestRouter.put("/auth/document_requests/update_id_link", response_model=dict)
# async def update_document_request_id_link(request_data: dict, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")

#         cursor = db[0].cursor()

#         # Check if the request ID exists and belongs to the current user
#         request_id = request_data.get('request_id')
#         id_link = request_data.get('id_link')
#         if not request_id or not id_link:
#             raise HTTPException(status_code=422, detail="Missing request_id or id_link")

#         query = "SELECT user_id FROM document_request WHERE request_id = %s"
#         cursor.execute(query, (request_id,))
#         result = cursor.fetchone()
#         if not result:
#             raise HTTPException(status_code=404, detail="Document request not found")
#         if result[0] != account_id:
#             raise HTTPException(status_code=403, detail="Unauthorized access")

#         # Update id_link for the document_request table
#         query = "UPDATE document_request SET id_link = %s WHERE request_id = %s"
#         cursor.execute(query, (id_link, request_id))

#         db[0].commit()

#         return {"message": "ID link updated successfully"}
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#MAY 15 2024
# from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
# from db import get_db
# import jwt
# import datetime
# from pydantic import BaseModel
# from jwt import PyJWTError, decode
# from typing import List, Optional
# from fastapi import Path

# import os

# SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
# ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

# DocumentRequestRouter = APIRouter(tags=["Document Requests"])

# latest_request_id = None  # Variable to store the latest request ID


# class DocumentRequestItem(BaseModel):
#     document_type_id: int
#     quantity: int  # Enforce integer quantity
#     mode_of_claiming: Optional[str] = None
    
# class DocumentRequest(BaseModel):
#     items: List[DocumentRequestItem]

# def oauth2_scheme(request: Request):
#     token = request.cookies.get("access_token")
#     return token


# @DocumentRequestRouter.post("/auth/document_requests/", response_model=DocumentRequest)
# async def create_document_request(items: DocumentRequest, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     global latest_request_id  # Access the global variable

#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")
#         print(f"Received request object: {items} from user {account_id}")

#         cursor = db[0].cursor()

#         # Insert into document_request table
#         query = "INSERT INTO document_request (user_id) VALUES (%s)"
#         cursor.execute(query, (account_id,))
#         latest_request_id = cursor.lastrowid  # Store the latest request ID

#         # Insert into document_request_item table
#         for item in items.items:
#             query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
#             cursor.execute(query, (latest_request_id, item.document_type_id, item.quantity))

#         # Insert into claiming_information table
#         for item in items.items:  # Iterate again to get the latest mode_of_claiming
#             query = "INSERT INTO claiming_information (request_id, mode_of_claiming) VALUES (%s, %s)"
#             cursor.execute(query, (latest_request_id, item.mode_of_claiming))

#         # Insert into document_transaction table
#         query = "INSERT INTO document_transaction (request_id) VALUES (%s)"
#         cursor.execute(query, (latest_request_id,))

#         # Insert into user_feedback table
#         query = "INSERT INTO user_feedback (user_id, request_id, feedback_text, feedback_rating, feedback_date) VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(query, (account_id, latest_request_id, None, None, None))

#         # Insert into user_transaction_history table
#         query = "INSERT INTO user_transaction_history (user_id, request_id, total_amount_paid, receipt_link) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (account_id, latest_request_id, 0.00, None))
        
#         db[0].commit()
#         print(f"Latest request ID: {latest_request_id}")

#         # Return the response with the latest request_id
#         return {"request_id": latest_request_id, "items": [], "message": "Document request created successfully"}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @DocumentRequestRouter.put("/auth/document_requests/{request_id}/claiming_information", response_model=dict)
# async def update_claiming_info(claiming_info: dict, request_id: int = Path(...), token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")

#         cursor = db[0].cursor()

#         # Update mode of claiming in claiming_information table
#         query = "UPDATE claiming_information SET mode_of_claiming = %s WHERE request_id = %s"
#         cursor.execute(query, (claiming_info['mode_of_claiming'], request_id))

#         db[0].commit()

#         return {"message": "Claiming information updated successfully"}
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @DocumentRequestRouter.post("/auth/courier_information/", response_model=dict)
# async def create_courier_information(
#     province: str,
#     municipality: str,
#     barangay: str,
#     present_address: str,
#     delivery_contact: str,
#     email: str,
#     token: str = Depends(oauth2_scheme),
#     db=Depends(get_db)
# ):
#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")

#         cursor = db[0].cursor()

#         # Fetch the latest request ID
#         query = "SELECT MAX(request_id) FROM document_request"
#         cursor.execute(query)
#         latest_request_id = cursor.fetchone()[0]

#         if latest_request_id is None:
#             raise HTTPException(status_code=404, detail="No request IDs found")

#         # Save courier information to courier_information table
#         query = """
#             INSERT INTO courier_information (
#                 request_id,
#                 user_id,
#                 province,
#                 municipality,
#                 barangay,
#                 present_address,
#                 delivery_contact,
#                 email
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(query, (latest_request_id, account_id, province, municipality, barangay, present_address, delivery_contact, email))

#         db[0].commit()

#         return {"message": "Courier information saved successfully"}
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @DocumentRequestRouter.put("/auth/document_requests/{request_id}/update_id_link", response_model=dict)
# async def update_document_request_id_link(request_data: dict, request_id: int = Path(...), token: str = Depends(oauth2_scheme), db=Depends(get_db)):

#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")

#         cursor = db[0].cursor()

#         # Update id_link for the document_request table
#         query = "UPDATE document_request SET id_link = %s WHERE request_id = %s"
#         cursor.execute(query, (request_data['id_link'], request_id))

#         db[0].commit()

#         return {"message": "ID link updated successfully"}
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
# from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Path
# from db import get_db
# import jwt
# import datetime
# from pydantic import BaseModel
# from jwt import PyJWTError, decode
# from typing import List, Optional
# import os

# SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
# ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

# DocumentRequestRouter = APIRouter(tags=["Document Requests"])

# latest_request_id = None  # Variable to store the latest request ID

# class DocumentRequestItem(BaseModel):
#     document_type_id: int
#     quantity: int  # Enforce integer quantity
#     mode_of_claiming: Optional[str] = None

# class DocumentRequest(BaseModel):
#     items: List[DocumentRequestItem]

# class UpdateClaimingInformation(BaseModel):
#     mode_of_claiming: Optional[str] = None
#     claiming_date: Optional[datetime.date] = None

# def oauth2_scheme(request: Request):
#     token = request.cookies.get("access_token")
#     return token

# @DocumentRequestRouter.post("/auth/document_requests/", response_model=DocumentRequest)
# async def create_document_request(items: DocumentRequest, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     global latest_request_id  # Access the global variable

#     try:
#         if token.startswith('b\''):
#             token = token[2:-1]
#         payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         account_id = payload.get("account_id")
#         print(f"Received request object: {items} from user {account_id}")

#         cursor = db[0].cursor()

#         # Insert into document_request table
#         query = "INSERT INTO document_request (user_id) VALUES (%s)"
#         cursor.execute(query, (account_id,))
#         latest_request_id = cursor.lastrowid  # Store the latest request ID

#         # Insert into document_request_item table
#         for item in items.items:
#             query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
#             cursor.execute(query, (latest_request_id, item.document_type_id, item.quantity))

#         # Insert into claiming_information table
#         for item in items.items:  # Iterate again to get the latest mode_of_claiming
#             query = "INSERT INTO claiming_information (request_id, mode_of_claiming) VALUES (%s, %s)"
#             cursor.execute(query, (latest_request_id, item.mode_of_claiming))

#         # Insert into document_transaction table
#         query = "INSERT INTO document_transaction (request_id) VALUES (%s)"
#         cursor.execute(query, (latest_request_id,))

#         # Insert into user_feedback table
#         query = "INSERT INTO user_feedback (user_id, request_id, feedback_text, feedback_rating, feedback_date) VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(query, (account_id, latest_request_id, None, None, None))

#         # Insert into user_transaction_history table
#         query = "INSERT INTO user_transaction_history (user_id, request_id, total_amount_paid, receipt_link) VALUES (%s, %s, %s, %s)"
#         cursor.execute(query, (account_id, latest_request_id, 0.00, None))
        
#         db[0].commit()
#         print(f"Latest request ID: {latest_request_id}")

#         # Return the response with the latest request_id
#         return {"request_id": latest_request_id, "items": [], "message": "Document request created successfully"}
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from db import get_db
import jwt
import datetime
from pydantic import BaseModel
from jwt import PyJWTError, decode
from typing import List, Optional
import os

SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

DocumentRequestRouter = APIRouter(tags=["Document Requests"])

latest_request_id = None  # Variable to store the latest request ID

class DocumentRequestItem(BaseModel):
    document_type_id: int
    quantity: int  # Enforce integer quantity
    mode_of_claiming: Optional[str] = None

class DocumentRequest(BaseModel):
    id_link: str
    items: List[DocumentRequestItem]

class CourierInformation(BaseModel):
    province: str
    municipality: str
    barangay: str
    present_address: str
    delivery_contact: str
    email: str

class UpdateClaimingInformation(BaseModel):
    mode_of_claiming: Optional[str] = None
    claiming_date: Optional[datetime.date] = None

def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    return token

@DocumentRequestRouter.post("/auth/document_requests/", response_model=DocumentRequest)
async def create_document_request(items: DocumentRequest, token: str = Depends(oauth2_scheme), db=Depends(get_db), courier_info: Optional[CourierInformation] = None):
    global latest_request_id  # Access the global variable

    try:
        if token.startswith('b\''):
            token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("account_id")
        print(f"Received request object: {items} from user {account_id}")

        cursor = db[0].cursor()

        # Insert into document_request table with provided id_link
        query = "INSERT INTO document_request (user_id, id_link) VALUES (%s, %s)"
        cursor.execute(query, (account_id, items.id_link))
        latest_request_id = cursor.lastrowid  # Store the latest request ID
        
        total_amount_paid = 0.00  # Initialize total amount paid


        # Insert into document_request_item table
        for item in items.items:
            query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (latest_request_id, item.document_type_id, item.quantity))
            
            query = "SELECT fee FROM document_type WHERE document_type_id = %s"
            cursor.execute(query, (item.document_type_id,))
            fee = cursor.fetchone()[0]

            total_amount_paid += float(fee) * item.quantity 

        # Insert into claiming_information table
        query = "INSERT INTO claiming_information (request_id, mode_of_claiming) VALUES (%s, %s)"
        cursor.execute(query, (latest_request_id, items.items[0].mode_of_claiming))

        # If mode of claiming is "Courier", insert into courier_information table
        if items.items[0].mode_of_claiming == "Courier" and courier_info:
            query = """
            INSERT INTO courier_information (
                user_id, request_id, province, municipality, barangay, present_address, delivery_contact, email
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                account_id, latest_request_id, courier_info.province, courier_info.municipality,
                courier_info.barangay, courier_info.present_address, courier_info.delivery_contact,
                courier_info.email
            ))

        # Insert into document_transaction table
        query = "INSERT INTO document_transaction (request_id) VALUES (%s)"
        cursor.execute(query, (latest_request_id,))

        # Insert into user_feedback table
        query = "INSERT INTO user_feedback (user_id, request_id, feedback_text, feedback_rating, feedback_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (account_id, latest_request_id, None, None, None))

        # Insert into user_transaction_history table
        query = "INSERT INTO user_transaction_history (user_id, request_id, total_amount_paid, receipt_link) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (account_id, latest_request_id, total_amount_paid, None))
        
        db[0].commit()
        print(f"Latest request ID: {latest_request_id}")

        # Return the response with the latest request_id
        return {"id_link": items.id_link, "request_id": latest_request_id, "items": items.items, "message": "Document request created successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
