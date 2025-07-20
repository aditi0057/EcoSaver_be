from fastapi import APIRouter, HTTPException
from app.models.product import ProductCreate
from typing import List, Optional
from pydantic import BaseModel
from rapidfuzz import fuzz
from app.services.utils import get_eco_score, get_products_by_supplier

router = APIRouter()

class CartItem(BaseModel):
    product_id: int
    product_name: str
    brand: str
    material: Optional[str] = ""
    eco_score: int

class EcoScoreResponse(BaseModel):
    product_id: int
    product_name: str
    eco_score: int

class AlternativeMatch(BaseModel):
    original: CartItem
    alternative: Optional[EcoScoreResponse]
@router.post("/cart/greener-options", response_model=List[AlternativeMatch])
async def get_greener_alternatives(cartItems: List[CartItem]):
    try:
        products = get_products_by_supplier()
        matches = []

        for cart_item in cartItems:
            best_alternative = None
            best_combined_score = 0
            best_eco_score = 0

            for prod in products:
                if prod["product_id"] == cart_item.product_id:
                    continue

                # Compute fuzzy match scores
                name_score = fuzz.partial_ratio(cart_item.product_name.lower(), prod["product_name"].lower())
                brand_score = fuzz.partial_ratio(cart_item.brand.lower(), prod["brand"].lower())
                material_score = fuzz.partial_ratio((cart_item.material or "").lower(), (prod.get("material") or "").lower())

                # Weighted score — prioritize name heavily
                combined_score = 0.6 * name_score + 0.2 * brand_score + 0.2 * material_score

                # Skip unrelated items
                if name_score < 60:  # name must be reasonably close
                    continue

                try:
                    eco_data = get_eco_score(prod["product_id"])
                except Exception:
                    continue

                eco_score = eco_data.get("eco_score", 0)

                # Only consider alternatives significantly greener
                if eco_score > cart_item.eco_score + 5:
                    if combined_score > best_combined_score or (
                        combined_score == best_combined_score and eco_score > best_eco_score
                    ):
                        best_alternative = EcoScoreResponse(**eco_data)
                        best_combined_score = combined_score
                        best_eco_score = eco_score

            matches.append({
                "original": cart_item,
                "alternative": best_alternative
            })

        return matches

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
