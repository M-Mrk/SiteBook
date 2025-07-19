from flask import Flask, render_template, redirect
from .yamlServices import loadEntriesYaml, validateEntries
from . import errorHandling

app = Flask(__name__, template_folder="../themes")

@app.route("/")
def home():
    entries = loadEntriesYaml()
    if errorHandling.errorExists():
        return redirect("/error")
    return render_template("main/standard.html", entries=entries)

@app.route("/error")
def errorPage(errors=None):
    if not errors:
        validateEntries()
        errors = errorHandling.getErrors()
    if not errors:
        return redirect("/")
    return render_template("error/standard.html", errors=errors)

# @app.route("/restart") #TODO find way to restart the app
# def restart():