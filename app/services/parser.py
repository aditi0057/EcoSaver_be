import pandas as pd
import io
import os
import json

def extract_products_from_excel(file_bytes):
    try:
        df = pd.read_excel(io.BytesIO(file_bytes))

        # Normalize column names: lowercase, underscores
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

        df.fillna("", inplace=True)

        products = df.to_dict(orient="records")

        has_product_id = "product_id" in df.columns

        for idx, product in enumerate(products):
            if not has_product_id or not product.get("product_id"):
                product["product_id"] = 1000 + idx
                
        return products

    except Exception as e:
        raise ValueError(f"Failed to parse Excel file: {e}")


def save_parsed_products(products: list, supplier_id: str):
    filepath = f"data/parsed/{supplier_id}_products.json"
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
    with open(filepath,"w") as f:
        json.dump(products,f,indent =2)

    latest_path = "data/parsed/latest_supplier_id.txt"
    with open(latest_path,"w") as f:
        f.write(supplier_id)

def load_parsed_products(supplier_id: str)->list :
    filepath = f"data/parsed/{supplier_id}_products.json"
    if not os.path.exists(filepath):
        raise FileNotFoundError("Supplier data not found")
    with open(filepath) as f:
        return json.load(f)
    

    
def get_latest_supplier_id()->str:
    path = "data/parsed/latest_supplier_id.txt"
    if not os.path.exists(path):
        raise FileNotFoundError("No suppplier data uploaded yet")
    with open(path) as f:
        return f.read().strip()