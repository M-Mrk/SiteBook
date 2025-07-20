from colorama import Fore, Back, Style, init

from app.yamlServices import validateYaml, createExampleEntriesYaml
from app import errorHandling
from app.settingHandling import getSettings, checkIfExistsOrIsEmpty, setAndWriteSetting

print("Starting SiteBook...")

init(autoreset=True)

# Create example entries.yaml if it does not exist
if createExampleEntriesYaml():
    print(Fore.YELLOW + "Created example entries.yaml. Please fill it with your entries and/or restart the app.")
    #TODO find a way to restart and restart automatically

# Validate YAML files
error = validateYaml()

# Start flask to either run normally or show the validation error(s)
from app.app import app

if errorHandling.errorExists():
    print(Fore.RED + f"Error in YAML file(s): {errorHandling.getErrorsPrintable()}")
else:
    print(Fore.GREEN + "YAML file loaded successfully.")
    
print("Starting Flask app...")

# Initialization of flask app here
if not checkIfExistsOrIsEmpty('secretKey'):
    print(Fore.YELLOW + "No secretKey set. Generating a new one...")
    import secrets
    setAndWriteSetting(settingsName='secretKey', value=secrets.token_urlsafe(32))
settings = getSettings()
app.secret_key = settings.secretKey

print("Output now from flask app:")
app.run(debug=False)