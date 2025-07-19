from flask import Flask, render_template, redirect
from .yamlServices import loadEntriesYaml
from . import errorHandling

from functools import wraps

app = Flask(__name__, template_folder="../themes")

def checkForError(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if errorHandling.errorExists():
            return redirect("/error")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@checkForError
def home():
    entries = loadEntriesYaml()
    checkForError(f=None)
    return render_template("main/standard.html", entries=entries)

@app.route("/error")
def errorPage(errors=None):
    if not errors:
        errors = errorHandling.getErrors()
    return render_template("error/standard.html", errors=errors)

# @app.route("/restart") #TODO find way to restart the app
# def restart():
    
if __name__ == "__main__":
    app.run(debug=True)