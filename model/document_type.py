from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from db import get_db

class DocumentType(BaseModel):
    document_type_id: int
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

