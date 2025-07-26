class Error:
    """
    Represents an error with an origin and a message.

    Attributes:
        origin (str): The origin of the error, e.g. the file where it occurred.
        message (str): The error message.
    """
    def __init__(self, category: str, origin: str, message: str):
        self.category = category
        self.origin = origin
        self.message = message

errors = []
errorPreventedStart = False

recoverableCategories = {'VALIDATION', 'CONFIG', 'SERVICES'} # These Categories of errors will be cleared on load
criticalCategories = {'SERVER', 'FILESYSTEM', 'NETWORK', 'UNKNOWN'} # These Categories will require manual intervention

def checkIfTopCategoryExists(category: str):
    """
    Checks if given category is part of the recoverable or critical categories.

    args:
        category (str): The category to check, e.g. VALIDATION, SERVER, etc.

    returns:
        bool: True if the category exists, False otherwise.
    """
    if category not in recoverableCategories and category not in criticalCategories:
        return False
    else:
        return True

def setError(message: str, origin: str = "Unknown", category: str = "UNKNOWN"):
    """
    Sets an error with a message, category and an optional origin.
    The top category must be part of either the recoverableCategories {VALIDATION, CONFIG, SERVICES}
    or in the criticalCategories {SERVER, FILESYSTEM, NETWORK, UNKNOWN}.
    The category is always Uppercase. After the top category there is an optional subCategory
    like TOPCATEGORY.SUBCATEGORY or VALIDATION.EXTRA.

    args:
        message (str): The error message to set.
        origin (str): The origin of the error, e.g. the file where it occurred, while in validation the yaml file name is used. Defaults to "Unknown".
    
    returns:
        None
    """
    splitCategories = category.split(".")
    if not checkIfTopCategoryExists(splitCategories[0]):
        raise ValueError(f"Category '{category}' does not exist. Please use one of the following: {', '.join(recoverableCategories.union(criticalCategories))}")
    error = Error(origin=origin, message=message, category=category)
    errors.append(error)

def errorExists():
    """
    Checks if there are any errors set.

    args:
        None

    returns:
        bool: True if there are errors, False otherwise.
    """
    if len(errors) > 0:
        return True
    else:
        return False
    
def removeErrorByOrigin(origin: str, evenCritical: bool = False):
    """
    Removes all errors with the specified origin.

    args:
        origin (str): The origin of the errors to remove e.g. entries.yaml.
        evenCritical (bool): If True, also removes critical errors. Defaults to False. Shouldnt be used in most cases.

    returns:
        None
    """
    global errors
    for error in errors:
        if error.origin == origin:
            if not evenCritical:
                if error.category not in criticalCategories:
                    errors.remove(error)
            else:
                errors.remove(error)

def removeErrorByCategory(category: str):
    """
    Removes all errors with the specified category.

    args:
        category (str): The category of the errors to remove e.g. VALIDATION.

    returns:
        None
    """
    global errors
    for error in errors:
        if error.category == category:
            errors.remove(error)

def removeAllRecoverableErrors():
    """
    Removes all errors whose category is a part of recoverableCategories.

    args:
        None

    returns:
        None
    """
    global errors
    for error in errors:
        if error.category in recoverableCategories:
            errors.remove(error)

def removeAllErrors():
    """
    Removes all errors.

    args:
        None

    returns:
        None
    """
    global errors
    errors = []

def getErrors():
    """
    Gets all errors.
    Erros have the following attributes:
        - origin: The origin of the error, e.g. the file where it occurred.
        - message: The error message.
        - category: The category of the error, e.g. VALIDATION, SERVER, etc.

    args:
        None

    returns:
        list: A list of all errors.
    """
    return errors

def getErrorsPrintable():
    """
    Gets all errors in a printable format.

    args:
        None

    returns:
        str: A string representation of all errors.
    """
    output = ""
    for error in errors:
        output += f"{error.category} in {error.origin}:\n\t{error.message}\n"
    return output.strip()

def setErrorPreventedStart():
    """
    Sets the status that an error prevented correct startup.
    This will put the flask app into an error only state where it only shows the errors.

    args:
        None

    returns:
        None
    """
    global errorPreventedStart
    errorPreventedStart = True

def errorPreventedStart():
    """
    Checks if an error prevented the correct startup.

    args:
        None

    returns:
        bool: True if an error prevented the correct startup, False otherwise.
    """
    return errorPreventedStart