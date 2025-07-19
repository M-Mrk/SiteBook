from app.yamlServices import validateYaml, createExampleEntriesYaml
from app import errorHandling

print("Starting SiteBook...")

# Create example entries.yaml if it does not exist
if createExampleEntriesYaml():
    print("Created example entries.yaml. Please fill it with your entries and/or restart the app.")
    #TODO find a way to restart and restart automatically

# Validate YAML files
error = validateYaml()

# Start flask to either run normally or show the validation error(s)
from app.app import app

if errorHandling.errorExists():
    print(f"Error in YAML file(s): {errorHandling.getErrorsPrintable()}")
else:
    print("YAML file loaded successfully.")
    print("Starting Flask app...  Output now from flask server:")
app.run(debug=True)