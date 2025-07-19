from pydantic import BaseModel, Extra, ValidationError, RootModel
from typing import Dict, Optional
from . import errorHandling
import yaml
import os

def createExampleEntriesYaml():
    """
    Creates an example entries.yaml file if it does not exist.
    
    args:
        None

    returns:
        True if the file was created, False if it already exists.
    """
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entriesPath = os.path.join(baseDir, "entries.yaml")
    if not os.path.exists(entriesPath):
        with open(entriesPath, "w") as file:
            file.write("# Example entries.yaml\n# Add your entries here in the format:\n# name:\n#   feature1:\n#   feature2:\n#   ...\n# Look at the documentation for more details.")
        errorHandling.setError(message=f"entries.yaml not found at {entriesPath}. Created a new example file. Fill it with your entries and/or restart.", origin="entries.yaml")
        return True
    return False

# Validating entries.yaml
class Entry(BaseModel): #List all allowed fields for an entry
    url: Optional[str] = None
    picture: Optional[str] = None
    description: Optional[str] = None

    class Config:
        extra = 'forbid'

class Entries(RootModel[Dict[str, Entry]]): #Basically says that any key in the dictionary is a string and the value is an Entry object
    root: Dict[str, Entry]

def validateEntries():
    """
    Validates the entries.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.
    """
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entriesPath = os.path.join(baseDir, "entries.yaml")
    if not os.path.exists(entriesPath):
        createExampleEntriesYaml()
        return f"entries.yaml not found at {entriesPath}. Created a new example file."
    with open(entriesPath, "r") as file:
        try:
            errorHandling.removeErrorByOrigin(origin="entries.yaml")  # Remove any previous errors of entries.yaml
            data = yaml.safe_load(file)
            Entries.model_validate(data)
        except (yaml.YAMLError, ValidationError) as exc:
            output = f"Error in entries.yaml: {exc}"
            errorHandling.setError(message=f"{exc}", origin="entries.yaml")
            return output

# Validating settings.yaml


def validateYaml():
    """
    Validates all YAML files, by calling each validation function.
    Remember that the validation functions also call the errorHandling functions to set errors if validation fails.`

    args:
        None

    returns:
        str: Error message if validation fails, None if successful
    """
    print("Validating YAML files...")
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
            errorHandling.setError(message=f"Error loading YAML file: {exc}", origin="entries.yaml")
            return None