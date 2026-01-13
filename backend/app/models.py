from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    products = relationship("TrackedProduct", back_populates="user")


class TrackedProduct(Base):
    __tablename__ = "tracked_products"

    id = Column(Integer, primary_key=True, index=True)
    product_url = Column(String, nullable=False)
    target_price = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="products")
