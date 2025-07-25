from pydantic import BaseModel
from typing import Optional

class FlaskSettings(BaseModel):
    secretKey: Optional[str] = None
    port: Optional[int] = None
    host: Optional[str] = None
    debug: Optional[bool] = None

    class Config:
        extra = 'forbid'

class SettingsModel(BaseModel):
    server: Optional[FlaskSettings] = None
    theme: Optional[str] = None
    searchbar: Optional[bool] = None
    
    class Config:
        extra = 'forbid'
