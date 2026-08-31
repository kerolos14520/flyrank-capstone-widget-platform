import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    widget_id = Column(String(36), nullable=False, index=True)
    email = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    data = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=False)
    geo_country = Column(String(100), nullable=True)
    geo_city = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)