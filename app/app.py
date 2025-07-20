from flask import Flask, render_template, redirect, flash
from .yamlServices import loadEntriesYaml, validateEntries
from . import errorHandling
from .settingHandling import getSettings, checkIfExistsOrIsEmpty
import os

app = Flask(__name__, template_folder="../themes")

def getTheme():
    settings = getSettings()
    if not checkIfExistsOrIsEmpty('theme'):
        return "standard"
    else:
        paths = [
            os.path.join(app.template_folder, f"base/{settings.theme}.html"),
            os.path.join(app.template_folder, f"main/{settings.theme}.html"),
            os.path.join(app.template_folder, f"error/{settings.theme}.html"),
            os.path.join(app.template_folder, f"settings/{settings.theme}.html")
        ]
        fileNotFound = False
        for path in paths:
            if not os.path.exists(path):
                fileNotFound = path
        if fileNotFound:
            flash(f"At least one Theme file of Theme: '{settings.theme}' not found at: {fileNotFound}. Using default theme instead.", "warning")
            return "standard"

        return settings.theme

@app.route("/")
def home():
    entries = loadEntriesYaml()
    if errorHandling.errorExists():
        return redirect("/error")
    return render_template(f"main/{getTheme()}.html", entries=entries, settings=getSettings())

@app.route("/error")
def errorPage(errors=None):
    if not errors:
        validateEntries()
        errors = errorHandling.getErrors()
    if not errors:
        return redirect("/")
    return render_template(f"error/{getTheme()}.html", errors=errors, settings=getSettings())

# @app.route("/restart") #TODO find way to restart the app
# def restart():