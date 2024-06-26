from datetime import date
from fastapi import Depends, HTTPException, APIRouter, Body
from pydantic import BaseModel
from db import get_db
class UpdateApprovalStatusRequest(BaseModel):
    user_id: int
    approved: str

NewAccountsRouter = APIRouter(tags=["New Accounts"])

@NewAccountsRouter.get("/new_accounts/", response_model=list)
async def read_new_accounts(db=Depends(get_db)):
    try:
        query = """
            SELECT
                u.user_id,
                COALESCE(s.student_school_id, '') AS student_school_id,
                u.first_name,
                COALESCE(u.middle_name, '') AS middle_name,
                u.last_name,
                COALESCE(u.suffix, '') AS suffix,
                CASE
                    WHEN s.degree IS NOT NULL THEN s.degree
                    ELSE ''
                END AS degree,
                u.email,
                u.registration_date,
                CASE
                    WHEN a.role IS NULL THEN 'Student'
                    ELSE a.role
                END AS role,
                aa.approved AS account_approval_status,
                s.contact,
                s.address,
                s.last_school_year
            FROM
                user u
            LEFT JOIN
                student s ON u.user_id = s.user_id
            LEFT JOIN
                administrator a ON u.user_id = a.user_id
            LEFT JOIN
                account_approval aa ON u.user_id = aa.user_id
            WHERE
                s.user_id IS NOT NULL;
        """
        cursor = db[1]
        cursor.execute(query)
        new_accounts = [{
            "user_id": row[0], "student_school_id": row[1], "first_name": row[2], "middle_name": row[3], "last_name": row[4], "suffix": row[5],
            "degree": row[6], "email": row[7], "registration_date": row[8], "role": row[9], "account_approval_status": row[10],
            "contact": row[11], "address": row[12], "last_school_year": row[13]
        } for row in cursor.fetchall()]
        return new_accounts
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.get("/admin_accounts/", response_model=list)
async def read_admin_accounts(db=Depends(get_db)):
    try:
        query = """
            SELECT
                u.user_id,
                u.first_name,
                COALESCE(u.middle_name, '') AS middle_name,
                u.last_name,
                COALESCE(u.suffix, '') AS suffix,
                u.email,
                u.password,
                u.registration_date,
                a.role,
                aa.approved AS account_approval_status
            FROM
                user u
            LEFT JOIN
                administrator a ON u.user_id = a.user_id
            LEFT JOIN
                account_approval aa ON u.user_id = aa.user_id
            WHERE
                a.role IS NOT NULL;
        """
        cursor = db[1]
        cursor.execute(query)
        admin_accounts = [{
            "user_id": row[0], "first_name": row[1], "middle_name": row[2], "last_name": row[3], "suffix": row[4],
            "email": row[5], "password": row[6], "registration_date": row[7], "role": row[8], "account_approval_status": row[9]
        } for row in cursor.fetchall()]
        return admin_accounts
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.get("/new_accounts/{user_id}", response_model=dict)
async def read_new_account(user_id: int, db=Depends(get_db)):
    try:
        query = """
            SELECT
                COALESCE(s.student_school_id, '') AS student_school_id,
                u.first_name,
                COALESCE(u.middle_name, '') AS middle_name,
                u.last_name,
                COALESCE(u.suffix, '') AS suffix,
                CASE
                    WHEN s.degree IS NOT NULL THEN s.degree
                    ELSE ''
                END AS degree,
                u.email,
                u.registration_date,
                CASE
                    WHEN a.role IS NULL THEN 'Student'
                    ELSE a.role
                END AS role,
                aa.approved AS account_approval_status
            FROM
                user u
            LEFT JOIN
                student s ON u.user_id = s.user_id
            LEFT JOIN
                administrator a ON u.user_id = a.user_id
            LEFT JOIN
                account_approval aa ON u.user_id = aa.user_id
            WHERE u.user_id = %s;
        """
        cursor = db[1]
        cursor.execute(query, (user_id,))
        new_account = cursor.fetchone()
        if new_account:
            return {
                "student_school_id": new_account[0], "first_name": new_account[1], "middle_name": new_account[2], "last_name": new_account[3], "suffix": new_account[4],
                "degree": new_account[5], "email": new_account[6], "registration_date": new_account[7], "role": new_account[8], "account_approval_status": new_account[9]
            }
        raise HTTPException(status_code=404, detail="New account not found")
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.post("/new_accounts/", response_model=dict)
async def create_new_account(
    user_id: int,
    student_school_id: str,
    first_name: str,
    last_name: str,
    email: str,
    registration_date: date,
    middle_name: str = '',
    suffix: str = '',
    degree: str = '',
    role: str = 'Student',
    account_approval_status: bool = False,
    db=Depends(get_db)
):
    try:
        query_user = "INSERT INTO user (user_id, first_name, middle_name, last_name, suffix, email, registration_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor = db[1]
        cursor.execute(query_user, (user_id, first_name, middle_name, last_name, suffix, email, registration_date))

        query_student = "INSERT INTO student (user_id, student_school_id, degree) VALUES (%s, %s, %s)"
        cursor.execute(query_student, (user_id, student_school_id, degree))

        query_approval = "INSERT INTO account_approval (user_id, approved) VALUES (%s, %s)"
        cursor.execute(query_approval, (user_id, account_approval_status))

        db[0].commit()

        return {
            "user_id": user_id, "student_school_id": student_school_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, "suffix": suffix,
            "degree": degree, "email": email, "registration_date": registration_date, "role": role, "account_approval_status": account_approval_status
        }
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.put("/new_accounts/{user_id}", response_model=dict)
async def update_new_account(
    user_id: int,
    first_name: str,
    last_name: str,
    email: str,
    student_school_id: str = '',
    middle_name: str = '',
    suffix: str = '',
    degree: str = '',
    role: str = 'Student',
    account_approval_status: bool = False,
    db=Depends(get_db)
):
    try:
        query_user = "UPDATE user SET first_name = %s, middle_name = %s, last_name = %s, suffix = %s, email = %s WHERE user_id = %s"
        cursor = db[1]
        cursor.execute(query_user, (first_name, middle_name, last_name, suffix, email, user_id))

        query_student = "UPDATE student SET student_school_id = %s, degree = %s WHERE user_id = %s"
        cursor.execute(query_student, (student_school_id, degree, user_id))

        if account_approval_status:
            query_approval = "UPDATE account_approval SET approved = %s WHERE user_id = %s"
            cursor.execute(query_approval, (account_approval_status, user_id))

        db[0].commit()

        return {
            "user_id": user_id, "student_school_id": student_school_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, "suffix": suffix,
            "degree": degree, "email": email, "role": role, "account_approval_status": account_approval_status
        }
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.delete("/new_accounts/{user_id}", response_model=dict)
async def delete_new_account(
    user_id: int,
    db=Depends(get_db)
):
    try:
        cursor = db[1]
        query_delete_approval = "DELETE FROM account_approval WHERE user_id = %s"
        cursor.execute(query_delete_approval, (user_id,))

        query_delete_student = "DELETE FROM student WHERE user_id = %s"
        cursor.execute(query_delete_student, (user_id,))

        query_delete_user = "DELETE FROM user WHERE user_id = %s"
        cursor.execute(query_delete_user, (user_id,))

        db[0].commit()

        return {"message": "New account deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.put("/new_accounts/{user_id}/approve", response_model=dict)
async def approve_new_account(
    user_id: int,
    approval_date: date,
    approved: str = 'TRUE',  # Set the default value to 'TRUE'
    db=Depends(get_db)
):
    try:
        cursor = db[1]
        # Check if an approval record already exists for the user
        query_check_approval = "SELECT approval_id FROM account_approval WHERE user_id = %s"
        cursor.execute(query_check_approval, (user_id,))
        existing_approval = cursor.fetchone()

        if existing_approval:
            # Update the existing approval record
            query_update_approval = "UPDATE account_approval SET approval_date = %s, approved = %s WHERE user_id = %s"
            cursor.execute(query_update_approval, (approval_date, approved, user_id))
            db[0].commit()
            return {"message": f"Account approval for user ID {user_id} has been updated successfully."}
        else:
            # Create a new approval record
            query_create_approval = "INSERT INTO account_approval (user_id, approval_date, approved) VALUES (%s, %s, %s)"
            cursor.execute(query_create_approval, (user_id, approval_date, approved))

            # Retrieve the last inserted ID using LAST_INSERT_ID()
            cursor.execute("SELECT LAST_INSERT_ID()")
            new_approval_id = cursor.fetchone()[0]
            db[0].commit()

            return {"message": f"Account for user ID {user_id} has been approved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()

@NewAccountsRouter.put("/update_approval_status/")
async def update_approval_status(request: UpdateApprovalStatusRequest, db=Depends(get_db)):
    try:
        query = """
            UPDATE account_approval
            SET approved = %s
            WHERE user_id = %s;
        """
        cursor = db[1]
        cursor.execute(query, (request.approved, request.user_id))
        db[0].commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Account approval status updated successfully"}
    finally:
        # Ensure to close the cursor and connection
        db[1].close()
        db[0].close()
