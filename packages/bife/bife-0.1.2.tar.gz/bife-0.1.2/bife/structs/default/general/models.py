import uuid
from datetime import datetime

from libs.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class TodoModel(Base):

    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String(60), init=False, default_factory=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(String(60), nullable=False)
