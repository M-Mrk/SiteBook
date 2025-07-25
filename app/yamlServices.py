from pydantic import BaseModel, ValidationError, RootModel
from typing import Dict, Optional
from .validationModels import EntryModel, SettingsModel
from . import errorHandling
import yaml
import os

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

def createExampleEntriesYaml():
    """
    Creates an example entries.yaml file if it does not exist.
    
    Returns:
        bool: True if the file was created, False if it already exists.
    
    Raises:
        PermissionError: If unable to write to the directory
        OSError: If there's a critical file system error
    """
    try:
        entriesPath = getYamlFilePath("entries.yaml")
        
        if os.path.exists(entriesPath):
            return False
        
        with open(entriesPath, "w", encoding="utf-8") as file:
            example_content = """# Example entries.yaml
# Add your entries here in the format:
# entry_name:
#   url: "https://example.com"
#   description: "A brief description"
#
# Example:
# homeassistant:
#   url: "http://192.168.2.15:8123"
#   description: "My Home Assistant instance"
"""
            file.write(example_content)
        
        errorHandling.setError(
            message=f"entries.yaml not found. Created example file at {entriesPath}. Please add your entries and restart the application.",
            origin="entries.yaml"
        )
        return True
        
    except PermissionError as e:
        raise PermissionError(f"Unable to create entries.yaml, permission denied: {e}")
    
    except OSError as e:
        raise OSError(f"File system error while creating entries.yaml: {e}")
    
    except Exception as e:
        errorHandling.setError(
            message=f"Unexpected error creating entries.yaml: {e}",
            origin="entries.yaml"
        )
        raise RuntimeError(f"Unexpected error creating example entries file: {e}")

def createExampleSettingsYaml():
    """
    Creates an example settings.yaml file if it does not exist.
    
    Returns:
        bool: True if the file was created, False if it already exists.
    
    Raises:
        PermissionError: If unable to write to the directory
        OSError: If there's a critical file system error
    """
    try:
        settingsPath = getYamlFilePath("settings.yaml")
        
        if os.path.exists(settingsPath):
            return False
        
        with open(settingsPath, "w", encoding="utf-8") as file:
            example_content = """# Example settings.yaml
# Configure your SiteBook application settings here
#
"""
            file.write(example_content)
        
        errorHandling.setError(
            message=f"settings.yaml not found. Created example file at {settingsPath}. Please configure your settings and restart the application.",
            origin="settings.yaml"
        )
        return True
        
    except PermissionError as e:
        raise PermissionError(f"Unable to create settings.yaml - permission denied: {e}")
    
    except OSError as e:
        raise OSError(f"File system error while creating settings.yaml: {e}")
    
    except Exception as e:
        errorHandling.setError(
            message=f"Unexpected error creating settings.yaml: {e}",
            origin="settings.yaml"
        )
        raise RuntimeError(f"Unexpected error creating example settings file: {e}")

def validateEntries():
    """
    Validates the entries.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.

    Returns:
        str: Error message if validation fails, None if successful.
    """
    try:
        entriesPath = getYamlFilePath("entries.yaml")

        if not os.path.exists(entriesPath):
            createExampleEntriesYaml()
            return f"entries.yaml not found at {entriesPath}. Created a new example file."

        with open(entriesPath, "r", encoding="utf-8") as file:
            errorHandling.removeErrorByOrigin(origin="entries.yaml")

            data = yaml.safe_load(file)

            if data is None:
                errorMsg = "entries.yaml is empty or contains only comments."
                errorHandling.setError(message=errorMsg, origin="entries.yaml")
                return errorMsg

            EntryModel.model_validate(data)

            return None

    except yaml.YAMLError as exc:
        errorMsg = f"Invalid YAML syntax: {exc}"
        errorHandling.setError(message=errorMsg, origin="entries.yaml")
        return errorMsg

    except ValidationError as exc:
        errorMsg = f"Invalid entry structure: {exc}"
        errorHandling.setError(message=errorMsg, origin="entries.yaml")
        return errorMsg

    except PermissionError as exc:
        raise PermissionError(f"Cannot read entries.yaml - permission denied: {exc}")

    except Exception as exc:
        errorMsg = f"Unexpected validation error: {exc}"
        errorHandling.setError(message=errorMsg, origin="entries.yaml")
        return errorMsg

