from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class SubmissionCreate(BaseModel):
    widget_id: str = Field(..., description="UUID of the target widget")
    email: EmailStr = Field(..., description="Visitor email address")
    name: Optional[str] = Field(None, max_length=100)
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Honeypot field: Must remain empty in real requests.
    # If filled, it indicates an automated spam bot.
    website_hp: Optional[str] = Field(None, alias="website")

class SubmissionResponse(BaseModel):
    status: str
    submission_id: str
    message: str