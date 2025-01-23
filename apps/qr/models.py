from django.db import models
from pydantic import BaseModel
from datetime import datetime
class QrStyles(BaseModel):
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

