from pydantic import ValidationError
from typing import Dict
from .validationModels import EntryModel, SettingsModel
from . import errorHandling
from .services import getPictureLink
import yaml
import os
from colorama import Fore

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
        bool: True if the file was created, False if not.
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
        return True
        
    except PermissionError as e:
        errorHandling.setError(
            message=e,
            origin="entries.yaml",
            category="FILESYSTEM.PERMISSION"
        )
        return False

    except OSError as e:
        errorHandling.setError(
            message=e,
            origin="entries.yaml",
            category="FILESYSTEM.ERROR"
        )
        return False
    
    except Exception as e:
        errorHandling.setError(
            message=e,
            origin="entries.yaml",
            category="UNKNOWN"
        )
        return False

def createExampleSettingsYaml():
    """
    Creates an example settings.yaml file if it does not exist.
    
    Returns:
        bool: True if the file was created, False if not.
    """
    try:
        settingsPath = getYamlFilePath("settings.yaml")
        
        if os.path.exists(settingsPath):
            return False
        
        with open(settingsPath, "w", encoding="utf-8") as file:
            example_content = """# Example settings.yaml
# Configure your SiteBook application settings here
"""
            file.write(example_content)
        
        return True
        
    except PermissionError as e:
        errorHandling.setError(
            message=e,
            origin="settings.yaml",
            category="FILESYSTEM.PERMISSION"
        )
        return False

    except OSError as e:
        errorHandling.setError(
            message=e,
            origin="settings.yaml",
            category="FILESYSTEM.ERROR"
        )
        return False
    
    except Exception as e:
        errorHandling.setError(
            message=e,
            origin="settings.yaml",
            category="UNKNOWN"
        )
        return False

def validateEntries():
    """
    Validates the entries.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.

    args:
        None

    returns:
        None
    """
    try:
        entriesPath = getYamlFilePath("entries.yaml")

        if not os.path.exists(entriesPath):
            createExampleEntriesYaml()
            return

        with open(entriesPath, "r", encoding="utf-8") as file:
            errorHandling.removeErrorByOrigin(origin="entries.yaml")

            data = yaml.safe_load(file)

            if data is None:
                return

            EntryModel.model_validate(data)

            return

    except yaml.YAMLError as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category="CONFIG.SYNTAX"
        )

    except ValidationError as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category="VALIDATION.STRUCTURE"
        )

    except PermissionError as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category="FILESYSTEM.PERMISSION"
        )

    except Exception as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category="UNKNOWN"
        )

def validateSettings():
    """
    Validates the settings.yaml file, checking if it exists and if it is valid.
    If it does not exist, it creates a new example file.

    args:
        None

    returns:
        None
    """
    try:
        settingsPath = getYamlFilePath("settings.yaml")

        if not os.path.exists(settingsPath):
            createExampleSettingsYaml()
            return

        with open(settingsPath, "r", encoding="utf-8") as file:
            errorHandling.removeErrorByOrigin(origin="settings.yaml")

            data = yaml.safe_load(file)

            if data is None:
                return

            SettingsModel.model_validate(data)

            return None

    except yaml.YAMLError as exc:
        errorHandling.setError(
            message=exc,
            origin="settings.yaml",
            category="CONFIG.SYNTAX"
        )

    except ValidationError as exc:
        errorHandling.setError(
            message=exc,
            origin="settings.yaml",
            category="VALIDATION.STRUCTURE"
        )

    except PermissionError as exc:
        errorHandling.setError(
            message=exc,
            origin="settings.yaml",
            category="FILESYSTEM.PERMISSION"
        )

    except Exception as exc:
        errorHandling.setError(
            message=exc,
            origin="settings.yaml",
            category="UNKNOWN"
        )

def validateYaml():
    """
    Validates all YAML files by calling each validation function.

    args:
        None

    returns:
        None
    """
    print("Validating YAML files...")

    validateEntries()
    validateSettings()

def loadEntriesYaml():
    """
    Loads, validates and returns all entries from entries.yaml

    args:
        none

    returns:
        the parsed entries or None if an error occurred
    """
    validateEntries()
    if errorHandling.errorExists():
        return
    
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entriesPath = os.path.join(baseDir, "entries.yaml")
    with open(entriesPath, "r") as file:
        try:
            entries = yaml.safe_load(file)

            if entries is None:
                return {}

            for name, entry in entries.items(): # Converting Entries with just the name into dict so it does not cause problems
                if entry is None: # check if entries data is None 
                    entries[name] = {} # create empty dict

            return entries
        except yaml.YAMLError as exc:
            errorHandling.setError(
                message=exc,
                origin="entries.yaml",
                category="CONFIG.SYNTAX"
            )
            return None
        
        except PermissionError as exc:
            errorHandling.setError(
                message=exc,
                origin="entries.yaml",
                category="FILESYSTEM.PERMISSION"
            )
            return None

        except Exception as exc:
            errorHandling.setError(
                message=exc,
                origin="entries.yaml",
                category="UNKNOWN"
            )
            return None

