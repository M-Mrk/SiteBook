from typing import get_type_hints, get_origin, get_args, Union
from .validationModels.entries import Entry
from . import errorHandling
import os

def getInputTypeFromHint(hint):
    """
    Convert Python type hints to user-friendly input type strings.
    
    args:
        hint: The type hint from the model field
        
    returns:
        str: User-friendly input type name
    """
    # Handle Optional types (Union[X, None])
    if get_origin(hint) is Union:
        args = get_args(hint)
        if len(args) == 2 and type(None) in args:
            # This is Optional[X], get the non-None type
            non_none_type = next(arg for arg in args if arg is not type(None))
            hint = non_none_type
    
    # Map Python types to user-friendly names
    type_mapping = {
        str: "string",
        int: "integer", 
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object"
    }
    
    return type_mapping.get(hint, "string")

def generateEntryOptions():
    """
    Dynamically generate entry options from the Entry validation model.

    args:
        None
    
    returns:
        list: List of dictionaries with entry option information
    """
    options = []
    
    # Get type hints from the Entry model
    typeHints = get_type_hints(Entry)
    
    # Define descriptions for each field
    fieldDescriptions = {
        "url": "The web address/URL for accessing this service",
        "description": "A brief description of what this service does",
        "picture": "URL to an image/logo representing this service",
    }
    
    for fieldName, fieldType in typeHints.items():
        description = fieldDescriptions.get(fieldName, f"Configuration option for {fieldName}")
        inputType = getInputTypeFromHint(fieldType)
        
        options.append({
            "name": fieldName,
            "description": description,
            "inputType": inputType
        })
    
    return options

# Generate entry options dynamically
entryOptions = generateEntryOptions()

def getEntryOptions():
    """
    Returns a list of entry options.
    Use to keep your theme more flexible and compatible.

    args:
        None

    returns:
        list: A list of dictionaries with entry option information.
              Each dictionary contains:
                - name (str): The name of the entry option.
                - description (str): A brief description of the entry option.
                - inputType (str): The type of input expected for this entry option (e.g. bool, string, integer, etc).
    """
    return entryOptions

def getPictureLink(pictureEntry):
    """
    Gets the filepath of the image if pictureEntry is not a link.

    args:
        pictureEntry: What is set in entry.picture

    returns:
        str: Which can be directly used as image source
    """
    if not pictureEntry:
        errorHandling.setError(message="No Picture Entry was provided when trying to get Link", category="SERVICES.TYPE")
        return None
    if "http" in pictureEntry.lower(): # Is a link to a picture
        return pictureEntry
    else: # Is not a link but a image name
        sliced = pictureEntry.split(".")
        if len(sliced) < 2:
            errorHandling.setError(message=f"Picture file name is wrongly formatted: {pictureEntry}", category="CONFIG.SYNTAX")
            return None
        
        baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imageDir = os.path.join(baseDir, "images")
        imagePath = os.path.join(imageDir, pictureEntry)
        if not os.path.exists(imagePath):
            errorHandling.setError(message=f"Picture: {pictureEntry} does not exist", category="CONFIG.MISSING")
            return None

        return f"images/{pictureEntry}"