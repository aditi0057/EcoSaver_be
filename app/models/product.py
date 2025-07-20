from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    product_name: str
    brand: Optional[str] = ""
    category: Optional[str] = ""
    product_description: Optional[str] = ""
    product_weight_or_volume: Optional[str] = ""
    actual_price: Optional[float] = 0.0
    selling_price: Optional[float] = 0.0
    discount: Optional[float] = 0.0
    avg_rating: Optional[float] = 0.0
    out_of_stock: Optional[bool] = False
    packing_material_type: Optional[str] = ""
    packing_material_weight: Optional[str] = ""
    shipping_packaging: Optional[str] = ""
    is_sustainable: Optional[bool] = False  # Will be overwritten later
    sustainability_factors: Optional[str] = ""
    certification_tags: Optional[str] = ""
    end_of_life_disposal: Optional[str] = ""
    image_url: Optional[str] = None
