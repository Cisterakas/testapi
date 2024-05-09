# from fastapi import Depends, HTTPException, APIRouter, Form
# import bcrypt
# from db import get_db

# AddAdminUserRouter = APIRouter(tags=["Add Admin User"])

# @AddAdminUserRouter.get("/addadminusers/", response_model=list)
# async def read_add_admin_users(
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT
#             u.first_name,
#             u.middle_name,
#             u.last_name,
#             u.suffix,
#             u.email,
#             u.password,
#             COALESCE(a.role, 'Student') AS role,
#             u.registration_date
#         FROM
#             user u
#         LEFT JOIN
#             administrator a ON u.user_id = a.user_id;
#     """
#     db[0].execute(query)
#     users = [{
#         "first_name": row[0], "middle_name": row[1], "last_name": row[2], "suffix": row[3],
#         "email": row[4], "password": row[5], "role": row[6], "registration_date": row[7]
#     } for row in db[0].fetchall()]
#     return users

# @AddAdminUserRouter.get("/addadminusers/{user_id}", response_model=dict)
# async def read_specific_admin_user(
#     user_id: int,
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT
#             u.first_name,
#             u.middle_name,
#             u.last_name,
#             u.suffix,
#             u.email,
#             u.password,
#             COALESCE(a.role, 'Student') AS role,
#             u.registration_date
#         FROM
#             user u
#         LEFT JOIN
#             administrator a ON u.user_id = a.user_id
#         WHERE
#             u.user_id = %s;
#     """
#     db[0].execute(query, (user_id,))
#     user = db[0].fetchone()
#     if user:
#         return {
#             "first_name": user[0], "middle_name": user[1], "last_name": user[2], "suffix": user[3],
#             "email": user[4], "password": user[5], "role": user[6], "registration_date": user[7]
#         }
#     raise HTTPException(status_code=404, detail="User not found")

# @AddAdminUserRouter.post("/addadminusers/", response_model=dict)
# async def create_add_admin_user(
#     first_name: str = Form(...), 
#     middle_name: str = Form(None), 
#     last_name: str = Form(...), 
#     suffix: str = Form(None), 
#     email: str = Form(...), 
#     password: str = Form(...), 
#     role: str = Form("Student"), 
#     db=Depends(get_db)
# ):
#     hashed_password = hash_password(password)

#     query_user = """
#         INSERT INTO user (first_name, middle_name, last_name, suffix, email, password, registration_date) 
#         VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
#     """
#     db[0].execute(query_user, (first_name, middle_name, last_name, suffix, email, hashed_password))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_user_id = db[0].fetchone()[0]

#     query_admin = """
#         INSERT INTO administrator (user_id, role) 
#         VALUES (%s, %s)
#     """
#     db[0].execute(query_admin, (new_user_id, role))

#     db[1].commit()

#     return {"user_id": new_user_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, 
#             "suffix": suffix, "email": email, "role": role}

# @AddAdminUserRouter.put("/addadminusers/{user_id}", response_model=dict)
# async def update_add_admin_user(
#     user_id: int,
#     first_name: str = Form(...),
#     middle_name: str = Form(None),
#     last_name: str = Form(...),
#     suffix: str = Form(None),
#     email: str = Form(...),
#     password: str = Form(...),
#     role: str = Form("Student"),
#     db=Depends(get_db)
# ):
#     hashed_password = hash_password(password)

#     query_user = """
#         UPDATE user 
#         SET first_name = %s, middle_name = %s, last_name = %s, suffix = %s, email = %s, password = %s 
#         WHERE user_id = %s
#     """
#     db[0].execute(query_user, (first_name, middle_name, last_name, suffix, email, hashed_password, user_id))

#     query_admin = """
#         UPDATE administrator 
#         SET role = %s 
#         WHERE user_id = %s
#     """
#     db[0].execute(query_admin, (role, user_id))

#     db[1].commit()

#     return {"message": "User updated successfully"}

# @AddAdminUserRouter.delete("/addadminusers/{user_id}", response_model=dict)
# async def delete_add_admin_user(
#     user_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         query_delete_admin = "DELETE FROM administrator WHERE user_id = %s"
#         db[0].execute(query_delete_admin, (user_id,))

