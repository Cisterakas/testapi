from fastapi import APIRouter, Depends, HTTPException, Request
from db import get_db
from pydantic import BaseModel
from typing import List, Optional
import datetime
from collections import defaultdict
import os

SECRET_KEY = os.getenv("SECRET_KEY")  # Access from environment
ALGORITHM = os.getenv("ALGORITHM")  # Access from environment

ConfirmationRouter = APIRouter(tags=["Confirmation"])

class DocumentRequestResponse(BaseModel):
    request_id: int
    student_id: int
    student_school_id: str
    student_full_name: str
    degree: str
    address: str
    contact: str
    email: str
    document_name: str
    request_date: str
    id_link: Optional[str] = None
    total_amount_paid: float
    claiming_method: Optional[str]
    status: str
    claiming_date: Optional[str]
    payment_date: Optional[str]
    courier_info: Optional[dict]

class UpdateStatus(BaseModel):
    request_id: int

def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    return token

@ConfirmationRouter.get("/confirmations/")
async def get_confirmation_requests(status: str = "To Receive", db=Depends(get_db)):
    try:
        cursor = db[0].cursor()

        query = """
        SELECT 
            dr.request_id,
            s.user_id AS student_id,
            s.student_school_id,
            CONCAT(u.first_name, ' ', COALESCE(u.middle_name, ''), ' ', u.last_name) AS student_full_name,
            s.degree,
            s.address,
            s.contact,
            u.email,
            dt.name AS document_name,
            dr.request_date,
            dr.id_link,
            uth.total_amount_paid,
            ci.mode_of_claiming AS claiming_method,
            dr.status,
            ci.claiming_date,
            dtt.payment_date,
            coi.province,
            coi.municipality,
            coi.barangay,
            coi.present_address,
            coi.delivery_contact,
            coi.email AS courier_email
        FROM document_request dr
        INNER JOIN student s ON dr.user_id = s.user_id
        INNER JOIN user u ON s.user_id = u.user_id
        INNER JOIN document_request_item dri ON dr.request_id = dri.request_id
        INNER JOIN document_type dt ON dri.document_type_id = dt.document_type_id
        LEFT JOIN claiming_information ci ON dr.request_id = ci.request_id
        LEFT JOIN courier_information coi ON dr.request_id = coi.request_id
        LEFT JOIN user_transaction_history uth ON dr.request_id = uth.request_id
        LEFT JOIN document_transaction dtt ON dr.request_id = dtt.request_id
        WHERE dr.status = %s
        """

        cursor.execute(query, (status,))
        result = cursor.fetchall()

        document_requests_dict = defaultdict(lambda: {
            "request_id": None,
            "student_id": None,
            "student_school_id": None,
            "student_full_name": None,
            "degree": None,
            "address": None,
            "contact": None,
            "email": None,
            "document_names": [],
            "request_date": None,
            "id_link": None,
            "total_amount_paid": 0.0,
            "claiming_method": None,
            "status": None,
            "claiming_date": None,
            "payment_date": None,
            "courier_info": None
        })

        for row in result:
            request_id, student_id, student_school_id, student_full_name, degree, address, contact, email, document_name, request_date, id_link, total_amount_paid, claiming_method, status, claiming_date, payment_date, province, municipality, barangay, present_address, delivery_contact, courier_email = row
            
            if document_requests_dict[request_id]["request_id"] is None:
                document_requests_dict[request_id].update({
                    "request_id": request_id,
                    "student_id": student_id,
                    "student_school_id": student_school_id,
                    "student_full_name": student_full_name,
                    "degree": degree,
                    "address": address,
                    "contact": contact,
                    "email": email,
                    "request_date": str(request_date),
                    "id_link": id_link,
                    "total_amount_paid": float(total_amount_paid),
                    "claiming_method": claiming_method,
                    "status": status,
                    "claiming_date": str(claiming_date) if claiming_date else None,
                    "payment_date": str(payment_date) if payment_date else None
                })
                if claiming_method == "Courier":
                    document_requests_dict[request_id]["courier_info"] = {
                        "province": province,
                        "municipality": municipality,
                        "barangay": barangay,
                        "present_address": present_address,
                        "delivery_contact": delivery_contact,
                        "email": courier_email
                    }
            document_requests_dict[request_id]["document_names"].append(document_name)

        document_requests = []
        for request in document_requests_dict.values():
            document_requests.append(DocumentRequestResponse(
                request_id=request["request_id"],
                student_id=request["student_id"],
                student_school_id=request["student_school_id"],
                student_full_name=request["student_full_name"],
                degree=request["degree"],
                address=request["address"],
                contact=request["contact"],
                email=request["email"],
                document_name=", ".join(request["document_names"]),
                request_date=request["request_date"],
                id_link=request["id_link"],
                total_amount_paid=request["total_amount_paid"],
                claiming_method=request["claiming_method"],
                status=request["status"],
                claiming_date=request["claiming_date"],
                payment_date=request["payment_date"],
                courier_info=request["courier_info"]
            ))

        return document_requests

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ConfirmationRouter.put("/confirmations/update-status/")
async def update_request_status(update_status: UpdateStatus, db=Depends(get_db)):
    try:
        cursor = db[0].cursor()

        query = """
        UPDATE document_request
        SET status = 'Received'
        WHERE request_id = %s
        """

        cursor.execute(query, (update_status.request_id,))
        db[0].commit()

        return {"message": "Status updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
