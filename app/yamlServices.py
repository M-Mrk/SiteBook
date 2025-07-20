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

def getYamlFilePath(fileName: str) -> str:
    """
    Returns the absolute path of a YAML file given its name.

    args:
        fileName (str): The name of the YAML file.

    returns:
        str: The absolute path to the YAML file.
    """
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(baseDir, fileName)

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
    entriesPath = getYamlFilePath("entries.yaml")
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
    settingsPath = getYamlFilePath("settings.yaml")
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
        
def writeToYaml(fileName: str, data: Dict, filterNoneOut=True):
    """
    Writes data to a YAML file.

    args:
        filePath (str): The path to the YAML file.
        data (Dict): The data to write to the YAML file.
        filterNoneOut (bool): Whether it should filter out keys which are None, defaults to True

    returns:
        bool: True if there was an error writing to the file, False if successful.
    """
    filePath = getYamlFilePath(fileName)
    if not os.path.exists(filePath):
        print(f"File {filePath} does not exist, aborting write.")
        return True
    
    #Read File to restore in case of error
    with open(filePath, "r") as file:
        currentData = file.read()

    if filterNoneOut:
        data = {key: value for key, value in data.items() if value is not None}

    with open(filePath, "w+") as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
        if validateYaml():
            print(f"Error writing to {filePath}. Validation failed.")
            
            file.seek(0)           # Move to the start of the file
            file.truncate()        # Clear the file contents
            file.write(currentData)  # Restore previous content if validation fails
            return True
        return False