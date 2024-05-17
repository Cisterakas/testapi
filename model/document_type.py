from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from db import get_db

class DocumentType(BaseModel):
    document_type_id: int
    name: str
    fee: float
    unit_name: str
    
class DocumentTypeCreate(BaseModel):
    name: str
    fee: float
    unit_name: str

DocumentTypeRouter = APIRouter(tags=["Document Types"])

@DocumentTypeRouter.get("/document_types/", response_model=List[DocumentType])
async def read_document_types(db=Depends(get_db)):
    try:
        query = "SELECT document_type_id, name, fee, unit_name FROM document_type"
        cursor = db[1]
        cursor.execute(query)
        document_types = [dict(zip(('document_type_id', 'name', 'fee', 'unit_name'), row)) for row in cursor.fetchall()]
        return document_types
    finally:
        # Ensure to close the cursor and connection (replace with your database connection management)
        db[1].close()
        db[0].close()


@DocumentTypeRouter.post("/document_types/", response_model=DocumentType)
async def create_document_type(document_type: DocumentTypeCreate, db=Depends(get_db)):
    try:
        query = "INSERT INTO document_type (name, fee, unit_name) VALUES (%s, %s, %s)"
        cursor = db[1]
        cursor.execute(query, (document_type.name, document_type.fee, document_type.unit_name))
        
        # Retrieve the last inserted ID using LAST_INSERT_ID()
        cursor.execute("SELECT LAST_INSERT_ID()")
        document_type_id = cursor.fetchone()[0]
        
        db[0].commit()
        return DocumentType(document_type_id=document_type_id, **document_type.dict())
    finally:
        db[1].close()
        db[0].close()

@DocumentTypeRouter.put("/document_types/{document_type_id}", response_model=DocumentType)
async def update_document_type(document_type_id: int, document_type: DocumentType, db=Depends(get_db)):
    try:
        query = "UPDATE document_type SET name = %s, fee = %s, unit_name = %s WHERE document_type_id = %s"
        cursor = db[1]
        cursor.execute(query, (document_type.name, document_type.fee, document_type.unit_name, document_type_id))
        db[0].commit()
        document_type.document_type_id = document_type_id
        return document_type
    finally:
        db[1].close()
        db[0].close()

@DocumentTypeRouter.delete("/document_types/{document_type_id}")
async def delete_document_type(document_type_id: int, db=Depends(get_db)):  
    try:
        query = "DELETE FROM document_type WHERE document_type_id = %s"
        cursor = db[1]
        cursor.execute(query, (document_type_id,))
        db[0].commit()
        return {"message": "Document Type deleted successfully"}
    finally:
        db[1].close()
        db[0].close()
