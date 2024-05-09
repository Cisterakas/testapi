# from fastapi import Depends, HTTPException, APIRouter, Form
# from db import get_db


# AdministratorRouter = APIRouter(tags=["Administrators"])

# # CRUD operations

# @AdministratorRouter.get("/administrators/", response_model=list)
# async def read_administrators(
#     db=Depends(get_db)
# ):
#     query = """
#     SELECT a.user_id, u.first_name, u.middle_name, u.last_name, a.role
#     FROM administrator a
#     INNER JOIN user u ON a.user_id = u.user_id
#     """
#     db[0].execute(query)
#     administrators = [{
#         "user_id": admin[0],
#         "full_name": " ".join(filter(None, [admin[1], admin[2], admin[3]])),
#         "role": admin[4]
#     } for admin in db[0].fetchall()]
#     return administrators

# @AdministratorRouter.get("/administrators/{user_id}", response_model=dict)
# async def read_administrator(
#     user_id: int, 
#     db=Depends(get_db)
# ):
#     query = """
#     SELECT a.user_id, u.first_name, u.middle_name, u.last_name, a.role
#     FROM administrator a
#     INNER JOIN user u ON a.user_id = u.user_id
#     WHERE a.user_id = %s
#     """
#     db[0].execute(query, (user_id,))
#     administrator = db[0].fetchone()
#     if administrator:
#         return {
#             "user_id": administrator[0],
#             "full_name": " ".join(filter(None, [administrator[1], administrator[2], administrator[3]])),
#             "role": administrator[4]
#         }
#     raise HTTPException(status_code=404, detail="Administrator not found")

# @AdministratorRouter.post("/administrators/", response_model=dict)
# async def create_administrator(
#     user_id: int = Form(...), 
#     role: str = Form(None), 
#     db=Depends(get_db)
# ):
#     query = "INSERT INTO administrator (user_id, role) VALUES (%s, %s)"
#     db[0].execute(query, (user_id, role))

#     db[1].commit()

#     return {
#         "user_id": user_id,
#         "role": role
#     }

# @AdministratorRouter.put("/administrators/{user_id}", response_model=dict)
# async def update_administrator(
#     user_id: int,
#     role: str = Form(None),
#     db=Depends(get_db)
# ):
#     query = """
#     UPDATE administrator
#     SET role = %s
#     WHERE user_id = %s
#     """
#     db[0].execute(query, (role, user_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "Administrator updated successfully"}
    
#     # If no rows were affected, administrator not found
#     raise HTTPException(status_code=404, detail="Administrator not found")

# @AdministratorRouter.delete("/administrators/{user_id}", response_model=dict)
# async def delete_administrator(
#     user_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the administrator exists
#         query_check_administrator = "SELECT user_id FROM administrator WHERE user_id = %s"
#         db[0].execute(query_check_administrator, (user_id,))
#         existing_administrator = db[0].fetchone()

#         if not existing_administrator:
#             raise HTTPException(status_code=404, detail="Administrator not found")

#         # Delete the administrator
#         query_delete_administrator = "DELETE FROM administrator WHERE user_id = %s"
#         db[0].execute(query_delete_administrator, (user_id,))
#         db[1].commit()

#         return {"message": "Administrator deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()
from fastapi import Depends, HTTPException, APIRouter, Form
from db import get_db

AdministratorRouter = APIRouter(tags=["Administrators"])

# CRUD operations

@AdministratorRouter.get("/administrators/", response_model=list)
async def read_administrators(
    db=Depends(get_db)
):
    query = """
    SELECT a.user_id, u.first_name, u.middle_name, u.last_name, a.role
    FROM administrator a
    INNER JOIN user u ON a.user_id = u.user_id
    """
    db[1].execute(query)
    administrators = [{
        "user_id": admin[0],
        "full_name": " ".join(filter(None, [admin[1], admin[2], admin[3]])),
        "role": admin[4]
    } for admin in db[1].fetchall()]
    return administrators

@AdministratorRouter.get("/administrators/{user_id}", response_model=dict)
async def read_administrator(
    user_id: int, 
    db=Depends(get_db)
):
    query = """
    SELECT a.user_id, u.first_name, u.middle_name, u.last_name, a.role
    FROM administrator a
    INNER JOIN user u ON a.user_id = u.user_id
    WHERE a.user_id = %s
    """
    db[1].execute(query, (user_id,))
    administrator = db[1].fetchone()
    if administrator:
        return {
            "user_id": administrator[0],
            "full_name": " ".join(filter(None, [administrator[1], administrator[2], administrator[3]])),
            "role": administrator[4]
        }
    raise HTTPException(status_code=404, detail="Administrator not found")

@AdministratorRouter.post("/administrators/", response_model=dict)
async def create_administrator(
    user_id: int = Form(...), 
    role: str = Form(None), 
    db=Depends(get_db)
):
    query = "INSERT INTO administrator (user_id, role) VALUES (%s, %s)"
    db[1].execute(query, (user_id, role))

    db[0].commit()

    return {
        "user_id": user_id,
        "role": role
    }

@AdministratorRouter.put("/administrators/{user_id}", response_model=dict)
async def update_administrator(
    user_id: int,
    role: str = Form(None),
    db=Depends(get_db)
):
    query = """
    UPDATE administrator
    SET role = %s
    WHERE user_id = %s
    """
    db[1].execute(query, (role, user_id))

    # Check if the update was successful
    if db[1].rowcount > 0:
        db[0].commit()
        return {"message": "Administrator updated successfully"}
    
    # If no rows were affected, administrator not found
    raise HTTPException(status_code=404, detail="Administrator not found")

@AdministratorRouter.delete("/administrators/{user_id}", response_model=dict)
async def delete_administrator(
    user_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the administrator exists
        query_check_administrator = "SELECT user_id FROM administrator WHERE user_id = %s"
        db[1].execute(query_check_administrator, (user_id,))
        existing_administrator = db[1].fetchone()

        if not existing_administrator:
            raise HTTPException(status_code=404, detail="Administrator not found")

        # Delete the administrator
        query_delete_administrator = "DELETE FROM administrator WHERE user_id = %s"
        db[1].execute(query_delete_administrator, (user_id,))
        db[0].commit()

        return {"message": "Administrator deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[1].close()
