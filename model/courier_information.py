# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db

# CourierInformationRouter = APIRouter(tags=["Courier Information"])

# @CourierInformationRouter.get("/courier_information/", response_model=list)
# async def read_courier_information(
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT courier_id, user_id, request_id, province, municipality, barangay, 
#                present_address, delivery_contact, email
#         FROM courier_information
#     """
#     db[0].execute(query)
#     courier_information = [{
#         "courier_id": info[0], "user_id": info[1], "request_id": info[2], 
#         "province": info[3], "municipality": info[4], "barangay": info[5], 
#         "present_address": info[6], "delivery_contact": info[7], "email": info[8]
#     } for info in db[0].fetchall()]
#     return courier_information

# @CourierInformationRouter.get("/courier_information/{courier_id}", response_model=dict)
# async def read_courier_information_by_id(
#     courier_id: int, 
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT courier_id, user_id, request_id, province, municipality, barangay, 
#                present_address, delivery_contact, email
#         FROM courier_information
#         WHERE courier_id = %s
#     """
#     db[0].execute(query, (courier_id,))
#     courier_info = db[0].fetchone()
#     if courier_info:
#         return {
#             "courier_id": courier_info[0], "user_id": courier_info[1], 
#             "request_id": courier_info[2], "province": courier_info[3], 
#             "municipality": courier_info[4], "barangay": courier_info[5], 
#             "present_address": courier_info[6], "delivery_contact": courier_info[7], 
#             "email": courier_info[8]
#         }
#     raise HTTPException(status_code=404, detail="Courier information not found")

