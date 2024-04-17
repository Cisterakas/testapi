from datetime import date
from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

AccountApprovalRouter = APIRouter(tags=["Account Approval"])

@AccountApprovalRouter.get("/account_approvals/", response_model=list)
async def read_account_approvals(
    db=Depends(get_db)
):
    query = """
        SELECT aa.approval_id, aa.user_id, aa.approval_date, aa.approved, 
               u.first_name, u.middle_name, u.last_name, u.suffix, u.email, 
               CASE 
                   WHEN s.user_id IS NOT NULL THEN 'student' 
                   WHEN a.user_id IS NOT NULL THEN 'admin' 
                   ELSE NULL 
               END AS role,
               a.role AS admin_role
        FROM account_approval aa
        INNER JOIN user u ON aa.user_id = u.user_id
        LEFT JOIN student s ON u.user_id = s.user_id
        LEFT JOIN administrator a ON u.user_id = a.user_id
    """
    db[0].execute(query)
    approvals = [{
        "approval_id": row[0], "user_id": row[1], "approval_date": row[2], "approved": row[3],
        "first_name": row[4], "middle_name": row[5], "last_name": row[6], "suffix": row[7], "email": row[8],
        "role": row[9], "admin_role": row[10]
    } for row in db[0].fetchall()]
    return approvals

@AccountApprovalRouter.get("/account_approvals/{approval_id}", response_model=dict)
async def read_account_approval(
    approval_id: int, 
    db=Depends(get_db)
):
    query = """
        SELECT aa.approval_id, aa.user_id, aa.approval_date, aa.approved, 
               u.first_name, u.middle_name, u.last_name, u.suffix, u.email, 
               CASE 
                   WHEN s.user_id IS NOT NULL THEN 'student' 
                   WHEN a.user_id IS NOT NULL THEN 'admin' 
                   ELSE NULL 
               END AS role,
               a.role AS admin_role
        FROM account_approval aa
        INNER JOIN user u ON aa.user_id = u.user_id
        LEFT JOIN student s ON u.user_id = s.user_id
        LEFT JOIN administrator a ON u.user_id = a.user_id
        WHERE aa.approval_id = %s
    """
    db[0].execute(query, (approval_id,))
    approval = db[0].fetchone()
    if approval:
        return {
            "approval_id": approval[0], "user_id": approval[1], "approval_date": approval[2], "approved": approval[3],
            "first_name": approval[4], "middle_name": approval[5], "last_name": approval[6], "suffix": approval[7], "email": approval[8],
            "role": approval[9], "admin_role": approval[10]
        }
    raise HTTPException(status_code=404, detail="Account approval not found")

@AccountApprovalRouter.post("/account_approvals/", response_model=dict)
async def create_account_approval(
    user_id: int, 
    approval_date: date,
    approved: bool = False,
    db=Depends(get_db)
):
    query = "INSERT INTO account_approval (user_id, approval_date, approved) VALUES (%s, %s, %s)"
    db[0].execute(query, (user_id, approval_date, approved))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_approval_id = db[0].fetchone()[0]
    db[1].commit()

    return {"approval_id": new_approval_id, "user_id": user_id, "approval_date": approval_date, "approved": approved}

@AccountApprovalRouter.put("/account_approvals/{approval_id}", response_model=dict)
async def update_account_approval(
    approval_id: int,
    approved: bool,
    db=Depends(get_db)
):
    query = "UPDATE account_approval SET approved = %s WHERE approval_id = %s"
    db[0].execute(query, (approved, approval_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Account approval updated successfully"}
    
    # If no rows were affected, account approval not found
    raise HTTPException(status_code=404, detail="Account approval not found")

@AccountApprovalRouter.delete("/account_approvals/{approval_id}", response_model=dict)
async def delete_account_approval(
    approval_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the account approval exists
        query_check_approval = "SELECT approval_id FROM account_approval WHERE approval_id = %s"
        db[0].execute(query_check_approval, (approval_id,))
        existing_approval = db[0].fetchone()

        if not existing_approval:
            raise HTTPException(status_code=404, detail="Account approval not found")

        # Delete the account approval
        query_delete_approval = "DELETE FROM account_approval WHERE approval_id = %s"
        db[0].execute(query_delete_approval, (approval_id,))
        db[1].commit()

        return {"message": "Account approval deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
