#app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import eco_score,parse_supplier,product,certs,greener

app = FastAPI(tittle = "Eco Backend")

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"],

)

#Register Routes 
app.include_router(eco_score.router, prefix="/api", tags = ["Eco Score"])
app.include_router(parse_supplier.router, prefix="/api", tags=["Supplier Parsing"])
app.include_router(product.router, prefix="/api", tags =["Products"])
app.include_router(greener.router, prefix="/api", tags =["Greener Alternatives"])