# @CourierInformationRouter.post("/courier_information/", response_model=dict)
# async def create_courier_information(
#     user_id: int, 
#     request_id: int,
#     province: str,
#     municipality: str,
#     barangay: str,
#     present_address: str,
#     delivery_contact: str,
#     email: str,
#     db=Depends(get_db)
# ):
#     query = """
#         INSERT INTO courier_information 
#         (user_id, request_id, province, municipality, barangay, 
#         present_address, delivery_contact, email) 
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     db[0].execute(query, (user_id, request_id, province, municipality, barangay, 
#                            present_address, delivery_contact, email))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_courier_id = db[0].fetchone()[0]
#     db[1].commit()

#     return {
#         "courier_id": new_courier_id, "user_id": user_id, "request_id": request_id,
#         "province": province, "municipality": municipality, "barangay": barangay,
#         "present_address": present_address, "delivery_contact": delivery_contact, "email": email
#     }

# @CourierInformationRouter.put("/courier_information/{courier_id}", response_model=dict)
# async def update_courier_information(
#     courier_id: int,
#     user_id: int, 
#     request_id: int,
#     province: str,
#     municipality: str,
#     barangay: str,
#     present_address: str,
#     delivery_contact: str,
#     email: str,
#     db=Depends(get_db)
# ):
#     query = """
#         UPDATE courier_information 
#         SET user_id = %s, request_id = %s, province = %s, municipality = %s, barangay = %s,
#         present_address = %s, delivery_contact = %s, email = %s 
#         WHERE courier_id = %s
#     """
#     db[0].execute(query, (user_id, request_id, province, municipality, barangay, 
#                            present_address, delivery_contact, email, courier_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "Courier information updated successfully"}
    
#     # If no rows were affected, courier information not found
#     raise HTTPException(status_code=404, detail="Courier information not found")

# @CourierInformationRouter.delete("/courier_information/{courier_id}", response_model=dict)
# async def delete_courier_information(
#     courier_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the courier information exists
#         query_check_info = "SELECT courier_id FROM courier_information WHERE courier_id = %s"
#         db[0].execute(query_check_info, (courier_id,))
#         existing_info = db[0].fetchone()

#         if not existing_info:
#             raise HTTPException(status_code=404, detail="Courier information not found")

#         # Delete the courier information
#         query_delete_info = "DELETE FROM courier_information WHERE courier_id = %s"
#         db[0].execute(query_delete_info, (courier_id,))
#         db[1].commit()

#         return {"message": "Courier information deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()

# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db

# CourierInformationRouter = APIRouter(tags=["Courier Information"])

# @CourierInformationRouter.get("/courier_information/", response_model=list)
# async def read_courier_information(
#     db=Depends(get_db)
# ):
#     try:
#         query = """
#             SELECT courier_id, user_id, request_id, province, municipality, barangay, 
#                    present_address, delivery_contact, email
#             FROM courier_information
#         """
#         db[1].execute(query)
#         courier_information = [{
#             "courier_id": info[0], "user_id": info[1], "request_id": info[2], 
#             "province": info[3], "municipality": info[4], "barangay": info[5], 
#             "present_address": info[6], "delivery_contact": info[7], "email": info[8]
#         } for info in db[1].fetchall()]
#         return courier_information
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db[1].close()
#         db[0].close()

# @CourierInformationRouter.get("/courier_information/{courier_id}", response_model=dict)
# async def read_courier_information_by_id(
#     courier_id: int, 
#     db=Depends(get_db)
# ):
#     try:
#         query = """
#             SELECT courier_id, user_id, request_id, province, municipality, barangay, 
#                    present_address, delivery_contact, email
#             FROM courier_information
#             WHERE courier_id = %s
#         """
#         db[1].execute(query, (courier_id,))
#         courier_info = db[1].fetchone()
#         if courier_info:
#             return {
#                 "courier_id": courier_info[0], "user_id": courier_info[1], 
#                 "request_id": courier_info[2], "province": courier_info[3], 
#                 "municipality": courier_info[4], "barangay": courier_info[5], 
#                 "present_address": courier_info[6], "delivery_contact": courier_info[7], 
#                 "email": courier_info[8]
#             }
#         raise HTTPException(status_code=404, detail="Courier information not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db[1].close()
#         db[0].close()

# @CourierInformationRouter.post("/courier_information/", response_model=dict)
# async def create_courier_information(
#     user_id: int, 
#     request_id: int,
#     province: str,
#     municipality: str,
#     barangay: str,
#     present_address: str,
#     delivery_contact: str,
#     email: str,
#     db=Depends(get_db)
# ):
#     try:
#         query = """
#             INSERT INTO courier_information 
#             (user_id, request_id, province, municipality, barangay, 
#             present_address, delivery_contact, email) 
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         db[1].execute(query, (user_id, request_id, province, municipality, barangay, 
#                                present_address, delivery_contact, email))

#         # Retrieve the last inserted ID using LAST_INSERT_ID()
#         db[1].execute("SELECT LAST_INSERT_ID()")
#         new_courier_id = db[1].fetchone()[0]
#         db[0].commit()

#         return {
#             "courier_id": new_courier_id, "user_id": user_id, "request_id": request_id,
#             "province": province, "municipality": municipality, "barangay": barangay,
#             "present_address": present_address, "delivery_contact": delivery_contact, "email": email
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db[1].close()
#         db[0].close()

# @CourierInformationRouter.put("/courier_information/{courier_id}", response_model=dict)
# async def update_courier_information(
#     courier_id: int,
#     user_id: int, 
#     request_id: int,
#     province: str,
#     municipality: str,
#     barangay: str,
#     present_address: str,
#     delivery_contact: str,
#     email: str,
#     db=Depends(get_db)
# ):
#     try:
#         query = """
#             UPDATE courier_information 
#             SET user_id = %s, request_id = %s, province = %s, municipality = %s, barangay = %s,
#             present_address = %s, delivery_contact = %s, email = %s 
#             WHERE courier_id = %s
#         """
#         db[1].execute(query, (user_id, request_id, province, municipality, barangay, 
#                                present_address, delivery_contact, email, courier_id))

#         # Check if the update was successful
#         if db[1].rowcount > 0:
#             db[0].commit()
#             return {"message": "Courier information updated successfully"}
        
#         # If no rows were affected, courier information not found
#         raise HTTPException(status_code=404, detail="Courier information not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db[1].close()
#         db[0].close()

# @CourierInformationRouter.delete("/courier_information/{courier_id}", response_model=dict)
# async def delete_courier_information(
#     courier_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the courier information exists
#         query_check_info = "SELECT courier_id FROM courier_information WHERE courier_id = %s"
#         db[1].execute(query_check_info, (courier_id,))
#         existing_info = db[1].fetchone()

#         if not existing_info:
#             raise HTTPException(status_code=404, detail="Courier information not found")

#         # Delete the courier information
#         query_delete_info = "DELETE FROM courier_information WHERE courier_id = %s"
#         db[1].execute(query_delete_info, (courier_id,))
#         db[0].commit()

#         return {"message": "Courier information deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[1].close()
#         db[0].close()

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from db import get_db
import jwt
from pydantic import BaseModel
from jwt import PyJWTError, decode

import os


SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    return token


# Define your models here
class CourierInformation(BaseModel):
    province: str
    municipality: str
    barangay: str
    present_address: str
    delivery_contact: str
    email: str

# Create the CourierInformationRouter instance
CourierInformationRouter = APIRouter(tags=["Courier Information"])

@CourierInformationRouter.post("/req/courier_information")
async def create_courier_information2(courier_info: CourierInformation, claiming_method: str, request_id: int, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """
    Creates a new courier information entry for a document request.
    """
    try:
        # Validate claiming method is "Courier"
        if claiming_method.lower() != "courier":
            raise HTTPException(status_code=400, detail="Claiming method must be 'Courier'")

        # Validate request_id exists (optional)
        # You can add logic to check if request_id exists in the database

        # Extract user_id from access token
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("account_id")  # Assuming "account_id" is the key in your payload

        query = """
            INSERT INTO courier_information (request_id, user_id, province, municipality, barangay, present_address, delivery_contact, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = db.cursor()
        cursor.execute(query, (request_id, user_id, courier_info.province, courier_info.municipality, courier_info.barangay,
                                courier_info.present_address, courier_info.delivery_contact, courier_info.email))
        db.commit()

        return {"message": "Courier information created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@CourierInformationRouter.get("/courier_information/", response_model=list)
async def read_courier_information(
    db=Depends(get_db)
):
    try:
        query = """
            SELECT courier_id, user_id, request_id, province, municipality, barangay, 
                   present_address, delivery_contact, email
            FROM courier_information
        """
        db[1].execute(query)
        courier_information = [{
            "courier_id": info[0], "user_id": info[1], "request_id": info[2], 
            "province": info[3], "municipality": info[4], "barangay": info[5], 
            "present_address": info[6], "delivery_contact": info[7], "email": info[8]
        } for info in db[1].fetchall()]
        return courier_information
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@CourierInformationRouter.get("/courier_information/{courier_id}", response_model=dict)
async def read_courier_information_by_id(
    courier_id: int, 
    db=Depends(get_db)
):
    try:
        query = """
            SELECT courier_id, user_id, request_id, province, municipality, barangay, 
                   present_address, delivery_contact, email
            FROM courier_information
            WHERE courier_id = %s
        """
        db[1].execute(query, (courier_id,))
        courier_info = db[1].fetchone()
        if courier_info:
            return {
                "courier_id": courier_info[0], "user_id": courier_info[1], 
                "request_id": courier_info[2], "province": courier_info[3], 
                "municipality": courier_info[4], "barangay": courier_info[5], 
                "present_address": courier_info[6], "delivery_contact": courier_info[7], 
                "email": courier_info[8]
            }
        raise HTTPException(status_code=404, detail="Courier information not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@CourierInformationRouter.post("/courier_information/", response_model=dict)
async def create_courier_information(
    user_id: int, 
    request_id: int,
    province: str,
    municipality: str,
    barangay: str,
    present_address: str,
    delivery_contact: str,
    email: str,
    db=Depends(get_db)
):
    try:
        query = """
            INSERT INTO courier_information 
            (user_id, request_id, province, municipality, barangay, 
            present_address, delivery_contact, email) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db[1].execute(query, (user_id, request_id, province, municipality, barangay, 
                               present_address, delivery_contact, email))

        # Retrieve the last inserted ID using LAST_INSERT_ID()
        db[1].execute("SELECT LAST_INSERT_ID()")
        new_courier_id = db[1].fetchone()[0]
        db[0].commit()

        return {
            "courier_id": new_courier_id, "user_id": user_id, "request_id": request_id,
            "province": province, "municipality": municipality, "barangay": barangay,
            "present_address": present_address, "delivery_contact": delivery_contact, "email": email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@CourierInformationRouter.put("/courier_information/{courier_id}", response_model=dict)
async def update_courier_information(
    courier_id: int,
    user_id: int, 
    request_id: int,
    province: str,
    municipality: str,
    barangay: str,
    present_address: str,
    delivery_contact: str,
    email: str,
    db=Depends(get_db)
):
    try:
        query = """
            UPDATE courier_information 
            SET user_id = %s, request_id = %s, province = %s, municipality = %s, barangay = %s,
            present_address = %s, delivery_contact = %s, email = %s 
            WHERE courier_id = %s
        """
        db[1].execute(query, (user_id, request_id, province, municipality, barangay, 
                               present_address, delivery_contact, email, courier_id))

        # Check if the update was successful
        if db[1].rowcount > 0:
            db[0].commit()
            return {"message": "Courier information updated successfully"}
        
        # If no rows were affected, courier information not found
        raise HTTPException(status_code=404, detail="Courier information not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@CourierInformationRouter.delete("/courier_information/{courier_id}", response_model=dict)
async def delete_courier_information(
    courier_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the courier information exists
        query_check_info = "SELECT courier_id FROM courier_information WHERE courier_id = %s"
        db[1].execute(query_check_info, (courier_id,))
        existing_info = db[1].fetchone()

        if not existing_info:
            raise HTTPException(status_code=404, detail="Courier information not found")

        # Delete the courier information
        query_delete_info = "DELETE FROM courier_information WHERE courier_id = %s"
        db[1].execute(query_delete_info, (courier_id,))
        db[0].commit()

        return {"message": "Courier information deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[1].close()
        db[0].close()