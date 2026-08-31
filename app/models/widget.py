import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Text
from app.core.database import Base

class Widget(Base):
    __tablename__ = "widgets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    button_text = Column(String(100), default="Submit")
    form_fields = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)