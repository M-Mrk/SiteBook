class Error:
    """
    Represents an error with an origin and a message.

    Attributes:
        origin (str): The origin of the error, e.g. the file where it occurred.
        message (str): The error message.
    """
    def __init__(self, origin: str, message: str):
        self.origin = origin
        self.message = message

errors = []

def setError(message: str, origin: str = "Unknown"):
    """
    Sets an error with a message and an optional origin.
    The origin is necessary so that the error can be resolved in runtime and not need an restart.

    args:
        message (str): The error message to set.
        origin (str): The origin of the error, e.g. the file where it occurred, while in validation the yaml file name is used. Defaults to "Unknown".
    
    returns:
        None
    """
    error = Error(origin=origin, message=message)
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
    
def removeErrorByOrigin(origin: str):
    """
    Removes all errors with the specified origin.

    args:
        origin (str): The origin of the errors to remove e.g. entries.yaml.

    returns:
        None
    """
    global errors
    for error in errors:
        if error.origin == origin:
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
    return "\n".join([f"{error.origin}: {error.message}" for error in getErrors()])