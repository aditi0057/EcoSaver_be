from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.parser import load_parsed_products, get_latest_supplier_id, save_parsed_products
from app.services.scoring import calclulate_ecoscore
from app.models.product import ProductCreate
from app.services.utils import update_sustainability_flags

import os
router = APIRouter()

@router.get("/products/latest")
def get_products_by_supplier():
    try:
        latest_path = "data/parsed/latest_supplier_id.txt"

        if not os.path.exists(latest_path):
            raise HTTPException(status_code=404, detail="No supplier file has been uploaded yet")
        
        with open(latest_path) as f:
            latest_supplier_id = f.read().strip()
        products = load_parsed_products(latest_supplier_id)
        return {
            "supplier_id": latest_supplier_id,
            "products": products
            }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products not found for this supplier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/product/{product_id}")
def get_product_by_id(product_id:int):
    try:
        latest_path = "data/parsed/latest_supplier_id.txt"
        if not os.path.exists(latest_path):
            raise HTTPException(status_code=404, detail="No uploaded supplier data found")
        with open(latest_path) as f:
            latest_supplier_id = f.read().strip()

        products = load_parsed_products(latest_supplier_id)
        for product in products:
            if str(product.get("product_id")) == str(product_id):
                return product
            
        raise HTTPException(status_code=404, detail=f"Product with ID { product_id} not found")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Supplier data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/product")
def add_mock_product(payload: ProductCreate):
    try:
        supplier_id= get_latest_supplier_id()
        products = load_parsed_products(supplier_id)
        max_id = max((p.get("product_id", 1000) for p in products), default = 1000)

        new_product = payload.dict()
        new_product["product_id"] = max_id +1

        products.append(new_product)
        save_parsed_products(products,supplier_id)

        return{
            "message": "Product added successfully",
            "product": new_product
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No supplier file has been uploaded yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products")
def get_products(sustainable: Optional[bool] = Query(None, description="Filter by sustainability")):
    try:
        update_sustainability_flags()
        supplier_id = get_latest_supplier_id()
        products = load_parsed_products(supplier_id)

        if sustainable is None:
            return{
                "supplier_id": supplier_id,
                "count": len(products),
                "products": products
            }
        
        filtered = []
        for product in products:
            score = calclulate_ecoscore(product)
            is_sustainable=score.get("eco_score", 0) >= 50
            if is_sustainable == sustainable:
                filtered.append(product)

        return{
            "supplier_id": supplier_id,
            "count": len(filtered),
            "products": filtered
        }
    
    except FileExistsError:
        raise HTTPException(status_code=404, detail="Supplier or products not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/update-sustainability")
def update_all_products_sustainability():
    try:
        updated_products = update_sustainability_flags()
        return {
            "updated_count": len(updated_products),
            "message": "Sustainability flags updated successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/recyclable")
def get_recyclable_products():
    try:
        latest_path = "data/parsed/latest_supplier_id.txt"

        if not os.path.exists(latest_path):
            raise HTTPException(status_code=404, detail="No uploaded supplier data found")

        with open(latest_path) as f:
            supplier_id = f.read().strip()

        products = load_parsed_products(supplier_id)
        print(f"✅ Loaded {len(products)} products")

        recyclable_keywords = ["recycle", "recyclable", "recycled", "recycle/compost"]
        filtered = []

        for product in products:
            end_life = str(product.get("end_of_life_disposal", "")).lower()
            certification = str(product.get("certification_tags", "")).lower()

            if any(kw in end_life for kw in recyclable_keywords) or "recyclable" in certification:
                filtered.append(product)

        return {
            "filter": "Recyclable Products",
            "supplier_id": supplier_id,
            "count": len(filtered),
            "products": filtered
        }

    except Exception as e:
        print(f"🔥 Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/water-friendly")
def get_water_friendly_products():
    try:
        update_sustainability_flags()
        supplier_id = get_latest_supplier_id()
        products = load_parsed_products(supplier_id)

        # Define water-friendly packaging materials
        water_friendly_materials = [
            "kraft paper", "paper wrap", "cardboard box", "recycled paper box"
        ]

        filtered = []
        for product in products:
            material = str(product.get("packing_material_type", "")).lower()
            if material in water_friendly_materials:
                filtered.append(product)

        return {
            "filter": "Water-Friendly Packaging",
            "supplier_id": supplier_id,
            "count": len(filtered),
            "products": filtered
        }

    except FileExistsError:
        raise HTTPException(status_code=404, detail="Supplier or products not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/certified")
def get_certified_products():
    try:
        update_sustainability_flags()
        supplier_id = get_latest_supplier_id()
        products = load_parsed_products(supplier_id)

        filtered = [
            product for product in products
            if product.get("certification_tags")
            and product.get("certification_tags").strip() not in ["", "-", "–"]
        ]

        return {
            "filter": "Certified Products Only",
            "supplier_id": supplier_id,
            "count": len(filtered),
            "products": filtered
        }

    except FileExistsError:
        raise HTTPException(status_code=404, detail="Supplier or products not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/products/{supplier_id}")
def get_products_by_supplier(supplier_id: str):
    try:
        products = load_parsed_products(supplier_id)
        return {"products": products}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="45Products not found for this supplier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    