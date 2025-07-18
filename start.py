from app.yamlServices import validateYaml

print("Starting SiteBook...")

# Validate YAML files
error = validateYaml()

# Start flask to either run normally or show the validation error(s)
from app.app import app, setError

if error:
    print(f"Error in YAML file: {error}")
    # Set the error to the flask app so it can show the error
    setError(error)
else:
    print("YAML file loaded successfully.")
    print("Starting Flask app...  Output now from flask server:")
app.run(debug=True)