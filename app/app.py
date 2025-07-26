from flask import Flask, render_template, redirect, flash, request
from .yamlServices import loadEntriesYaml, validateYaml
from . import errorHandling
from .settingHandling import getSettings, checkIfExistsOrIsEmpty
import os
from functools import wraps

app = Flask(__name__, template_folder="../themes")

def checkIfStartUpPrevented(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if errorHandling.errorPreventedStart():
            return redirect("/error")

        return f(*args, **kwargs)
    return decorated_function

def getTheme():
    settings = getSettings()
    if not checkIfExistsOrIsEmpty('theme.name'):
        return "standard"
    else:
        baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        themesDir = os.path.join(baseDir, "themes")

        themeBaseDir = os.path.join(themesDir, 'base')
        themeMainDir = os.path.join(themesDir, 'main')
        themeErrorDir = os.path.join(themesDir, 'error')
        themeSettingsDir = os.path.join(themesDir, 'settings')
        
        paths = [
            os.path.join(themeBaseDir, f"{settings.theme.name}.html"),
            os.path.join(themeMainDir, f"{settings.theme.name}.html"), 
            os.path.join(themeErrorDir, f"{settings.theme.name}.html"),
            os.path.join(themeSettingsDir, f"{settings.theme.name}.html")
        ]
        fileNotFound = False
        falsePaths = []
        for path in paths:
            if not os.path.exists(path):
                fileNotFound = True
                falsePaths.append(path)
        if fileNotFound:
            printPaths = "\n".join(falsePaths)
            flash(f"{len(falsePaths)} Theme file(s) of Theme: '{settings.theme.name}' not found at: {printPaths}. Using default theme instead.", "warning")
            return "standard"

        return settings.theme.name

@app.route("/")
@checkIfStartUpPrevented
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
def errorPage():
    errors = errorHandling.getErrors()
    if errors:
        validateYaml()
    if not errors:
        return redirect("/")
    return render_template(f"error/{getTheme()}.html", errors=errors, startUpPrevented=errorHandling.errorPreventedStart(), settings=getSettings())

# @app.route("/power", methods=["POST"]) #TODO find way to restart the app
# def power():

#TODO: Rework how errors get returned, currently not uniform