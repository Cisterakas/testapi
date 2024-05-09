# from fastapi import Depends, HTTPException, APIRouter, Form
# import bcrypt
# from db import get_db

# AddStudentUserRouter = APIRouter(tags=["Add Student User"])

# @AddStudentUserRouter.get("/addusers/email-exists/")
# async def check_email_exists(email: str, db=Depends(get_db)):
#     query = "SELECT COUNT(*) FROM user WHERE email = %s"
#     db[0].execute(query, (email,))
#     result = db[0].fetchone()[0]
#     return {"email_exists": result > 0}

# @AddStudentUserRouter.get("/addusers/student-school-id-exists/")
# async def check_student_school_id_exists(student_school_id: str, db=Depends(get_db)):
#     query = "SELECT COUNT(*) FROM student WHERE student_school_id = %s"
#     db[0].execute(query, (student_school_id,))
#     result = db[0].fetchone()[0]
#     return {"student_school_id_exists": result > 0}

# @AddStudentUserRouter.get("/addusers/", response_model=list)
# async def read_add_users(
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT
#             COALESCE(s.student_school_id, '') AS student_school_id,
#             u.first_name,
#             COALESCE(u.middle_name, '') AS middle_name,
#             u.last_name,
#             COALESCE(u.suffix, '') AS suffix,
#             COALESCE(s.address, '') AS address,
#             COALESCE(s.contact, '') AS contact,
#             COALESCE(s.last_school_year, '') AS last_school_year,
#             COALESCE(s.degree, '') AS degree,
#             u.email,
#             u.registration_date
#         FROM
#             user u
#         LEFT JOIN
#             student s ON u.user_id = s.user_id;
#     """
#     db[0].execute(query)
#     users = [{
#         "student_school_id": row[0], "first_name": row[1], "middle_name": row[2], "last_name": row[3], "suffix": row[4],
#         "address": row[5], "contact": row[6], "last_school_year": row[7], "degree": row[8], "email": row[9], "registration_date": row[10]
#     } for row in db[0].fetchall()]
#     return users

# @AddStudentUserRouter.get("/addusers/{user_id}", response_model=dict)
# async def read_specific_user(
#     user_id: int,
#     db=Depends(get_db)
# ):
#     query = """
#         SELECT
#             COALESCE(s.student_school_id, '') AS student_school_id,
#             u.first_name,
#             COALESCE(u.middle_name, '') AS middle_name,
#             u.last_name,
#             COALESCE(u.suffix, '') AS suffix,
#             COALESCE(s.address, '') AS address,
#             COALESCE(s.contact, '') AS contact,
#             COALESCE(s.last_school_year, '') AS last_school_year,
#             COALESCE(s.degree, '') AS degree,
#             u.email,
#             u.registration_date
#         FROM
#             user u
#         LEFT JOIN
#             student s ON u.user_id = s.user_id
#         WHERE
#             u.user_id = %s;
#     """
#     db[0].execute(query, (user_id,))
#     user = db[0].fetchone()
#     if user:
#         return {
#             "student_school_id": user[0], "first_name": user[1], "middle_name": user[2], "last_name": user[3], "suffix": user[4],
#             "address": user[5], "contact": user[6], "last_school_year": user[7], "degree": user[8], "email": user[9], "registration_date": user[10]
#         }
#     raise HTTPException(status_code=404, detail="User not found")

# @AddStudentUserRouter.post("/addusers/", response_model=dict)
# async def create_add_user(
#     student_school_id: str = Form(None),
#     first_name: str = Form(...), 
#     middle_name: str = Form(None), 
#     last_name: str = Form(...), 
#     suffix: str = Form(None), 
#     address: str = Form(None), 
#     contact: str = Form(None), 
#     last_school_year: str = Form(None), 
#     degree: str = Form(None), 
#     email: str = Form(...), 
#     password: str = Form(...), 
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

#     query_student = """
#         INSERT INTO student (user_id, student_school_id, address, contact, last_school_year, degree) 
#         VALUES (%s, %s, %s, %s, %s, %s)
#     """
#     db[0].execute(query_student, (new_user_id, student_school_id, address, contact, last_school_year, degree))

#     db[1].commit()

#     return {"user_id": new_user_id, "student_school_id": student_school_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, 
#             "suffix": suffix, "address": address, "contact": contact, "last_school_year": last_school_year, 
#             "degree": degree, "email": email}

# @AddStudentUserRouter.put("/addusers/{user_id}", response_model=dict)
# async def update_add_user(
#     user_id: int,
#     first_name: str = Form(...),
#     middle_name: str = Form(None),
#     last_name: str = Form(...),
#     suffix: str = Form(None),
#     address: str = Form(None),
#     contact: str = Form(None),
#     last_school_year: str = Form(None),
#     degree: str = Form(None),
#     email: str = Form(...),
#     password: str = Form(...),
#     db=Depends(get_db)
# ):
#     hashed_password = hash_password(password)

#     query_user = """
#         UPDATE user 
#         SET first_name = %s, middle_name = %s, last_name = %s, suffix = %s, email = %s, password = %s 
#         WHERE user_id = %s
#     """
#     db[0].execute(query_user, (first_name, middle_name, last_name, suffix, email, hashed_password, user_id))

#     query_student = """
#         UPDATE student 
#         SET address = %s, contact = %s, last_school_year = %s, degree = %s 
#         WHERE user_id = %s
#     """
#     db[0].execute(query_student, (address, contact, last_school_year, degree, user_id))

#     db[1].commit()

#     return {"message": "User updated successfully"}

