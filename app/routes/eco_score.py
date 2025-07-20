from fastapi import APIRouter, HTTPException
from app.services.parser import load_parsed_products, get_latest_supplier_id
from app.services.scoring import calclulate_ecoscore

router = APIRouter()

@router.get("/eco_score/{product_id}")
def get_eco_score(product_id: int):
    try:
        supplier_id = get_latest_supplier_id()
        products = load_parsed_products(supplier_id)
        product = next((p for p in products if p.get("product_id")==product_id), None)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        score_result = calclulate_ecoscore(product)
        return{
            "product_id": product_id,
            "product_name": product.get("product_name"),
            **score_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/eco-breakdown/{product_id}")
def get_eco_score_breakdown(product_id: int):
    try:
        supplier_id = get_latest_supplier_id()
        products = load_parsed_products(supplier_id)
        product = next((p for p in products if p.get("product_id") == product_id), None)

        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        score_result = calclulate_ecoscore(product)

        return {
            "product_id": product_id,
            "product_name": product.get("product_name"),
            "eco_score": score_result["eco_score"],
            "breakdown": score_result["breakdown"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))