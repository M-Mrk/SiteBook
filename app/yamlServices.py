from pydantic import BaseModel, Extra, ValidationError, RootModel
from typing import Dict, Optional
from . import errorHandling
import yaml
import os

class Entry(BaseModel):
    url: Optional[str] = None
    picture: Optional[str] = None
    description: Optional[str] = None

    class Config:
        extra = Extra.forbid

class Entries(RootModel[Dict[str, Entry]]):
    root: Dict[str, Entry]

def validateEntries():
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entriesPath = os.path.join(baseDir, "entries.yaml")
    if not os.path.exists(entriesPath):
        with open(entriesPath, "x") as file:
            file.write("# Example entries.yaml\n# Add your entries here in the format:\n# name:\n#   feature1:\n#   feature2:\n#   ...\n# Look at the documentation for more details.")
        return f"entries.yaml not found at {entriesPath}. Created a new example file."
    with open(entriesPath, "r") as file:
        try:
            data = yaml.safe_load(file)
            Entries.model_validate(data)
            errorHandling.removeErrors() 
        except (yaml.YAMLError, ValidationError) as exc:
            output = f"Error in entries.yaml: {exc}"
            errorHandling.setError(output)
            return output

def validateYaml():
    output = None
    entriesError = validateEntries()
    if entriesError:
        output = f"Error in entries.yaml: {entriesError}"
    return output

def loadEntriesYaml():
    error = validateEntries()
    if error:
        return
    
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entriesPath = os.path.join(baseDir, "entries.yaml")
    with open(entriesPath, "r") as file:
        try:
            entries = yaml.safe_load(file)
            return entries
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")
            errorHandling.setError(f"Error loading YAML file: {exc}")
            return None