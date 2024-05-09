# from fastapi import Depends, HTTPException, APIRouter
# from db import get_db
# from datetime import date

# ClaimingInformationRouter = APIRouter(tags=["Claiming Information"])

# @ClaimingInformationRouter.get("/claiming_information/", response_model=list)
# async def read_claiming_information(
#     db=Depends(get_db)
# ):
#     query = "SELECT claiming_id, request_id, mode_of_claiming, claiming_date FROM claiming_information"
#     db[0].execute(query)
#     claiming_information = [{
#         "claiming_id": info[0], "request_id": info[1], 
#         "mode_of_claiming": info[2], "claiming_date": info[3]
#     } for info in db[0].fetchall()]
#     return claiming_information

# @ClaimingInformationRouter.get("/claiming_information/{claiming_id}", response_model=dict)
# async def read_claiming_information_by_id(
#     claiming_id: int, 
#     db=Depends(get_db)
# ):
#     query = "SELECT claiming_id, request_id, mode_of_claiming, claiming_date FROM claiming_information WHERE claiming_id = %s"
#     db[0].execute(query, (claiming_id,))
#     claiming_info = db[0].fetchone()
#     if claiming_info:
#         return {
#             "claiming_id": claiming_info[0], "request_id": claiming_info[1], 
#             "mode_of_claiming": claiming_info[2], "claiming_date": claiming_info[3]
#         }
#     raise HTTPException(status_code=404, detail="Claiming information not found")

# @ClaimingInformationRouter.post("/claiming_information/", response_model=dict)
# async def create_claiming_information(
#     request_id: int, 
#     mode_of_claiming: str,
#     claiming_date: date = None,
#     db=Depends(get_db)
# ):
#     query = "INSERT INTO claiming_information (request_id, mode_of_claiming, claiming_date) VALUES (%s, %s, %s)"
#     db[0].execute(query, (request_id, mode_of_claiming, claiming_date))

#     # Retrieve the last inserted ID using LAST_INSERT_ID()
#     db[0].execute("SELECT LAST_INSERT_ID()")
#     new_claiming_id = db[0].fetchone()[0]
#     db[1].commit()

#     return {
#         "claiming_id": new_claiming_id, "request_id": request_id, 
#         "mode_of_claiming": mode_of_claiming, "claiming_date": claiming_date
#     }

# @ClaimingInformationRouter.put("/claiming_information/{claiming_id}", response_model=dict)
# async def update_claiming_information(
#     claiming_id: int,
#     request_id: int, 
#     mode_of_claiming: str,
#     claiming_date: date = None,
#     db=Depends(get_db)
# ):
#     query = "UPDATE claiming_information SET request_id = %s, mode_of_claiming = %s, claiming_date = %s WHERE claiming_id = %s"
#     db[0].execute(query, (request_id, mode_of_claiming, claiming_date, claiming_id))

#     # Check if the update was successful
#     if db[0].rowcount > 0:
#         db[1].commit()
#         return {"message": "Claiming information updated successfully"}
    
#     # If no rows were affected, claiming information not found
#     raise HTTPException(status_code=404, detail="Claiming information not found")

# @ClaimingInformationRouter.delete("/claiming_information/{claiming_id}", response_model=dict)
# async def delete_claiming_information(
#     claiming_id: int,
#     db=Depends(get_db)
# ):
#     try:
#         # Check if the claiming information exists
#         query_check_info = "SELECT claiming_id FROM claiming_information WHERE claiming_id = %s"
#         db[0].execute(query_check_info, (claiming_id,))
#         existing_info = db[0].fetchone()

#         if not existing_info:
#             raise HTTPException(status_code=404, detail="Claiming information not found")

#         # Delete the claiming information
#         query_delete_info = "DELETE FROM claiming_information WHERE claiming_id = %s"
#         db[0].execute(query_delete_info, (claiming_id,))
#         db[1].commit()

