from sqlalchemy.orm import Session
from . import models


def get_or_create_demo_user(db: Session) -> models.User:
    demo_email = "demo@salealertbot.local"
    user = db.query(models.User).filter(models.User.email == demo_email).first()
    if user:
        return user

    user = models.User(email=demo_email, hashed_password="not-used-yet")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_tracked_product(
    db: Session,
    user_id: int,
    product_url: str,
    target_price: int | None,
) -> models.TrackedProduct:
    product = models.TrackedProduct(
        user_id=user_id,
        product_url=product_url,
        target_price=target_price,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_tracked_products(db: Session, user_id: int) -> list[models.TrackedProduct]:
    return (
        db.query(models.TrackedProduct)
        .filter(models.TrackedProduct.user_id == user_id)
        .order_by(models.TrackedProduct.id.desc())
        .all()
    )
