from .yamlServices import loadSettingsYaml
from .validationModels import SettingsModel


def getSettings():
    """
    Loads the settings from settings.yaml and returns them. 
    Example usage: settings = getSettings() settings.foo or settings.bar

    args:
        None

    returns:
        SettingsModel: An instance of SettingsModel containing the settings.
    If settings.yaml does not exist or is invalid, it returns an empty SettingsModel.
    """
    settings = loadSettingsYaml()
    if settings is None:
        return SettingsModel()  # Return empty SettingsModel instead of dict
    return SettingsModel(**settings)

def checkIfExistsOrIsEmpty(settingsName):
    """
    Checks if a setting exists and is not empty.
    Use to check if there is a corresponding setting set or whether it should use an default value (See app.py's getTheme() for an example). 

    args:
        settingsName (str): The name of the setting to check.

    returns:
        bool: True if the setting exists and is not empty, False otherwise.
    """
    settings = getSettings()
    if not hasattr(settings, settingsName) or getattr(settings, settingsName) is None:
        return False
    return True

#TODO: Add writing settings/yaml functionality. Especially for setting secret_key in app.py