#         return {"message": "Claiming information deleted successfully"}
#     except Exception as e:
#         # Handle other exceptions if necessary
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         # Close the database cursor
#         db[0].close()

from fastapi import Depends, HTTPException, APIRouter
from db import get_db
from datetime import date

ClaimingInformationRouter = APIRouter(tags=["Claiming Information"])

@ClaimingInformationRouter.get("/claiming_information/", response_model=list)
async def read_claiming_information(
    db=Depends(get_db)
):
    try:
        query = "SELECT claiming_id, request_id, mode_of_claiming, claiming_date FROM claiming_information"
        db[1].execute(query)
        claiming_information = [{
            "claiming_id": info[0], "request_id": info[1], 
            "mode_of_claiming": info[2], "claiming_date": info[3]
        } for info in db[1].fetchall()]
        return claiming_information
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@ClaimingInformationRouter.get("/claiming_information/{claiming_id}", response_model=dict)
async def read_claiming_information_by_id(
    claiming_id: int, 
    db=Depends(get_db)
):
    try:
        query = "SELECT claiming_id, request_id, mode_of_claiming, claiming_date FROM claiming_information WHERE claiming_id = %s"
        db[1].execute(query, (claiming_id,))
        claiming_info = db[1].fetchone()
        if claiming_info:
            return {
                "claiming_id": claiming_info[0], "request_id": claiming_info[1], 
                "mode_of_claiming": claiming_info[2], "claiming_date": claiming_info[3]
            }
        raise HTTPException(status_code=404, detail="Claiming information not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@ClaimingInformationRouter.post("/claiming_information/", response_model=dict)
async def create_claiming_information(
    request_id: int, 
    mode_of_claiming: str,
    claiming_date: date = None,
    db=Depends(get_db)
):
    try:
        query = "INSERT INTO claiming_information (request_id, mode_of_claiming, claiming_date) VALUES (%s, %s, %s)"
        db[1].execute(query, (request_id, mode_of_claiming, claiming_date))

        # Retrieve the last inserted ID using LAST_INSERT_ID()
        db[1].execute("SELECT LAST_INSERT_ID()")
        new_claiming_id = db[1].fetchone()[0]
        db[0].commit()

        return {
            "claiming_id": new_claiming_id, "request_id": request_id, 
            "mode_of_claiming": mode_of_claiming, "claiming_date": claiming_date
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@ClaimingInformationRouter.put("/claiming_information/{claiming_id}", response_model=dict)
async def update_claiming_information(
    claiming_id: int,
    request_id: int, 
    mode_of_claiming: str,
    claiming_date: date = None,
    db=Depends(get_db)
):
    try:
        query = "UPDATE claiming_information SET request_id = %s, mode_of_claiming = %s, claiming_date = %s WHERE claiming_id = %s"
        db[1].execute(query, (request_id, mode_of_claiming, claiming_date, claiming_id))

        # Check if the update was successful
        if db[1].rowcount > 0:
            db[0].commit()
            return {"message": "Claiming information updated successfully"}
        
        # If no rows were affected, claiming information not found
        raise HTTPException(status_code=404, detail="Claiming information not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db[1].close()
        db[0].close()

@ClaimingInformationRouter.delete("/claiming_information/{claiming_id}", response_model=dict)
async def delete_claiming_information(
    claiming_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the claiming information exists
        query_check_info = "SELECT claiming_id FROM claiming_information WHERE claiming_id = %s"
        db[1].execute(query_check_info, (claiming_id,))
        existing_info = db[1].fetchone()

        if not existing_info:
            raise HTTPException(status_code=404, detail="Claiming information not found")

        # Delete the claiming information
        query_delete_info = "DELETE FROM claiming_information WHERE claiming_id = %s"
        db[1].execute(query_delete_info, (claiming_id,))
        db[0].commit()

        return {"message": "Claiming information deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Close the database cursor
        db[1].close()
        db[0].close()
