# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db

# UserTransactionHistoryRouter = APIRouter(tags=["User Transaction History"])

# @UserTransactionHistoryRouter.get("/user_transaction_history/", response_model=list)
# async def read_user_transaction_history(
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT transaction_id, user_id, request_id, total_amount_paid, receipt_link
#         FROM user_transaction_history
#     """
#     db[0].execute(query)
#     user_transaction_history = [{
#         "transaction_id": info[0], "user_id": info[1], "request_id": info[2], 
#         "total_amount_paid": float(info[3]), "receipt_link": info[4]
#     } for info in db[0].fetchall()]
#     return user_transaction_history

# @UserTransactionHistoryRouter.get("/user_transaction_history/{transaction_id}", response_model=dict)
# async def read_user_transaction_history_by_id(
#     transaction_id: int, 
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT transaction_id, user_id, request_id, total_amount_paid, receipt_link
#         FROM user_transaction_history
#         WHERE transaction_id = %s
#     """
#     db[0].execute(query, (transaction_id,))
#     transaction_info = db[0].fetchone()
#     if transaction_info:
#         return {
#             "transaction_id": transaction_info[0], "user_id": transaction_info[1], 
#             "request_id": transaction_info[2], "total_amount_paid": float(transaction_info[3]), 
#             "receipt_link": transaction_info[4]
#         }
#     raise HTTPException(status_code=404, detail="User transaction history not found")

# @UserTransactionHistoryRouter.post("/user_transaction_history/", response_model=dict)
# async def create_user_transaction_history(
#     user_id: int, 
#     total_amount_paid: float,
#     request_id: int = None,
#     receipt_link: str = None,
#     db=Depends(get_db)
# ):
#     query = """
#         INSERT INTO user_transaction_history 
#         (user_id, request_id, total_amount_paid, receipt_link) 
#         VALUES (%s, %s, %s, %s)
#     """
#     db[0].execute(query, (user_id, request_id, total_amount_paid, receipt_link))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_transaction_id = db[0].fetchone()[0]
#     db[1].commit()

#     return {
#         "transaction_id": new_transaction_id, "user_id": user_id, 
#         "request_id": request_id, "total_amount_paid": total_amount_paid, 
#         "receipt_link": receipt_link
#     }

# @UserTransactionHistoryRouter.put("/user_transaction_history/{transaction_id}", response_model=dict)
# async def update_user_transaction_history(
#     transaction_id: int,
#     user_id: int, 
#     total_amount_paid: float,
#     request_id: int = None,
#     receipt_link: str = None,
#     db=Depends(get_db)
# ):
#     query = """
#         UPDATE user_transaction_history 
#         SET user_id = %s, request_id = %s, total_amount_paid = %s, receipt_link = %s 
#         WHERE transaction_id = %s
#     """
#     db[0].execute(query, (user_id, request_id, total_amount_paid, receipt_link, transaction_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "User transaction history updated successfully"}
    
#     # If no rows were affected, user transaction history not found
#     raise HTTPException(status_code=404, detail="User transaction history not found")

# @UserTransactionHistoryRouter.delete("/user_transaction_history/{transaction_id}", response_model=dict)
# async def delete_user_transaction_history(
#     transaction_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the user transaction history exists
#         query_check_info = "SELECT transaction_id FROM user_transaction_history WHERE transaction_id = %s"
#         db[0].execute(query_check_info, (transaction_id,))
#         existing_info = db[0].fetchone()

#         if not existing_info:
#             raise HTTPException(status_code=404, detail="User transaction history not found")

#         # Delete the user transaction history
#         query_delete_info = "DELETE FROM user_transaction_history WHERE transaction_id = %s"
#         db[0].execute(query_delete_info, (transaction_id,))
#         db[1].commit()

#         return {"message": "User transaction history deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()
from fastapi import Depends, HTTPException, APIRouter
from db import get_db

UserTransactionHistoryRouter = APIRouter(tags=["User Transaction History"])

