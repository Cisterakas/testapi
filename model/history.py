from fastapi import APIRouter, Depends, HTTPException
from db import get_db

HistoryDocumentsRouter = APIRouter(tags=["History Documents"])

@HistoryDocumentsRouter.get("/history")
async def get_all_document_requests(db=Depends(get_db)):
    try:
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
        """

        cursor.execute(query)
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
            raise HTTPException(status_code=404, detail="No document requests found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@HistoryDocumentsRouter.get("/history/received")
async def get_received_document_requests(db=Depends(get_db)):
    try:
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
            dr.status = 'Received'
        """

        cursor.execute(query)
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
            raise HTTPException(status_code=404, detail="No document requests found with status 'Received'")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
