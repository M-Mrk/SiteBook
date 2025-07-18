from flask import Flask, render_template, redirect
from .yamlServices import loadEntriesYaml

from functools import wraps

app = Flask(__name__, template_folder="../themes")

def setError(error):
    app.config['ERROR'] = error

def checkForError(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        error = app.config.get('ERROR')
        if error:
            return redirect("/error")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@checkForError
def home():
    entries = loadEntriesYaml()
    return render_template("main/standard.html", entries=entries)

@app.route("/error")
def errorPage(error=None):
    if not error:
        error = app.config.get('ERROR')
    return render_template("error/standard.html", error=error)

# @app.route("/restart") #TODO find way to restart the app
# def restart():
    
if __name__ == "__main__":
    app.run(debug=True)