from colorama import Fore, init

from app.yamlServices import validateYaml, createExampleEntriesYaml, createExampleSettingsYaml
from app import errorHandling
from app.settingHandling import getSettings, checkIfExistsOrIsEmpty, setAndWriteSetting

print("Starting SiteBook...")

init(autoreset=True) #colorama init

# Create example entries.yaml if it does not exist
if createExampleEntriesYaml():
    print(Fore.YELLOW + "Created example entries.yaml.")
    #TODO find a way to restart and restart automatically, yes but not here

if createExampleSettingsYaml():
    print(Fore.YELLOW + "Created example settings.yaml.")

validateYaml() # Validate YAML files

# Start flask to either run normally or show the validation error(s)
from app.app import app

if errorHandling.errorExists():
    print(Fore.RED + f"Error in YAML file(s): {errorHandling.getErrorsPrintable()}")
else:
    print(Fore.GREEN + "YAML file loaded successfully.")
print("Starting Flask app...")

# Initialization of flask app here
# Settings which will get writtent if they do not exist
try:
    if not checkIfExistsOrIsEmpty('server.port'):
        print(Fore.YELLOW + "No port set. Setting to 5000...")
        setAndWriteSetting(settingsName='server.port', value=5000)

    if not checkIfExistsOrIsEmpty('server.secretKey'):
        print(Fore.YELLOW + "No secretKey set. Generating a new one...")
        import secrets
        setAndWriteSetting(settingsName='server.secretKey', value=secrets.token_urlsafe(32))
    settings = getSettings()
    app.secret_key = settings.server.secretKey

    # Settings to assume defaults if not set
    if not checkIfExistsOrIsEmpty('server.host'):
        print("No host set. Using default of 127.0.0.1...")
        settings.server.host = '127.0.0.1'

    if not checkIfExistsOrIsEmpty('server.debug'):
        settings.server.debug = False

    print(Fore.YELLOW + f"Using port: {settings.server.port} and host: {settings.server.host}")
    print("Output now from flask app:")
    app.run(debug=settings.server.debug, port=settings.server.port, host=settings.server.host)

except Exception as e:
    errorHandling.setErrorPreventedStart()
    debugSetting = getattr(settings.server, "debug", True)
    portSetting = getattr(settings.server, "port", 5000)
    hostSetting = getattr(settings.server, "host", '127.0.0.1')
    if not app.secret_key:
        import secrets
        app.secret_key = secrets.token_urlsafe(32)
    print(Fore.RED + f"Error while starting: {e}\nStarting Flask app: http://{hostSetting}:{portSetting} with debug {debugSetting}.")
    app.run(debug=debugSetting, port=portSetting, host=hostSetting)

