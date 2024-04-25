import uuid
from datetime import datetime

from libs.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String(60), init=False, default_factory=lambda: str(uuid.uuid4())
    )

    username: Mapped[str] = mapped_column(String(60), nullable=False)
    fullname: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False)

    is_admin: Mapped[bool] = mapped_column(default=False)
    disabled: Mapped[bool] = mapped_column(default=False)

    member_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now()
    )
