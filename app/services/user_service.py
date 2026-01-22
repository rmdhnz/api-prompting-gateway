from sqlalchemy.orm import Session
from app.models.user_model import User


def get_or_create_user(
    db: Session,
    baus_user_id: int,
    username: str,
):
    user = (
        db.query(User)
        .filter(User.baus_user_id == baus_user_id)
        .first()
    )

    if user:
        return user

    user = User(
        baus_user_id=baus_user_id,
        username=username,
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