def loadSettingsYaml():
    """
    Loads, validates and returns all settings from settings.yaml

    args:
        none

    returns:
        the parsed settings or None if an error occurred
    """
    validateSettings()
    if errorHandling.errorExists():
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

def restoreYaml(fileName: str, data = None, truncatePosition = None):
    """
    Method to restore Yaml file contents. Automatically handles further exceptions.

    args:
        filename: the name of the file to restore (e.g. "settings.yaml")
        Either:
        - data: the data to write to the file. Truncates the file and then writes the data.
        - truncatePosition: the position to trucate the file. (NO DATA BEING WRITEN)

        If both are set an exception is raised

    returns:
        none or raises RuntimeError if restoration fails

    """
    print("Restoring ...")
    filePath = getYamlFilePath(fileName)
    try:
        if data is None and truncatePosition is None:
            raise ValueError("Provided data for restoration is None and truncatePosition is also None")
        
        if data is not None and truncatePosition is not None:
            raise ValueError("Both data and truncatePosition are set, only set one of them. If you have data to write, set only data.")
        
        if not filePath:
            raise ValueError(f"The filename: {fileName} did not return a valid path")

        if truncatePosition is None:
            fileMode = "w"
        else:
            fileMode = "r+"

        with open(filePath, fileMode, encoding="utf-8") as file:
            if truncatePosition is not None:
                file.seek(truncatePosition)
                file.truncate()
            else:
                file.write(data)

    except Exception as exc:
        print(Fore.RED + f"""
Critical error was raised. What happend:
\t1. Write to {fileName} was called
\t2. An error was raised while writing, which let to a restoration of the original content
\t3. Then this critical error occured while writing the original content: {exc}

Current Errors:
\t{errorHandling.getErrorsPrintable()}
""")
        raise RuntimeError(f"Failed to restore {fileName}, stopping application.")

def writeYamlFile(fileName: str, data: Dict, filterNoneValues: bool = True):
    """
    Writes data to a YAML file.

    args:
        fileName (str): The name of the YAML file.
        data (Dict): The data to write to the YAML file.
        filterNoneValues (bool): Whether it should filter out keys which are None, defaults to True

    returns:
        none
    """
    currentData = None
    try:
        filePath = getYamlFilePath(fileName)

        if not os.path.exists(filePath):
            errorMsg = f"File {filePath} does not exist, aborting write."
            errorHandling.setError(
                message=errorMsg,
                origin=fileName,
                category='FILESYSTEM.NONEXISTENT'
                )
            return

        # Read file to restore in case of error
        with open(filePath, "r", encoding="utf-8") as file:
            currentData = file.read()

        if filterNoneValues:
            data = filterNoneOut(data)

        with open(filePath, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

        # Validate the written file
        validateYaml()
        if errorHandling.errorExists(): # Check if an error was raised.
            restoreYaml(fileName="settings.yaml", data=currentData) # Restore the original content
        return

    except yaml.YAMLError as exc:
        errorHandling.setError(
            message=exc,
            origin=fileName,
            category='CONFIG.SYNTAX'
            )

    except PermissionError as exc:
        errorHandling.setError(
            message=exc,
            origin=fileName,
            category='FILESYSTEM.PERMISSION'
            )

    except Exception as exc:
        errorHandling.setError(
            message=exc,
            origin=fileName,
            category='UNKNOWN'
            )
    
    restoreYaml(fileName="settings.yaml", data=currentData) # Also restore if an exception occured.

def appendEntry(entryName: str, entryData: Dict):
    """
    Appends a new entry to the entries.yaml file.

    args:
        entryName (str): The name of the entry to append.
        entryData (Dict): The data of the entry to append.

    returns:
        None
    """
    entry = {}
    entry[entryName] = entryData

    filePath = getYamlFilePath("entries.yaml")

    currentPosition = None
    try:
        with open(filePath, "a", encoding= "UTF-8") as file:
            currentPosition = file.tell() # Get the current end of the file
            file.write("\n") # Add a new line

        with open(filePath, "a", encoding="UTF-8") as file: # Reopen file so newline doesnt get over written
            yaml.dump(entry, file, default_flow_style=False, allow_unicode=True)

        validateYaml()
        if errorHandling.errorExists():
            print("Boing")
            restoreYaml(fileName="entries.yaml", truncatePosition=currentPosition)
        return
    
    except yaml.YAMLError as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category='CONFIG.SYNTAX'
            )

    except PermissionError as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category='FILESYSTEM.PERMISSION'
            )

    except Exception as exc:
        errorHandling.setError(
            message=exc,
            origin="entries.yaml",
            category='UNKNOWN'
            )
    
    restoreYaml(fileName="entries.yaml", truncatePosition=currentPosition)

