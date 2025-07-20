from pydantic import BaseModel
from typing import Optional

class SettingsModel(BaseModel):
    secretKey: Optional[str] = None
    theme: Optional[str] = None
    searchbar: Optional[bool] = None
    
    class Config:
        extra = 'forbid'