@UserTransactionHistoryRouter.get("/user_transaction_history/", response_model=list)
async def read_user_transaction_history(
    db=Depends(get_db)
):
    try:
        query = """
            SELECT transaction_id, user_id, request_id, total_amount_paid, receipt_link
            FROM user_transaction_history
        """
        db[1].execute(query)
        user_transaction_history = [{
            "transaction_id": info[0], "user_id": info[1], "request_id": info[2], 
            "total_amount_paid": float(info[3]), "receipt_link": info[4]
        } for info in db[1].fetchall()]
        return user_transaction_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@UserTransactionHistoryRouter.get("/user_transaction_history/{transaction_id}", response_model=dict)
async def read_user_transaction_history_by_id(
    transaction_id: int, 
    db=Depends(get_db)
):
    try:
        query = """
            SELECT transaction_id, user_id, request_id, total_amount_paid, receipt_link
            FROM user_transaction_history
            WHERE transaction_id = %s
        """
        db[1].execute(query, (transaction_id,))
        transaction_info = db[1].fetchone()
        if transaction_info:
            return {
                "transaction_id": transaction_info[0], "user_id": transaction_info[1], 
                "request_id": transaction_info[2], "total_amount_paid": float(transaction_info[3]), 
                "receipt_link": transaction_info[4]
            }
        raise HTTPException(status_code=404, detail="User transaction history not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@UserTransactionHistoryRouter.post("/user_transaction_history/", response_model=dict)
async def create_user_transaction_history(
    user_id: int, 
    total_amount_paid: float,
    request_id: int = None,
    receipt_link: str = None,
    db=Depends(get_db)
):
    try:
        query = """
            INSERT INTO user_transaction_history 
            (user_id, request_id, total_amount_paid, receipt_link) 
            VALUES (%s, %s, %s, %s)
        """
        db[1].execute(query, (user_id, request_id, total_amount_paid, receipt_link))

        # Retrieve the last inserted ID using LAST_INSERT_ID()
        db[1].execute("SELECT LAST_INSERT_ID()")
        new_transaction_id = db[1].fetchone()[0]
        db[0].commit()

        return {
            "transaction_id": new_transaction_id, "user_id": user_id, 
            "request_id": request_id, "total_amount_paid": total_amount_paid, 
            "receipt_link": receipt_link
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@UserTransactionHistoryRouter.put("/user_transaction_history/{transaction_id}", response_model=dict)
async def update_user_transaction_history(
    transaction_id: int,
    user_id: int, 
    total_amount_paid: float,
    request_id: int = None,
    receipt_link: str = None,
    db=Depends(get_db)
):
    try:
        query = """
            UPDATE user_transaction_history 
            SET user_id = %s, request_id = %s, total_amount_paid = %s, receipt_link = %s 
            WHERE transaction_id = %s
        """
        db[1].execute(query, (user_id, request_id, total_amount_paid, receipt_link, transaction_id))

        # Check if the update was successful
        if db[1].rowcount > 0:
            db[0].commit()
            return {"message": "User transaction history updated successfully"}
        
        # If no rows were affected, user transaction history not found
        raise HTTPException(status_code=404, detail="User transaction history not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@UserTransactionHistoryRouter.delete("/user_transaction_history/{transaction_id}", response_model=dict)
async def delete_user_transaction_history(
    transaction_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user transaction history exists
        query_check_info = "SELECT transaction_id FROM user_transaction_history WHERE transaction_id = %s"
        db[1].execute(query_check_info, (transaction_id,))
        existing_info = db[1].fetchone()

        if not existing_info:
            raise HTTPException(status_code=404, detail="User transaction history not found")

        # Delete the user transaction history
        query_delete_info = "DELETE FROM user_transaction_history WHERE transaction_id = %s"
        db[1].execute(query_delete_info, (transaction_id,))
        db[0].commit()

        return {"message": "User transaction history deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[1].close()
        db[0].close()
