from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from .db import get_db

class DocumentType(BaseModel):
    name: str
    fee: float
    unit_name: str

DocumentTypeRouter = APIRouter(tags=["Document Types"])

@DocumentTypeRouter.get("/document_types/", response_model=List[DocumentType])
async def read_document_types(
    db=Depends(get_db)
):
    query = "SELECT document_type_id, name, fee, unit_name FROM document_type"
    db[0].execute(query)
    document_types = [dict(zip(('document_type_id', 'name', 'fee', 'unit_name'), row)) for row in db[0].fetchall()]
    return document_types

@DocumentTypeRouter.get("/document_types/{document_type_id}", response_model=DocumentType)
async def read_document_type(
    document_type_id: int,
    db=Depends(get_db)
):
    query = "SELECT name, fee, unit_name FROM document_type WHERE document_type_id = %s"
    db[0].execute(query, (document_type_id,))
    document_type = db[0].fetchone()
    if document_type:
        return dict(zip(('name', 'fee', 'unit_name'), document_type))
    raise HTTPException(status_code=404, detail="Document type not found")

@DocumentTypeRouter.post("/document_types/", response_model=DocumentType)
async def create_document_type(
    document_type: DocumentType,
    db=Depends(get_db)
):
    query = "INSERT INTO document_type (name, fee, unit_name) VALUES (%s, %s, %s)"
    db[0].execute(query, (document_type.name, document_type.fee, document_type.unit_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_document_type_id = db[0].fetchone()[0]
    db[1].commit()

    return {**document_type.dict(), "document_type_id": new_document_type_id}

@DocumentTypeRouter.put("/document_types/{document_type_id}", response_model=DocumentType)
async def update_document_type(
    document_type_id: int,
    document_type: DocumentType,
    db=Depends(get_db)
):
    query = "UPDATE document_type SET name = %s, fee = %s, unit_name = %s WHERE document_type_id = %s"
    db[0].execute(query, (document_type.name, document_type.fee, document_type.unit_name, document_type_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {**document_type.dict(), "document_type_id": document_type_id}
    
    # If no rows were affected, document type not found
    raise HTTPException(status_code=404, detail="Document type not found")

@DocumentTypeRouter.delete("/document_types/{document_type_id}")
async def delete_document_type(
    document_type_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the document type exists
        query_check_document_type = "SELECT document_type_id FROM document_type WHERE document_type_id = %s"
        db[0].execute(query_check_document_type, (document_type_id,))
        existing_document_type = db[0].fetchone()

        if not existing_document_type:
            raise HTTPException(status_code=404, detail="Document type not found")

        # Delete the document type
        query_delete_document_type = "DELETE FROM document_type WHERE document_type_id = %s"
        db[0].execute(query_delete_document_type, (document_type_id,))
        db[1].commit()

        return {"message": "Document type deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
