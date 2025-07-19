from app.yamlServices import validateYaml
from app import errorHandling

print("Starting SiteBook...")

# Validate YAML files
error = validateYaml()

# Start flask to either run normally or show the validation error(s)
from app.app import app

if errorHandling.errorExists():
    print(f"Error in YAML file: {errorHandling.getErrors()}")
else:
    print("YAML file loaded successfully.")
    print("Starting Flask app...  Output now from flask server:")
app.run(debug=True)