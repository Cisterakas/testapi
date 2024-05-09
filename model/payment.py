from fastapi import Depends, HTTPException, APIRouter
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
                ut.total_amount_paid AS total_fee,
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
            LEFT JOIN (
                SELECT
                    request_id,
                    SUM(dt.fee * dri.quantity) AS total_amount_paid
                FROM
                    document_request_item dri
                JOIN document_type dt ON dri.document_type_id = dt.document_type_id
                GROUP BY
                    dri.request_id
            ) ut ON dr.request_id = ut.request_id
            LEFT JOIN user_transaction_history dtu ON dr.request_id = dtu.request_id
            LEFT JOIN document_transaction dt_alias ON dr.request_id = dt_alias.request_id
            LEFT JOIN claiming_information ci ON dr.request_id = ci.request_id
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
