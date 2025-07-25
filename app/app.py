from flask import Flask, render_template, redirect, flash, request
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
        baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        themesDir = os.path.join(baseDir, "themes")
        
        paths = [
            os.path.join(themesDir, f"base/{settings.theme}.html"),
            os.path.join(themesDir, f"main/{settings.theme}.html"), 
            os.path.join(themesDir, f"error/{settings.theme}.html"),
            os.path.join(themesDir, f"settings/{settings.theme}.html")
        ]
        fileNotFound = False
        falsePaths = []
        for path in paths:
            if not os.path.exists(path):
                fileNotFound = True
                falsePaths.append(path)
        if fileNotFound:
            printPaths = "\n".join(falsePaths)
            flash(f"{len(falsePaths)} Theme file(s) of Theme: '{settings.theme}' not found at: {printPaths}. Using default theme instead.", "warning")
            return "standard"

        return settings.theme

@app.route("/")
def home():
    entries = loadEntriesYaml()
    if errorHandling.errorExists():
        return redirect("/error")
    return render_template(f"main/{getTheme()}.html", entries=entries, settings=getSettings())

# @app.route("/add", methods=["POST"])
# def add():
#     name = request.form.get("name")
#     url = request.form.get("url")
#     description = request.form.get("description")
#     if not name:
#         flash("No name provided for new entry. Couldn't create new entry", "warning")
#         return redirect("/")
    

@app.route("/error")
def errorPage(errors=None):
    if not errors:
        validateEntries()
        errors = errorHandling.getErrors()
    if not errors:
        return redirect("/")
    return render_template(f"error/{getTheme()}.html", errors=errors, settings=getSettings())

# @app.route("/power", methods=["POST"]) #TODO find way to restart the app
# def power():

#TODO: Rework how errors get returned, currently not uniform