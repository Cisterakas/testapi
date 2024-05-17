from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from db import get_db
PaymentsRouter = APIRouter(tags=["Payments"])

@PaymentsRouter.get("/payments/", response_model=list)
async def read_payments(db=Depends(get_db)):
    try:
        query = """
           SELECT
    dr.request_id AS request_number,
    s.student_school_id AS school_student_id,
    CONCAT(u.first_name, ' ', IFNULL(u.middle_name, ''), ' ', u.last_name) AS full_name,
    GROUP_CONCAT(dt.name SEPARATOR ', ') AS document_names,
    MAX(dtu.total_amount_paid) AS total_fee,
    MAX(dtu.receipt_link) AS receipt_link,
    MAX(dt_alias.payment_date) AS payment_date,
    MAX(ci.claiming_date) AS claiming_date,
    dr.status
FROM
    document_request dr
JOIN user u ON dr.user_id = u.user_id
JOIN student s ON dr.user_id = s.user_id
LEFT JOIN document_request_item dri ON dr.request_id = dri.request_id
LEFT JOIN document_type dt ON dri.document_type_id = dt.document_type_id
LEFT JOIN user_transaction_history dtu ON dr.request_id = dtu.request_id
LEFT JOIN document_transaction dt_alias ON dr.request_id = dt_alias.request_id
LEFT JOIN claiming_information ci ON dr.request_id = ci.request_id
WHERE
    dr.status = 'To Pay'
GROUP BY
    dr.request_id, s.student_school_id, u.first_name, u.middle_name, u.last_name, dr.status;

        """
        cursor = db[1]
        cursor.execute(query)
        payments = [{
            "request_number": row[0], "school_student_id": row[1], "full_name": row[2], "document_names": row[3],
            "total_fee": row[4], "receipt_link": row[5], "payment_date": row[6], "claiming_date": row[7], "status": row[8]
        } for row in cursor.fetchall()]
        return payments
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

# Other CRUD operations (create, update, delete) can be added as needed
class UpdateStatus(BaseModel):
    status: str

class UpdatePaymentDate(BaseModel):
    payment_date: str

class UpdateClaimingDate(BaseModel):
    claiming_date: str

class UpdateReceiptLink(BaseModel):
    receipt_link: str

@PaymentsRouter.put("/payments/update-status/{request_number}")
async def update_status(request_number: int, update_data: UpdateStatus, db=Depends(get_db)):
    status = update_data.status
    try:
        query = "UPDATE document_request SET status = %s WHERE request_id = %s;"
        cursor = db[1]
        cursor.execute(query, (status, request_number))
        db[0].commit()
        return {"message": "Status updated successfully."}
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@PaymentsRouter.put("/payments/update-payment-date/{request_number}")
async def update_payment_date(request_number: int, update_data: UpdatePaymentDate, db=Depends(get_db)):
    payment_date = update_data.payment_date
    try:
        query = "UPDATE document_transaction SET payment_date = %s WHERE request_id = %s;"
        cursor = db[1]
        cursor.execute(query, (payment_date, request_number))
        db[0].commit()
        return {"message": "Payment date updated successfully."}
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@PaymentsRouter.put("/payments/update-claiming-date/{request_number}")
async def update_claiming_date(request_number: int, update_data: UpdateClaimingDate, db=Depends(get_db)):
    claiming_date = update_data.claiming_date
    try:
        query = "UPDATE claiming_information SET claiming_date = %s WHERE request_id = %s;"
        cursor = db[1]  
        cursor.execute(query, (claiming_date, request_number))
        db[0].commit()
        return {"message": "Claiming date updated successfully."}
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@PaymentsRouter.put("/payments/update-receipt-link/{request_number}")
async def update_receipt_link(request_number: int, update_data: UpdateReceiptLink, db=Depends(get_db)):
    receipt_link = update_data.receipt_link
    try:
        query = "UPDATE user_transaction_history SET receipt_link = %s WHERE request_id = %s;"
        cursor = db[1]
        cursor.execute(query, (receipt_link, request_number))
        db[0].commit()
        return {"message": "Receipt link updated successfully."}
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()
