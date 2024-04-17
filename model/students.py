from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


StudentRouter = APIRouter(tags=["Students"])

# CRUD operations

@StudentRouter.get("/students/", response_model=list)
async def read_students(
    db=Depends(get_db)
):
    query = """
    SELECT s.user_id, u.first_name, u.middle_name, u.last_name, s.student_school_id, s.contact, s.address, s.degree, s.last_school_year
    FROM student s
    INNER JOIN user u ON s.user_id = u.user_id
    """
    db[0].execute(query)
    students = [{
        "user_id": student[0],
        "full_name": " ".join(filter(None, [student[1], student[2], student[3]])),
        "student_school_id": student[4],
        "contact": student[5],
        "address": student[6],
        "degree": student[7],
        "last_school_year": student[8]
    } for student in db[0].fetchall()]
    return students

@StudentRouter.get("/students/{user_id}", response_model=dict)
async def read_student(
    user_id: int, 
    db=Depends(get_db)
):
    query = """
    SELECT s.user_id, u.first_name, u.middle_name, u.last_name, s.student_school_id, s.contact, s.address, s.degree, s.last_school_year
    FROM student s
    INNER JOIN user u ON s.user_id = u.user_id
    WHERE s.user_id = %s
    """
    db[0].execute(query, (user_id,))
    student = db[0].fetchone()
    if student:
        return {
            "user_id": student[0],
            "full_name": " ".join(filter(None, [student[1], student[2], student[3]])),
            "student_school_id": student[4],
            "contact": student[5],
            "address": student[6],
            "degree": student[7],
            "last_school_year": student[8]
        }
    raise HTTPException(status_code=404, detail="Student not found")

@StudentRouter.post("/students/", response_model=dict)
async def create_student(
    user_id: int = Form(...), 
    student_school_id: str = Form(...), 
    contact: str = Form(...), 
    address: str = Form(...), 
    degree: str = Form(...), 
    last_school_year: str = Form(...), 
    db=Depends(get_db)
):
    query = "INSERT INTO student (user_id, student_school_id, contact, address, degree, last_school_year) VALUES (%s, %s, %s, %s, %s, %s)"
    db[0].execute(query, (user_id, student_school_id, contact, address, degree, last_school_year))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {
        "user_id": user_id,
        "student_school_id": student_school_id,
        "contact": contact,
        "address": address,
        "degree": degree,
        "last_school_year": last_school_year
    }

@StudentRouter.put("/students/{user_id}", response_model=dict)
async def update_student(
    user_id: int,
    student_school_id: str = Form(...),
    contact: str = Form(...),
    address: str = Form(...),
    degree: str = Form(...),
    last_school_year: str = Form(...),
    db=Depends(get_db)
):
    query = """
    UPDATE student
    SET student_school_id = %s, contact = %s, address = %s, degree = %s, last_school_year = %s
    WHERE user_id = %s
    """
    db[0].execute(query, (student_school_id, contact, address, degree, last_school_year, user_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Student updated successfully"}
    
    # If no rows were affected, student not found
    raise HTTPException(status_code=404, detail="Student not found")

@StudentRouter.delete("/students/{user_id}", response_model=dict)
async def delete_student(
    user_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the student exists
        query_check_student = "SELECT user_id FROM student WHERE user_id = %s"
        db[0].execute(query_check_student, (user_id,))
        existing_student = db[0].fetchone()

        if not existing_student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Delete the student
        query_delete_student = "DELETE FROM student WHERE user_id = %s"
        db[0].execute(query_delete_student, (user_id,))
        db[1].commit()

        return {"message": "Student deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
