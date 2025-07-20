from pydantic import BaseModel, ValidationError, RootModel
from typing import Dict, Optional
from .validationModels import EntryModel, SettingsModel
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

def createExampleSettingsYaml():
    """
    Creates an example settings.yaml file if it does not exist.
    
    args:
        None

    returns:
        True if the file was created, False if it already exists.
    """
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    settingsPath = os.path.join(baseDir, "settings.yaml")
    if not os.path.exists(settingsPath):
        with open(settingsPath, "w") as file:
            file.write("# Example settings.yaml\n# Add your settings here in the format:\n# feature1:\n#   feature2:\n# Look at the documentation for more details.")
        errorHandling.setError(message=f"settings.yaml not found at {settingsPath}. Created a new example file. Fill it with your settings and/or restart.", origin="settings.yaml")
        return True
    return False

# Validating entries.yaml
def validateEntries():
    """
    Validates the entries.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.

    args:
        None

    returns:
        str: Error message if validation fails, None if successful
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
            EntryModel.model_validate(data)
        except (yaml.YAMLError, ValidationError) as exc:
            output = f"Error in entries.yaml: {exc}"
            errorHandling.setError(message=f"{exc}", origin="entries.yaml")
            return output

# Validating settings.yaml
def validateSettings():
    """
    Validates the settings.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.
    """
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    settingsPath = os.path.join(baseDir, "settings.yaml")
    if not os.path.exists(settingsPath):
        createExampleSettingsYaml()
        return f"settings.yaml not found at {settingsPath}. Created a new example file."
    with open(settingsPath, "r") as file:
        try:
            errorHandling.removeErrorByOrigin(origin="settings.yaml")  # Remove any previous errors of settings.yaml
            data = yaml.safe_load(file)
            SettingsModel.model_validate(data)
        except (yaml.YAMLError, ValidationError) as exc:
            output = f"Error in settings.yaml: {exc}"
            errorHandling.setError(message=f"{exc}", origin="settings.yaml")
            return output

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
        
def loadSettingsYaml():
    error = validateSettings()
    if error:
        return
    
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    settingsPath = os.path.join(baseDir, "settings.yaml")
    with open(settingsPath, "r") as file:
        try:
            settings = yaml.safe_load(file)
            return settings
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")
            errorHandling.setError(message=f"Error loading YAML file: {exc}", origin="settings.yaml")
            return None