from fastapi import Depends, HTTPException, APIRouter
from .db import get_db

DocumentRequestItemRouter = APIRouter(tags=["Document Request Item"])

@DocumentRequestItemRouter.get("/document_request_items/", response_model=list)
async def read_document_request_items(
    db=Depends(get_db)
):
    query = "SELECT item_id, request_id, document_type_id, quantity FROM document_request_item"
    db[0].execute(query)
    document_request_items = [{
        "item_id": item[0], "request_id": item[1], 
        "document_type_id": item[2], "quantity": item[3]
    } for item in db[0].fetchall()]
    return document_request_items

@DocumentRequestItemRouter.get("/document_request_items/{item_id}", response_model=dict)
async def read_document_request_item(
    item_id: int, 
    db=Depends(get_db)
):
    query = "SELECT item_id, request_id, document_type_id, quantity FROM document_request_item WHERE item_id = %s"
    db[0].execute(query, (item_id,))
    document_request_item = db[0].fetchone()
    if document_request_item:
        return {
            "item_id": document_request_item[0], "request_id": document_request_item[1], 
            "document_type_id": document_request_item[2], "quantity": document_request_item[3]
        }
    raise HTTPException(status_code=404, detail="Document request item not found")

@DocumentRequestItemRouter.post("/document_request_items/", response_model=dict)
async def create_document_request_item(
    request_id: int, 
    document_type_id: int,
    quantity: int,
    db=Depends(get_db)
):
    query = "INSERT INTO document_request_item (request_id, document_type_id, quantity) VALUES (%s, %s, %s)"
    db[0].execute(query, (request_id, document_type_id, quantity))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_item_id = db[0].fetchone()[0]
    db[1].commit()

    return {
        "item_id": new_item_id, "request_id": request_id, 
        "document_type_id": document_type_id, "quantity": quantity
    }

@DocumentRequestItemRouter.put("/document_request_items/{item_id}", response_model=dict)
async def update_document_request_item(
    item_id: int,
    request_id: int, 
    document_type_id: int,
    quantity: int,
    db=Depends(get_db)
):
    query = "UPDATE document_request_item SET request_id = %s, document_type_id = %s, quantity = %s WHERE item_id = %s"
    db[0].execute(query, (request_id, document_type_id, quantity, item_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Document request item updated successfully"}
    
    # If no rows were affected, document request item not found
    raise HTTPException(status_code=404, detail="Document request item not found")

@DocumentRequestItemRouter.delete("/document_request_items/{item_id}", response_model=dict)
async def delete_document_request_item(
    item_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the document request item exists
        query_check_item = "SELECT item_id FROM document_request_item WHERE item_id = %s"
        db[0].execute(query_check_item, (item_id,))
        existing_item = db[0].fetchone()

        if not existing_item:
            raise HTTPException(status_code=404, detail="Document request item not found")

        # Delete the document request item
        query_delete_item = "DELETE FROM document_request_item WHERE item_id = %s"
        db[0].execute(query_delete_item, (item_id,))
        db[1].commit()

        return {"message": "Document request item deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
