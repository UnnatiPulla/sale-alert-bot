from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models  # noqa
from . import crud, schemas
from .deps import get_db
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import unquote
from typing import List



app = FastAPI(title="Sale Alert Bot")

@app.get("/")
def root():
    return {"message": "Sale Alert Bot API is running"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db_ok": result == 1}

@app.post("/track", response_model=schemas.TrackProductResponse)
def track_product(payload: schemas.TrackProductRequest, db: Session = Depends(get_db)):
    user = crud.get_or_create_demo_user(db)
    product = crud.create_tracked_product(
        db=db,
        user_id=user.id,
        product_url=str(payload.product_url),
        target_price=payload.target_price,
    )
    return schemas.TrackProductResponse(
        id=product.id,
        product_url=product.product_url,
        target_price=product.target_price,
    )

@app.get("/add/{encoded_url:path}")
def add_via_prefix_url(encoded_url: str, db: Session = Depends(get_db)):
    product_url = unquote(encoded_url)

    if not product_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid product URL")

    user = crud.get_or_create_demo_user(db)
    product = crud.create_tracked_product(
        db=db,
        user_id=user.id,
        product_url=product_url,
        target_price=None,
    )

    # simple redirect to docs for now (we'll build a real UI later)
    return {"added_id": product.id, "product_url": product.product_url}

@app.get("/products", response_model=List[schemas.TrackedProductListItem])
def list_products(db: Session = Depends(get_db)):
    user = crud.get_or_create_demo_user(db)
    products = crud.list_tracked_products(db, user.id)
    return [
        schemas.TrackedProductListItem(
            id=p.id,
            product_url=p.product_url,
            target_price=p.target_price,
        )
        for p in products
    ]
