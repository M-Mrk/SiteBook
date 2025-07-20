from pydantic import BaseModel, RootModel
from typing import Dict, Optional

class Entry(BaseModel): #List all allowed fields for an entry
    url: Optional[str] = None
    picture: Optional[str] = None
    description: Optional[str] = None

    class Config:
        extra = 'forbid'

class EntryModel(RootModel[Dict[str, Entry]]): #Basically says that any key in the dictionary is a string and the value is an Entry object
    root: Dict[str, Entry]