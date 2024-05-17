from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from db import get_db
import jwt
from jwt import PyJWTError, decode
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

TrackDocumentsRouter = APIRouter(tags=["Track Documents"])

class UpdateReceiptLinkModel(BaseModel):
    request_id: int
    receipt_link: str

class UpdateStatusModel(BaseModel):
    request_id: int
    new_status: str

class UpdateFeedbackModel(BaseModel):
    request_id: int
    feedback_text: str
    feedback_rating: int
    
def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    return token

@TrackDocumentsRouter.get("/auth/track_document_requests")
async def get_document_requests(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        if token.startswith('b\''):
            token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("account_id")
        print(f"Fetching document requests for user {account_id}")

        cursor = db[0].cursor()

        query = """
        SELECT
            dr.request_id, 
            dr.user_id,
            s.student_school_id,
            CONCAT(u.first_name, ' ', COALESCE(u.middle_name, ''), ' ', u.last_name, ' ', COALESCE(u.suffix, '')) AS full_name,
            s.degree,
            u.email,
            s.address,
            s.contact,
            s.last_school_year,
            dt.name AS document_name,
            dr.request_date,
            dt2.payment_date,
            ci.claiming_date,
            dr.id_link,
            uth.total_amount_paid,
            uth.receipt_link,
            ci.mode_of_claiming,
            dr.status,
            cf.province,
            cf.municipality,
            cf.barangay,
            cf.present_address,
            cf.delivery_contact,
            cf.email AS courier_email,
            uf.feedback_text,
            uf.feedback_rating,
            uf.feedback_date
        FROM
            document_request dr
            JOIN student s ON dr.user_id = s.user_id
            JOIN user u ON dr.user_id = u.user_id
            JOIN document_request_item dri ON dr.request_id = dri.request_id
            JOIN document_type dt ON dri.document_type_id = dt.document_type_id
            LEFT JOIN document_transaction dt2 ON dr.request_id = dt2.request_id
            LEFT JOIN claiming_information ci ON dr.request_id = ci.request_id
            LEFT JOIN user_transaction_history uth ON dr.request_id = uth.request_id
            LEFT JOIN user_feedback uf ON dr.request_id = uf.request_id
            LEFT JOIN courier_information cf ON dr.request_id = cf.request_id
        WHERE
            dr.user_id = %s
        """
        cursor.execute(query, (account_id,))
        results = cursor.fetchall()
        
        if results:
            document_requests_dict = {}
            for result in results:
                request_id = result[0]
                if request_id not in document_requests_dict:
                    document_requests_dict[request_id] = {
                        "request_id": result[0],
                        "student_id": result[1],
                        "student_school_id": result[2],
                        "student_full_name": result[3],
                        "degree": result[4],
                        "email": result[5],
                        "address": result[6],
                        "contact": result[7],
                        "last_school_year": result[8],
                        "document_names": [result[9]],
                        "request_date": result[10],
                        "payment_date": result[11],
                        "claiming_date": result[12],
                        "id_link": result[13],
                        "total_amount_paid": result[14],
                        "receipt_link": result[15],
                        "mode_of_claiming": result[16],
                        "status": result[17],
                        "courier_info": {
                            "province": result[18],
                            "municipality": result[19],
                            "barangay": result[20],
                            "present_address": result[21],
                            "delivery_contact": result[22],
                            "email": result[23]
                        } if result[16] == "Courier" else None,
                        "feedback_text": result[24],
                        "feedback_rating": result[25],
                        "feedback_date": result[26]
                    }
                else:
                    document_requests_dict[request_id]["document_names"].append(result[9])

            document_requests = []
            for request_data in document_requests_dict.values():
                # Join the list of document names into a comma-separated string
                request_data["document_names"] = ", ".join(request_data["document_names"])
                document_requests.append({
                    "request_id": request_data["request_id"],
                    "student_id": request_data["student_id"],
                    "student_school_id": request_data["student_school_id"],
                    "student_full_name": request_data["student_full_name"],
                    "degree": request_data["degree"],
                    "email": request_data["email"],
                    "address": request_data["address"],
                    "contact": request_data["contact"],
                    "last_school_year": request_data["last_school_year"],
                    "document_names": request_data["document_names"],
                    "request_date": request_data["request_date"],
                    "payment_date": request_data["payment_date"],
                    "claiming_date": request_data["claiming_date"],
                    "id_link": request_data["id_link"],
                    "total_amount_paid": request_data["total_amount_paid"],
                    "receipt_link": request_data["receipt_link"],
                    "mode_of_claiming": request_data["mode_of_claiming"],
                    "status": request_data["status"],
                    "courier_info": request_data["courier_info"],
                    "feedback_text": request_data["feedback_text"],
                    "feedback_rating": request_data["feedback_rating"],
                    "feedback_date": request_data["feedback_date"]
                })

            return document_requests
        else:
            raise HTTPException(status_code=404, detail="No document requests found for the user")
        
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@TrackDocumentsRouter.put("/auth/update_receipt_link")
async def update_receipt_link(data: UpdateReceiptLinkModel, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        if token.startswith('b\''):
            token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("account_id")
        print(f"Updating receipt link for user {account_id}")

        cursor = db[0].cursor()

        query = """
        UPDATE user_transaction_history
        SET receipt_link = %s
        WHERE request_id = %s AND user_id = %s
        """
        cursor.execute(query, (data.receipt_link, data.request_id, account_id))
        db[0].commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Document request not found or not authorized to update")

        return {"message": "Receipt link updated successfully"}

    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@TrackDocumentsRouter.put("/auth/update_status")
async def update_status(data: UpdateStatusModel, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        if token.startswith('b\''):
            token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("account_id")
        print(f"Updating status for user {account_id}")

        cursor = db[0].cursor()

        query = """
        UPDATE document_request
        SET status = %s
        WHERE request_id = %s AND user_id = %s
        """
        cursor.execute(query, (data.new_status, data.request_id, account_id))
        db[0].commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Document request not found or not authorized to update")

        return {"message": "Status updated successfully"}

    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@TrackDocumentsRouter.put("/auth/update_feedback")
async def update_feedback(data: UpdateFeedbackModel, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        if token.startswith('b\''):
            token = token[2:-1]
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("account_id")
        print(f"Updating feedback for user {account_id}")

        cursor = db[0].cursor()

        query = """
        UPDATE user_feedback
        SET feedback_text = %s, feedback_rating = %s, feedback_date = %s
        WHERE request_id = %s AND user_id = %s
        """
        feedback_date = datetime.now()
        cursor.execute(query, (data.feedback_text, data.feedback_rating, feedback_date, data.request_id, account_id))
        db[0].commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Document request not found or not authorized to update")

        return {"message": "Feedback updated successfully"}

    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))