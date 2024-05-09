# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db
# from datetime import date

# AdminApprovalRouter = APIRouter(tags=["Admin Approval"])

# @AdminApprovalRouter.get("/admin_approvals/", response_model=list)
# async def read_admin_approvals(
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT admin_approval_id, request_id, admin_id, approval_date, approved
#         FROM admin_approval
#     """
#     db[0].execute(query)
#     admin_approvals = [{
#         "admin_approval_id": approval[0], "request_id": approval[1], 
#         "admin_id": approval[2], "approval_date": approval[3], 
#         "approved": approval[4]
#     } for approval in db[0].fetchall()]
#     return admin_approvals

# @AdminApprovalRouter.get("/admin_approvals/{admin_approval_id}", response_model=dict)
# async def read_admin_approval(
#     admin_approval_id: int, 
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT admin_approval_id, request_id, admin_id, approval_date, approved
#         FROM admin_approval
#         WHERE admin_approval_id = %s
#     """
#     db[0].execute(query, (admin_approval_id,))
#     admin_approval = db[0].fetchone()
#     if admin_approval:
#         return {
#             "admin_approval_id": admin_approval[0], "request_id": admin_approval[1], 
#             "admin_id": admin_approval[2], "approval_date": admin_approval[3], 
#             "approved": admin_approval[4]
#         }
#     raise HTTPException(status_code=404, detail="Admin approval not found")

# @AdminApprovalRouter.post("/admin_approvals/", response_model=dict)
# async def create_admin_approval(
#     request_id: int, 
#     admin_id: int,
#     approval_date: date = None,
#     approved: str = "To be approved",
#     db=Depends(get_db)
# ):
#     query = """
#         INSERT INTO admin_approval (request_id, admin_id, approval_date, approved) 
#         VALUES (%s, %s, %s, %s)
#     """
#     db[0].execute(query, (request_id, admin_id, approval_date, approved))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_admin_approval_id = db[0].fetchone()[0]
#     db[1].commit()

#     return {
#         "admin_approval_id": new_admin_approval_id, "request_id": request_id, 
#         "admin_id": admin_id, "approval_date": approval_date, "approved": approved
#     }

# @AdminApprovalRouter.put("/admin_approvals/{admin_approval_id}", response_model=dict)
# async def update_admin_approval(
#     admin_approval_id: int,
#     request_id: int, 
#     admin_id: int,
#     approval_date: date = None,
#     approved: str = "To be approved",
#     db=Depends(get_db)
# ):
#     query = """
#         UPDATE admin_approval 
#         SET request_id = %s, admin_id = %s, approval_date = %s, approved = %s 
#         WHERE admin_approval_id = %s
#     """
#     db[0].execute(query, (request_id, admin_id, approval_date, approved, admin_approval_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "Admin approval updated successfully"}
    
#     # If no rows were affected, admin approval not found
#     raise HTTPException(status_code=404, detail="Admin approval not found")

# @AdminApprovalRouter.delete("/admin_approvals/{admin_approval_id}", response_model=dict)
# async def delete_admin_approval(
#     admin_approval_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the admin approval exists
#         query_check_approval = "SELECT admin_approval_id FROM admin_approval WHERE admin_approval_id = %s"
#         db[0].execute(query_check_approval, (admin_approval_id,))
#         existing_approval = db[0].fetchone()

#         if not existing_approval:
#             raise HTTPException(status_code=404, detail="Admin approval not found")

#         # Delete the admin approval
#         query_delete_approval = "DELETE FROM admin_approval WHERE admin_approval_id = %s"
#         db[0].execute(query_delete_approval, (admin_approval_id,))
#         db[1].commit()

#         return {"message": "Admin approval deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()
from fastapi import Depends, HTTPException, APIRouter
from db import get_db
from datetime import date

AdminApprovalRouter = APIRouter(tags=["Admin Approval"])

@AdminApprovalRouter.get("/admin_approvals/", response_model=list)
async def read_admin_approvals(
    db=Depends(get_db)
):
    query = """
        SELECT admin_approval_id, request_id, admin_id, approval_date, approved
        FROM admin_approval
    """
    db[1].execute(query)
    admin_approvals = [{
        "admin_approval_id": approval[0], "request_id": approval[1], 
        "admin_id": approval[2], "approval_date": approval[3], 
        "approved": approval[4]
    } for approval in db[1].fetchall()]
    return admin_approvals

@AdminApprovalRouter.get("/admin_approvals/{admin_approval_id}", response_model=dict)
async def read_admin_approval(
    admin_approval_id: int, 
    db=Depends(get_db)
):
    query = """
        SELECT admin_approval_id, request_id, admin_id, approval_date, approved
        FROM admin_approval
        WHERE admin_approval_id = %s
    """
    db[1].execute(query, (admin_approval_id,))
    admin_approval = db[1].fetchone()
    if admin_approval:
        return {
            "admin_approval_id": admin_approval[0], "request_id": admin_approval[1], 
            "admin_id": admin_approval[2], "approval_date": admin_approval[3], 
            "approved": admin_approval[4]
        }
    raise HTTPException(status_code=404, detail="Admin approval not found")

@AdminApprovalRouter.post("/admin_approvals/", response_model=dict)
async def create_admin_approval(
    request_id: int, 
    admin_id: int,
    approval_date: date = None,
    approved: str = "To be approved",
    db=Depends(get_db)
):
    query = """
        INSERT INTO admin_approval (request_id, admin_id, approval_date, approved) 
        VALUES (%s, %s, %s, %s)
    """
    db[1].execute(query, (request_id, admin_id, approval_date, approved))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[1].execute("SELECT LAST_INSERT_ID()")
    new_admin_approval_id = db[1].fetchone()[0]
    db[0].commit()

    return {
        "admin_approval_id": new_admin_approval_id, "request_id": request_id, 
        "admin_id": admin_id, "approval_date": approval_date, "approved": approved
    }

@AdminApprovalRouter.put("/admin_approvals/{admin_approval_id}", response_model=dict)
async def update_admin_approval(
    admin_approval_id: int,
    request_id: int, 
    admin_id: int,
    approval_date: date = None,
    approved: str = "To be approved",
    db=Depends(get_db)
):
    query = """
        UPDATE admin_approval 
        SET request_id = %s, admin_id = %s, approval_date = %s, approved = %s 
        WHERE admin_approval_id = %s
    """
    db[1].execute(query, (request_id, admin_id, approval_date, approved, admin_approval_id))

    # Check if the update was successful
    if db[1].rowcount > 0:
        db[0].commit()
        return {"message": "Admin approval updated successfully"}
    
    # If no rows were affected, admin approval not found
    raise HTTPException(status_code=404, detail="Admin approval not found")

@AdminApprovalRouter.delete("/admin_approvals/{admin_approval_id}", response_model=dict)
async def delete_admin_approval(
    admin_approval_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the admin approval exists
        query_check_approval = "SELECT admin_approval_id FROM admin_approval WHERE admin_approval_id = %s"
        db[1].execute(query_check_approval, (admin_approval_id,))
        existing_approval = db[1].fetchone()

        if not existing_approval:
            raise HTTPException(status_code=404, detail="Admin approval not found")

        # Delete the admin approval
        query_delete_approval = "DELETE FROM admin_approval WHERE admin_approval_id = %s"
        db[1].execute(query_delete_approval, (admin_approval_id,))
        db[0].commit()

        return {"message": "Admin approval deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[1].close()