#         query_delete_user = "DELETE FROM user WHERE user_id = %s"
#         db[0].execute(query_delete_user, (user_id,))

#         db[1].commit()

#         return {"message": "User deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# def hash_password(password: str):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')
from fastapi import Depends, HTTPException, APIRouter, Form
from db import get_db

AddAdminUserRouter = APIRouter(tags=["Add Admin User"])

@AddAdminUserRouter.get("/addadminusers/", response_model=list)
async def read_add_admin_users(
    db=Depends(get_db)
):
    query = """
        SELECT
            u.first_name,
            u.middle_name,
            u.last_name,
            u.suffix,
            u.email,
            u.password,
            COALESCE(a.role, 'Student') AS role,
            u.registration_date
        FROM
            user u
        LEFT JOIN
            administrator a ON u.user_id = a.user_id;
    """
    db[1].execute(query)
    users = [{
        "first_name": row[0], "middle_name": row[1], "last_name": row[2], "suffix": row[3],
        "email": row[4], "password": row[5], "role": row[6], "registration_date": row[7]
    } for row in db[1].fetchall()]
    return users

@AddAdminUserRouter.get("/addadminusers/{user_id}", response_model=dict)
async def read_specific_admin_user(
    user_id: int,
    db=Depends(get_db)
):
    query = """
        SELECT
            u.first_name,
            u.middle_name,
            u.last_name,
            u.suffix,
            u.email,
            u.password,
            COALESCE(a.role, 'Student') AS role,
            u.registration_date
        FROM
            user u
        LEFT JOIN
            administrator a ON u.user_id = a.user_id
        WHERE
            u.user_id = %s;
    """
    db[1].execute(query, (user_id,))
    user = db[1].fetchone()
    if user:
        return {
            "first_name": user[0], "middle_name": user[1], "last_name": user[2], "suffix": user[3],
            "email": user[4], "password": user[5], "role": user[6], "registration_date": user[7]
        }
    raise HTTPException(status_code=404, detail="User not found")

@AddAdminUserRouter.post("/addadminusers/", response_model=dict)
async def create_add_admin_user(
    first_name: str = Form(...), 
    middle_name: str = Form(None), 
    last_name: str = Form(...), 
    suffix: str = Form(None), 
    email: str = Form(...), 
    password: str = Form(...), 
    role: str = Form("Student"), 
    db=Depends(get_db)
):
    query_user = """
        INSERT INTO user (first_name, middle_name, last_name, suffix, email, password, registration_date) 
        VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
    """
    db[1].execute(query_user, (first_name, middle_name, last_name, suffix, email, password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[1].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[1].fetchone()[0]

    query_admin = """
        INSERT INTO administrator (user_id, role) 
        VALUES (%s, %s)
    """
    db[1].execute(query_admin, (new_user_id, role))

    db[0].commit()

    return {"user_id": new_user_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, 
            "suffix": suffix, "email": email, "role": role}

@AddAdminUserRouter.put("/addadminusers/{user_id}", response_model=dict)
async def update_add_admin_user(
    user_id: int,
    first_name: str = Form(...),
    middle_name: str = Form(None),
    last_name: str = Form(...),
    suffix: str = Form(None),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("Student"),
    db=Depends(get_db)
):
    query_user = """
        UPDATE user 
        SET first_name = %s, middle_name = %s, last_name = %s, suffix = %s, email = %s, password = %s 
        WHERE user_id = %s
    """
    db[1].execute(query_user, (first_name, middle_name, last_name, suffix, email, password, user_id))

    query_admin = """
        UPDATE administrator 
        SET role = %s 
        WHERE user_id = %s
    """
    db[1].execute(query_admin, (role, user_id))

    db[0].commit()

    return {"message": "User updated successfully"}

@AddAdminUserRouter.delete("/addadminusers/{user_id}", response_model=dict)
async def delete_add_admin_user(
    user_id: int,
    db=Depends(get_db)
):
    try:
        query_delete_admin = "DELETE FROM administrator WHERE user_id = %s"
        db[1].execute(query_delete_admin, (user_id,))

        query_delete_user = "DELETE FROM user WHERE user_id = %s"
        db[1].execute(query_delete_user, (user_id,))

        db[0].commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
