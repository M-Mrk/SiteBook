from .yamlServices import loadSettingsYaml, writeYamlFile
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
        settingsName (str): The name of the setting to check. Seperate with dots for nested settings (e.g. server.debug)

    returns:
        bool: True if the setting exists and is not empty, False otherwise.
    """

    allSettingNames = settingsName.split('.')
    settings = getSettings()
    if len(allSettingNames) > 1:
        for i in range(len(allSettingNames) - 1):
            if i == 0:
                parentObj = getattr(settings, allSettingNames[i], None)
            else:
                parentObj = getattr(parentObj, allSettingNames[i], None)

            if parentObj is None:
                return False
        if not hasattr(parentObj, allSettingNames[-1]) or getattr(parentObj, allSettingNames[-1]) is None:
            return False 
    else:
        if not hasattr(settings, settingsName) or getattr(settings, settingsName) is None:
            return False
    return True

def setAndWriteSetting(settingsName, value):
    """
    Sets a setting and writes it to settings.yaml.

    Args:
        settingsName (str): e.g. 'theme' or for nested seperated with a dot 'server.port'.
        value: The value to set the setting to.

    Returns:
        none
    """
    allSettingNames = settingsName.split('.')
    settings = getSettings()
    
    settingsDict = settings.model_dump() if hasattr(settings, 'model_dump') else settings.__dict__
    parentObj = settingsDict

    for key in allSettingNames[:-1]:
        if key not in parentObj or parentObj[key] is None:
            parentObj[key] = {}
        parentObj = parentObj[key]

    parentObj[allSettingNames[-1]] = value
    writeYamlFile(fileName="settings.yaml", data=settingsDict, filterNoneValues=True)
