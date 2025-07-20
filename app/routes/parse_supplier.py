from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import extract_products_from_excel, save_parsed_products
from app.services.utils import update_sustainability_flags
import uuid
router = APIRouter()

@router.post("/parse-supplier")
async def parse_supplier_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Please upload an Excel file")
    
    contents = await file.read()
    products = extract_products_from_excel(contents)
    supplier_id = str(uuid.uuid4())
    save_parsed_products(products, supplier_id)

    update_sustainability_flags()

    return { 
        "message": "Products parse and saved successfully",
        "supplier_id": supplier_id,
        "products": products 
        }
