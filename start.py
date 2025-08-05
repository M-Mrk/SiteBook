from colorama import Fore, init
import waitress

from app.yamlServices import validateYaml, createExampleEntriesYaml, createExampleSettingsYaml
from app import errorHandling
from app.settingHandling import getSettings, checkIfSettingExistsOrIsEmpty, setAndWriteSetting

def restart():
    import sys, os
    print(Fore.YELLOW + "Restarting SiteBook...")
    pythonInterpreter = sys.executable
    os.execl(pythonInterpreter, pythonInterpreter, *sys.argv)

print("Starting SiteBook...")

init(autoreset=True) #colorama init

# Create example entries.yaml if it does not exist
if createExampleEntriesYaml():
    print(Fore.YELLOW + "Created example entries.yaml.")
    restart()

if createExampleSettingsYaml():
    print(Fore.YELLOW + "Created example settings.yaml.")
    restart()

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
    settings = getSettings()

    if not checkIfSettingExistsOrIsEmpty('server.port'):
        print(Fore.YELLOW + "No port set. Setting to 5000...")
        setAndWriteSetting(settingsName='server.port', value=5000)
        settings = getSettings()

    if not checkIfSettingExistsOrIsEmpty('server.secretKey'):
        print(Fore.YELLOW + "No secretKey set. Generating a new one...")
        import secrets
        setAndWriteSetting(settingsName='server.secretKey', value=secrets.token_urlsafe(32))
        settings = getSettings()
    app.secret_key = settings.server.secretKey

    if not checkIfSettingExistsOrIsEmpty('server.host'):
        print("No host set. Setting to 127.0.0.1...")
        setAndWriteSetting(settingsName='server.host', value='127.0.0.1')
        settings = getSettings()

    if not checkIfSettingExistsOrIsEmpty('server.threads'):
        print(Fore.YELLOW + "No amount of threads set. Setting to 4...")
        setAndWriteSetting(settingsName='server.threads', value=4)
        settings = getSettings()

    if not checkIfSettingExistsOrIsEmpty('server.debug'):
        setAndWriteSetting(settingsName='server.debug', value=False)
        settings = getSettings()

    print(Fore.YELLOW + f"Starting on http://{settings.server.host}:{settings.server.port} with debug {settings.server.debug} and threads {settings.server.threads}.")
    print("Output now from flask app:")
    if settings.server.debug:
        app.run(debug=settings.server.debug, port=settings.server.port, host=settings.server.host)
    waitress.serve(app, host=settings.server.host, port=settings.server.port, threads=settings.server.threads)

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