def validateSettings():
    """
    Validates the settings.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.

    Returns:
        str: Error message if validation fails, None if successful.
    """
    try:
        settingsPath = getYamlFilePath("settings.yaml")

        if not os.path.exists(settingsPath):
            createExampleSettingsYaml()
            return f"settings.yaml not found at {settingsPath}. Created a new example file."

        with open(settingsPath, "r", encoding="utf-8") as file:
            errorHandling.removeErrorByOrigin(origin="settings.yaml")

            data = yaml.safe_load(file)

            if data is None:
                data = {}

            SettingsModel.model_validate(data)

            return None

    except yaml.YAMLError as exc:
        errorMsg = f"Invalid YAML syntax in settings: {exc}"
        errorHandling.setError(message=errorMsg, origin="settings.yaml")
        return errorMsg

    except ValidationError as exc:
        errorMsg = f"Invalid settings configuration: {exc}"
        errorHandling.setError(message=errorMsg, origin="settings.yaml")
        return errorMsg

    except PermissionError as exc:
        raise PermissionError(f"Cannot read settings.yaml, permission denied: {exc}")

    except Exception as exc:
        errorMsg = f"Unexpected validation error: {exc}"
        errorHandling.setError(message=errorMsg, origin="settings.yaml")
        return errorMsg

def validateYaml():
    """
    Validates all YAML files by calling each validation function.
    Returns:
        str: Error message if any validation fails, None if all validations are successful.
    """
    print("Validating YAML files...")
    output = None

    entriesError = validateEntries()
    if entriesError:
        output = entriesError

    settingsError = validateSettings()
    if settingsError:
        output = settingsError if output is None else f"{output}\n{settingsError}"

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

def filterNoneOut(data: Dict):
    """
    Filter out None values even when nested.
    
    Args:
        data: The data structure to filter (dict, list, or other)
        
    Returns:
        Filtered data structure with None values removed
    """

    filtered = {}
    for key, value in data.items():
        if value is not None:
            if isinstance(value, dict):
                filtered_value = filterNoneOut(value)
                if filtered_value:
                    filtered[key] = filtered_value
            elif isinstance(value, list):
                filtered_list = []
                for item in value:
                    if item is not None:
                        if isinstance(item, dict):
                            filtered_item = filterNoneOut(item)
                            if filtered_item:
                                filtered_list.append(filtered_item)
                        else:
                            filtered_list.append(item)
                if filtered_list:
                    filtered[key] = filtered_list
            else:
                filtered[key] = value
    return filtered

def writeYamlFile(fileName: str, data: Dict, filterNoneValues: bool = True):
    """
    Writes data to a YAML file.

    args:
        fileName (str): The name of the YAML file.
        data (Dict): The data to write to the YAML file.
        filterNoneValues (bool): Whether it should filter out keys which are None, defaults to True

    returns:
        bool: True if there was an error writing to the file, False if successful.
    """
    try:
        filePath = getYamlFilePath(fileName)

        if not os.path.exists(filePath):
            errorMsg = f"File {filePath} does not exist, aborting write."
            print(errorMsg)
            errorHandling.setError(message=errorMsg, origin=fileName)
            return True

        # Read file to restore in case of error
        with open(filePath, "r", encoding="utf-8") as file:
            currentData = file.read()

        if filterNoneValues:
            data = filterNoneOut(data)

        with open(filePath, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

        # Validate the written file
        validationError = validateYaml()
        if validationError:
            errorMsg = f"Error writing to {filePath}. Validation failed: {validationError}"
            print(errorMsg)
            errorHandling.setError(message=errorMsg, origin=fileName)

            # Restore previous content if validation fails
            with open(filePath, "w", encoding="utf-8") as file:
                file.write(currentData)
            return True

        return False

    except yaml.YAMLError as exc:
        errorMsg = f"YAML error while writing to {fileName}: {exc}"
        print(errorMsg)
        errorHandling.setError(message=errorMsg, origin=fileName)
        return True

    except PermissionError as exc:
        errorMsg = f"Permission denied while writing to {fileName}: {exc}"
        print(errorMsg)
        errorHandling.setError(message=errorMsg, origin=fileName)
        return True

    except Exception as exc:
        errorMsg = f"Unexpected error while writing to {fileName}: {exc}"
        print(errorMsg)
        errorHandling.setError(message=errorMsg, origin=fileName)
        return True