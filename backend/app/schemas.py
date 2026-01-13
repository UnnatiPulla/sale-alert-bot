from pydantic import BaseModel, HttpUrl
from typing import Optional


class TrackProductRequest(BaseModel):
    product_url: HttpUrl
    target_price: Optional[int] = None


class TrackProductResponse(BaseModel):
    id: int
    product_url: str
    target_price: Optional[int]

class TrackedProductListItem(BaseModel):
    id: int
    product_url: str
    target_price: Optional[int] = None
