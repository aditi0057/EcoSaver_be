import os
from fastapi import APIRouter, HTTPException
from app.services.scoring import calclulate_ecoscore
from app.services.parser import load_parsed_products, save_parsed_products, get_latest_supplier_id
from typing import List, Dict

def update_sustainability_flags():
    supplier_id = get_latest_supplier_id()
    products = load_parsed_products(supplier_id)

    for product in products:
        score_data = calclulate_ecoscore(product)
        product["is_sustainable"] = score_data.get("eco_score",0) >= 60

    save_parsed_products(products, supplier_id)
    return products

def get_eco_score(product_id: int) -> dict:
    try:
        supplier_id = get_latest_supplier_id()
        products = load_parsed_products(supplier_id)
        
        # Find product by ID
        product = next((p for p in products if p.get("product_id") == product_id), None)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Calculate eco score
        score_result = calclulate_ecoscore(product)

        # Return a flat dict with required fields
        return {
            "product_id": product_id,
            "product_name": product.get("product_name"),
            "eco_score": score_result.get("eco_score", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_products_by_supplier() -> List[dict]:
    try:
        latest_path = "data/parsed/latest_supplier_id.txt"

        if not os.path.exists(latest_path):
            raise HTTPException(status_code=404, detail="No supplier file has been uploaded yet")
        
        with open(latest_path) as f:
            latest_supplier_id = f.read().strip()

        products = load_parsed_products(latest_supplier_id)

        return products  # ✅ Return only the product list

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products not found for this supplier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
