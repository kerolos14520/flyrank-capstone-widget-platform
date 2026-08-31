from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class WidgetConfigResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: Optional[str]
    button_text: str
    form_fields: List[Dict[str, Any]]

    class Config:
        from_attributes = True