from fastapi import Depends, HTTPException, APIRouter
from .db import get_db
from datetime import date

UserFeedbackRouter = APIRouter(tags=["User Feedback"])

@UserFeedbackRouter.get("/user_feedback/", response_model=list)
async def read_user_feedback(
    db=Depends(get_db)
):
    query = """
        SELECT feedback_id, user_id, request_id, feedback_text, feedback_rating, feedback_date
        FROM user_feedback
    """
    db[0].execute(query)
    user_feedback = [{
        "feedback_id": feedback[0], "user_id": feedback[1], 
        "request_id": feedback[2], "feedback_text": feedback[3], 
        "feedback_rating": feedback[4], "feedback_date": feedback[5]
    } for feedback in db[0].fetchall()]
    return user_feedback

@UserFeedbackRouter.get("/user_feedback/{feedback_id}", response_model=dict)
async def read_user_feedback_by_id(
    feedback_id: int, 
    db=Depends(get_db)
):
    query = """
        SELECT feedback_id, user_id, request_id, feedback_text, feedback_rating, feedback_date
        FROM user_feedback
        WHERE feedback_id = %s
    """
    db[0].execute(query, (feedback_id,))
    feedback_info = db[0].fetchone()
    if feedback_info:
        return {
            "feedback_id": feedback_info[0], "user_id": feedback_info[1], 
            "request_id": feedback_info[2], "feedback_text": feedback_info[3], 
            "feedback_rating": feedback_info[4], "feedback_date": feedback_info[5]
        }
    raise HTTPException(status_code=404, detail="User feedback not found")

@UserFeedbackRouter.post("/user_feedback/", response_model=dict)
async def create_user_feedback(
    user_id: int, 
    feedback_text: str,
    feedback_rating: int,
    request_id: int = None,
    feedback_date: date = date.today(),
    db=Depends(get_db)
):
    query = """
        INSERT INTO user_feedback 
        (user_id, request_id, feedback_text, feedback_rating, feedback_date) 
        VALUES (%s, %s, %s, %s, %s)
    """
    db[0].execute(query, (user_id, request_id, feedback_text, feedback_rating, feedback_date))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_feedback_id = db[0].fetchone()[0]
    db[1].commit()

    return {
        "feedback_id": new_feedback_id, "user_id": user_id, 
        "request_id": request_id, "feedback_text": feedback_text, 
        "feedback_rating": feedback_rating, "feedback_date": feedback_date
    }

@UserFeedbackRouter.put("/user_feedback/{feedback_id}", response_model=dict)
async def update_user_feedback(
    feedback_id: int,
    user_id: int, 
    feedback_text: str,
    feedback_rating: int,
    request_id: int = None,
    feedback_date: date = date.today(),
    db=Depends(get_db)
):
    query = """
        UPDATE user_feedback 
        SET user_id = %s, request_id = %s, feedback_text = %s, 
        feedback_rating = %s, feedback_date = %s 
        WHERE feedback_id = %s
    """
    db[0].execute(query, (user_id, request_id, feedback_text, feedback_rating, feedback_date, feedback_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User feedback updated successfully"}
    
    # If no rows were affected, user feedback not found
    raise HTTPException(status_code=404, detail="User feedback not found")

@UserFeedbackRouter.delete("/user_feedback/{feedback_id}", response_model=dict)
async def delete_user_feedback(
    feedback_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user feedback exists
        query_check_feedback = "SELECT feedback_id FROM user_feedback WHERE feedback_id = %s"
        db[0].execute(query_check_feedback, (feedback_id,))
        existing_feedback = db[0].fetchone()

        if not existing_feedback:
            raise HTTPException(status_code=404, detail="User feedback not found")

        # Delete the user feedback
        query_delete_feedback = "DELETE FROM user_feedback WHERE feedback_id = %s"
        db[0].execute(query_delete_feedback, (feedback_id,))
        db[1].commit()

        return {"message": "User feedback deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
