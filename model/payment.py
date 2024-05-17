# from fastapi import Depends, HTTPException, APIRouter
# from pydantic import BaseModel
# from db import get_db
# PaymentsRouter = APIRouter(tags=["Payments"])

# @PaymentsRouter.get("/payments/", response_model=list)
# async def read_payments(db=Depends(get_db)):
#     try:
#         query = """
#            SELECT
#     dr.request_id AS request_number,
#     s.student_school_id AS school_student_id,
#     CONCAT(u.first_name, ' ', IFNULL(u.middle_name, ''), ' ', u.last_name) AS full_name,
#     GROUP_CONCAT(dt.name SEPARATOR ', ') AS document_names,
#     MAX(dtu.total_amount_paid) AS total_fee,
#     MAX(dtu.receipt_link) AS receipt_link,
#     MAX(dt_alias.payment_date) AS payment_date,
#     MAX(ci.claiming_date) AS claiming_date,
#     dr.status
# FROM
#     document_request dr
# JOIN user u ON dr.user_id = u.user_id
# JOIN student s ON dr.user_id = s.user_id
# LEFT JOIN document_request_item dri ON dr.request_id = dri.request_id
# LEFT JOIN document_type dt ON dri.document_type_id = dt.document_type_id
# LEFT JOIN user_transaction_history dtu ON dr.request_id = dtu.request_id
# LEFT JOIN document_transaction dt_alias ON dr.request_id = dt_alias.request_id
# LEFT JOIN claiming_information ci ON dr.request_id = ci.request_id
# WHERE
#     dr.status = 'To Pay'
# GROUP BY
#     dr.request_id, s.student_school_id, u.first_name, u.middle_name, u.last_name, dr.status;

#         """
#         cursor = db[1]
#         cursor.execute(query)
#         payments = [{
#             "request_number": row[0], "school_student_id": row[1], "full_name": row[2], "document_names": row[3],
#             "total_fee": row[4], "receipt_link": row[5], "payment_date": row[6], "claiming_date": row[7], "status": row[8]
#         } for row in cursor.fetchall()]
#         return payments
#     finally:
#         # Ensure to close the cursor and connection
#         db[1].close()
#         db[0].close()

# # Other CRUD operations (create, update, delete) can be added as needed
# class UpdateStatus(BaseModel):
#     status: str

# class UpdatePaymentDate(BaseModel):
#     payment_date: str

# class UpdateClaimingDate(BaseModel):
#     claiming_date: str

# class UpdateReceiptLink(BaseModel):
#     receipt_link: str

# @PaymentsRouter.put("/payments/update-status/{request_number}")
# async def update_status(request_number: int, update_data: UpdateStatus, db=Depends(get_db)):
#     status = update_data.status
#     try:
#         query = "UPDATE document_request SET status = %s WHERE request_id = %s;"
#         cursor = db[1]
#         cursor.execute(query, (status, request_number))
#         db[0].commit()
#         return {"message": "Status updated successfully."}
#     finally:
#         # Ensure to close the cursor and connection
#         db[1].close()
#         db[0].close()

# @PaymentsRouter.put("/payments/update-payment-date/{request_number}")
# async def update_payment_date(request_number: int, update_data: UpdatePaymentDate, db=Depends(get_db)):
#     payment_date = update_data.payment_date
#     try:
#         query = "UPDATE document_transaction SET payment_date = %s WHERE request_id = %s;"
#         cursor = db[1]
#         cursor.execute(query, (payment_date, request_number))
#         db[0].commit()
#         return {"message": "Payment date updated successfully."}
#     finally:
#         # Ensure to close the cursor and connection
#         db[1].close()
#         db[0].close()

# @PaymentsRouter.put("/payments/update-claiming-date/{request_number}")
# async def update_claiming_date(request_number: int, update_data: UpdateClaimingDate, db=Depends(get_db)):
#     claiming_date = update_data.claiming_date
#     try:
#         query = "UPDATE claiming_information SET claiming_date = %s WHERE request_id = %s;"
#         cursor = db[1]  
#         cursor.execute(query, (claiming_date, request_number))
#         db[0].commit()
#         return {"message": "Claiming date updated successfully."}
#     finally:
#         # Ensure to close the cursor and connection
#         db[1].close()
#         db[0].close()

# @PaymentsRouter.put("/payments/update-receipt-link/{request_number}")
# async def update_receipt_link(request_number: int, update_data: UpdateReceiptLink, db=Depends(get_db)):
#     receipt_link = update_data.receipt_link
#     try:
#         query = "UPDATE user_transaction_history SET receipt_link = %s WHERE request_id = %s;"
#         cursor = db[1]
#         cursor.execute(query, (receipt_link, request_number))
#         db[0].commit()
#         return {"message": "Receipt link updated successfully."}
#     finally:
#         # Ensure to close the cursor and connection
#         db[1].close()
#         db[0].close()

from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from db import get_db
from datetime import datetime

PaymentsRouter = APIRouter(tags=["Payments"])

class PaymentUpdate(BaseModel):
    request_number: int
    total_fee: float
    claiming_date: datetime  # Updated data type to datetime
    documents: list

class PaymentStatusUpdate(BaseModel):
    request_number: int
    status: str

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
        db[1].close()
        db[0].close()

@PaymentsRouter.put("/payments/update/")
async def update_payment(payment: PaymentUpdate, db=Depends(get_db)):
    try:
        cursor = db[1]

        # Update total fee
        update_fee_query = """
            UPDATE user_transaction_history
            SET total_amount_paid = %s
            WHERE request_id = %s;
        """
        cursor.execute(update_fee_query, (
            payment.total_fee,
            payment.request_number
        ))

        # Update claiming date
        update_claiming_date_query = """
            UPDATE claiming_information
            SET claiming_date = %s
            WHERE request_id = %s;
        """
        cursor.execute(update_claiming_date_query, (
            payment.claiming_date,
            payment.request_number
        ))

        # Update documents quantities (if necessary)
        for document in payment.documents:
            update_doc_query = """
                UPDATE document_request_item
                SET quantity = %s
                WHERE request_id = %s AND document_type_id = %s;
            """
            cursor.execute(update_doc_query, (
                document['quantity'],
                payment.request_number,
                document['document_type_id']
            ))

        db[0].commit()
        return {"message": "Payment updated successfully"}
    finally:
        db[1].close()
        db[0].close()

@PaymentsRouter.put("/payments/update-status/")
async def update_payment_status(payment_status: PaymentStatusUpdate, db=Depends(get_db)):
    try:
        cursor = db[1]
        update_query = """
            UPDATE document_request dr
            JOIN document_transaction dt_alias ON dr.request_id = dt_alias.request_id
            SET dr.status = %s,
                dt_alias.payment_date = CASE WHEN %s = 'To Receive' THEN %s ELSE dt_alias.payment_date END
            WHERE dr.request_id = %s;
        """
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payment_date = current_timestamp if payment_status.status == 'To Receive' else None
        cursor.execute(update_query, (
            payment_status.status,
            payment_status.status,
            payment_date,
            payment_status.request_number
        ))
        db[0].commit()
        return {"message": "Payment status updated successfully"}
    finally:
        db[1].close()
        db[0].close()