# @AddStudentUserRouter.delete("/addusers/{user_id}", response_model=dict)
# async def delete_add_user(
#     user_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         query_delete_student = "DELETE FROM student WHERE user_id = %s"
#         db[0].execute(query_delete_student, (user_id,))

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

AddStudentUserRouter = APIRouter(tags=["Add Student User"])

@AddStudentUserRouter.get("/addusers/email-exists/")
async def check_email_exists(email: str, db=Depends(get_db)):
    query = "SELECT COUNT(*) FROM user WHERE email = %s"
    db[1].execute(query, (email,))
    result = db[1].fetchone()[0]
    return {"email_exists": result > 0}

@AddStudentUserRouter.get("/addusers/student-school-id-exists/")
async def check_student_school_id_exists(student_school_id: str, db=Depends(get_db)):
    query = "SELECT COUNT(*) FROM student WHERE student_school_id = %s"
    db[1].execute(query, (student_school_id,))
    result = db[1].fetchone()[0]
    return {"student_school_id_exists": result > 0}

@AddStudentUserRouter.get("/addusers/", response_model=list)
async def read_add_users(
    db=Depends(get_db)
):
    query = """
        SELECT
            COALESCE(s.student_school_id, '') AS student_school_id,
            u.first_name,
            COALESCE(u.middle_name, '') AS middle_name,
            u.last_name,
            COALESCE(u.suffix, '') AS suffix,
            COALESCE(s.address, '') AS address,
            COALESCE(s.contact, '') AS contact,
            COALESCE(s.last_school_year, '') AS last_school_year,
            COALESCE(s.degree, '') AS degree,
            u.email,
            u.registration_date
        FROM
            user u
        LEFT JOIN
            student s ON u.user_id = s.user_id;
    """
    db[1].execute(query)
    users = [{
        "student_school_id": row[0], "first_name": row[1], "middle_name": row[2], "last_name": row[3], "suffix": row[4],
        "address": row[5], "contact": row[6], "last_school_year": row[7], "degree": row[8], "email": row[9], "registration_date": row[10]
    } for row in db[1].fetchall()]
    return users

@AddStudentUserRouter.get("/addusers/{user_id}", response_model=dict)
async def read_specific_user(
    user_id: int,
    db=Depends(get_db)
):
    query = """
        SELECT
            COALESCE(s.student_school_id, '') AS student_school_id,
            u.first_name,
            COALESCE(u.middle_name, '') AS middle_name,
            u.last_name,
            COALESCE(u.suffix, '') AS suffix,
            COALESCE(s.address, '') AS address,
            COALESCE(s.contact, '') AS contact,
            COALESCE(s.last_school_year, '') AS last_school_year,
            COALESCE(s.degree, '') AS degree,
            u.email,
            u.registration_date
        FROM
            user u
        LEFT JOIN
            student s ON u.user_id = s.user_id
        WHERE
            u.user_id = %s;
    """
    db[1].execute(query, (user_id,))
    user = db[1].fetchone()
    if user:
        return {
            "student_school_id": user[0], "first_name": user[1], "middle_name": user[2], "last_name": user[3], "suffix": user[4],
            "address": user[5], "contact": user[6], "last_school_year": user[7], "degree": user[8], "email": user[9], "registration_date": user[10]
        }
    raise HTTPException(status_code=404, detail="User not found")

@AddStudentUserRouter.post("/addusers/", response_model=dict)
async def create_add_user(
    student_school_id: str = Form(None),
    first_name: str = Form(...), 
    middle_name: str = Form(None), 
    last_name: str = Form(...), 
    suffix: str = Form(None), 
    address: str = Form(None), 
    contact: str = Form(None), 
    last_school_year: str = Form(None), 
    degree: str = Form(None), 
    email: str = Form(...), 
    password: str = Form(...), 
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

    query_student = """
        INSERT INTO student (user_id, student_school_id, address, contact, last_school_year, degree) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    db[1].execute(query_student, (new_user_id, student_school_id, address, contact, last_school_year, degree))

    db[0].commit()

    return {"user_id": new_user_id, "student_school_id": student_school_id, "first_name": first_name, "middle_name": middle_name, "last_name": last_name, 
            "suffix": suffix, "address": address, "contact": contact, "last_school_year": last_school_year, 
            "degree": degree, "email": email}

@AddStudentUserRouter.put("/addusers/{user_id}", response_model=dict)
async def update_add_user(
    user_id: int,
    first_name: str = Form(...),
    middle_name: str = Form(None),
    last_name: str = Form(...),
    suffix: str = Form(None),
    address: str = Form(None),
    contact: str = Form(None),
    last_school_year: str = Form(None),
    degree: str = Form(None),
    email: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    query_user = """
        UPDATE user 
        SET first_name = %s, middle_name = %s, last_name = %s, suffix = %s, email = %s, password = %s 
        WHERE user_id = %s
    """
    db[1].execute(query_user, (first_name, middle_name, last_name, suffix, email, password, user_id))

    query_student = """
        UPDATE student 
        SET address = %s, contact = %s, last_school_year = %s, degree = %s 
        WHERE user_id = %s
    """
    db[1].execute(query_student, (address, contact, last_school_year, degree, user_id))

    db[0].commit()

    return {"message": "User updated successfully"}

@AddStudentUserRouter.delete("/addusers/{user_id}", response_model=dict)
async def delete_add_user(
    user_id: int,
    db=Depends(get_db)
):
    try:
        query_delete_student = "DELETE FROM student WHERE user_id = %s"
        db[1].execute(query_delete_student, (user_id,))

        query_delete_user = "DELETE FROM user WHERE user_id = %s"
        db[1].execute(query_delete_user, (user_id,))

        db[0].commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
