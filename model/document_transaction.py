# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db
# from datetime import date

# DocumentTransactionRouter = APIRouter(tags=["Document Transaction"])

# @DocumentTransactionRouter.get("/document_transactions/", response_model=list)
# async def read_document_transactions(
#     db=Depends(get_db)
# ):
#     query = "SELECT transaction_id, request_id, payment_date FROM document_transaction"
#     db[0].execute(query)
#     document_transactions = [{
#         "transaction_id": transaction[0], "request_id": transaction[1], 
#         "payment_date": transaction[2]
#     } for transaction in db[0].fetchall()]
#     return document_transactions

# @DocumentTransactionRouter.get("/document_transactions/{transaction_id}", response_model=dict)
# async def read_document_transaction(
#     transaction_id: int, 
#     db=Depends(get_db)
# ):
#     query = "SELECT transaction_id, request_id, payment_date FROM document_transaction WHERE transaction_id = %s"
#     db[0].execute(query, (transaction_id,))
#     document_transaction = db[0].fetchone()
#     if document_transaction:
#         return {
#             "transaction_id": document_transaction[0], "request_id": document_transaction[1], 
#             "payment_date": document_transaction[2]
#         }
#     raise HTTPException(status_code=404, detail="Document transaction not found")

# @DocumentTransactionRouter.post("/document_transactions/", response_model=dict)
# async def create_document_transaction(
#     request_id: int, 
#     payment_date: date,
#     db=Depends(get_db)
# ):
#     query = "INSERT INTO document_transaction (request_id, payment_date) VALUES (%s, %s)"
#     db[0].execute(query, (request_id, payment_date))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_transaction_id = db[0].fetchone()[0]
#     db[1].commit()

#     return {
#         "transaction_id": new_transaction_id, "request_id": request_id, 
#         "payment_date": payment_date
#     }

# @DocumentTransactionRouter.put("/document_transactions/{transaction_id}", response_model=dict)
# async def update_document_transaction(
#     transaction_id: int,
#     request_id: int, 
#     payment_date: date,
#     db=Depends(get_db)
# ):
#     query = "UPDATE document_transaction SET request_id = %s, payment_date = %s WHERE transaction_id = %s"
#     db[0].execute(query, (request_id, payment_date, transaction_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "Document transaction updated successfully"}
    
#     # If no rows were affected, document transaction not found
#     raise HTTPException(status_code=404, detail="Document transaction not found")

# @DocumentTransactionRouter.delete("/document_transactions/{transaction_id}", response_model=dict)
# async def delete_document_transaction(
#     transaction_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the document transaction exists
#         query_check_transaction = "SELECT transaction_id FROM document_transaction WHERE transaction_id = %s"
#         db[0].execute(query_check_transaction, (transaction_id,))
#         existing_transaction = db[0].fetchone()

#         if not existing_transaction:
#             raise HTTPException(status_code=404, detail="Document transaction not found")

#         # Delete the document transaction
#         query_delete_transaction = "DELETE FROM document_transaction WHERE transaction_id = %s"
#         db[0].execute(query_delete_transaction, (transaction_id,))
#         db[1].commit()

#         return {"message": "Document transaction deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()

from fastapi import Depends, HTTPException, APIRouter
from db import get_db
from datetime import date

DocumentTransactionRouter = APIRouter(tags=["Document Transaction"])

@DocumentTransactionRouter.get("/document_transactions/", response_model=list)
async def read_document_transactions(
    db=Depends(get_db)
):
    query = "SELECT transaction_id, request_id, payment_date FROM document_transaction"
    db[1].execute(query)
    document_transactions = [{
        "transaction_id": transaction[0], "request_id": transaction[1], 
        "payment_date": transaction[2]
    } for transaction in db[1].fetchall()]
    return document_transactions

@DocumentTransactionRouter.get("/document_transactions/{transaction_id}", response_model=dict)
async def read_document_transaction(
    transaction_id: int, 
    db=Depends(get_db)
):
    query = "SELECT transaction_id, request_id, payment_date FROM document_transaction WHERE transaction_id = %s"
    db[1].execute(query, (transaction_id,))
    document_transaction = db[1].fetchone()
    if document_transaction:
        return {
            "transaction_id": document_transaction[0], "request_id": document_transaction[1], 
            "payment_date": document_transaction[2]
        }
    raise HTTPException(status_code=404, detail="Document transaction not found")

@DocumentTransactionRouter.post("/document_transactions/", response_model=dict)
async def create_document_transaction(
    request_id: int, 
    payment_date: date,
    db=Depends(get_db)
):
    query = "INSERT INTO document_transaction (request_id, payment_date) VALUES (%s, %s)"
    db[1].execute(query, (request_id, payment_date))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[1].execute("SELECT LAST_INSERT_ID()")
    new_transaction_id = db[1].fetchone()[0]
    db[0].commit()

    return {
        "transaction_id": new_transaction_id, "request_id": request_id, 
        "payment_date": payment_date
    }

@DocumentTransactionRouter.put("/document_transactions/{transaction_id}", response_model=dict)
async def update_document_transaction(
    transaction_id: int,
    request_id: int, 
    payment_date: date,
    db=Depends(get_db)
):
    query = "UPDATE document_transaction SET request_id = %s, payment_date = %s WHERE transaction_id = %s"
    db[1].execute(query, (request_id, payment_date, transaction_id))

    # Check if the update was successful
    if db[1].rowcount > 0:
        db[0].commit()
        return {"message": "Document transaction updated successfully"}
    
    # If no rows were affected, document transaction not found
    raise HTTPException(status_code=404, detail="Document transaction not found")

@DocumentTransactionRouter.delete("/document_transactions/{transaction_id}", response_model=dict)
async def delete_document_transaction(
    transaction_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the document transaction exists
        query_check_transaction = "SELECT transaction_id FROM document_transaction WHERE transaction_id = %s"
        db[1].execute(query_check_transaction, (transaction_id,))
        existing_transaction = db[1].fetchone()

        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Document transaction not found")

        # Delete the document transaction
        query_delete_transaction = "DELETE FROM document_transaction WHERE transaction_id = %s"
        db[1].execute(query_delete_transaction, (transaction_id,))
        db[0].commit()

        return {"message": "Document transaction deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[1].close()
