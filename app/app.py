from flask import Flask, render_template, redirect, flash, request
from .yamlServices import loadEntriesYaml, validateYaml, appendEntry
from . import errorHandling
from .settingHandling import getSettings, checkIfSettingExistsOrIsEmpty
from .services import getEntryOptions, getPictureLink
import os
from functools import wraps
import sys
from threading import Timer
from werkzeug.utils import secure_filename
from flask import redirect, url_for

baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder="../themes", static_folder="../images")

def checkIfStartUpPrevented(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if errorHandling.errorPreventedStart():
            return redirect("/error")

        return f(*args, **kwargs)
    return decorated_function

def getTheme():
    settings = getSettings()
    if not checkIfSettingExistsOrIsEmpty('theme.name'):
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
    
    for entry in entries: # Check if all images actually exist
        if getattr(entry, "picture", None):
            getPictureLink(entry.picture)
    if errorHandling.errorExists():
        return redirect("/error")
    
    return render_template(f"main/{getTheme()}.html", entries=entries, settings=getSettings())

@app.route("/add/picture", methods=["POST"])
def uploadPicture():
    if 'file' not in request.files:
        flash(message="No File uploaded", category="warning")
        return redirect(request.referrer or url_for('index')), 400
    
    file = request.files['file']
    if file.filename == '':
        flash(message="No File uploaded", category="warning")
        return redirect(request.referrer or url_for('index')), 400

    # Security: Use secure_filename to prevent directory traversal
    filename = secure_filename(file.filename)
    
    # Optional: Validate file type
    allowedExtensions = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    if not filename.lower().endswith(tuple(allowedExtensions)): # Check if file has allowed extension
        flash(message="Invalid file type", category="error")
        return redirect(request.referrer or url_for('index')), 400

    imagesDir = os.path.join(baseDir, 'images')
    os.makedirs(imagesDir, exist_ok=True)  # Ensure directory exists
    
    try:
        file.save(os.path.join(imagesDir, filename))
        flash(message="File uploaded successfully", category="success")
        return redirect(request.referrer or url_for('index')), 200
    except Exception as e:
        flash(message="Upload failed", category="error")
        return redirect(request.referrer or url_for('index')), 500

@app.route("/add", methods=["POST"])
def add():
    print(request.form)
    dataDict = {}
    name = None
    for key in request.form:
        if not name and key == "name":
            name = request.form[key]
        else:
            dataDict[key] = request.form[key]

    if not name or name.strip() == "":
        flash("No name provided for new entry. Couldn't create new entry", "warning")
        return redirect("/")
    print("appending")
    appendEntry(entryName=name, entryData=dataDict)
    if errorHandling.errorExists:
        return redirect("/error/f")
    return redirect("/")
    
@app.route("/error")
def errorPage():
    errors = errorHandling.getErrors()
    if errors:
        validateYaml()
    if not errors:
        return redirect("/")
    return render_template(f"error/{getTheme()}.html", errors=errors, startUpPrevented=errorHandling.errorPreventedStart(), settings=getSettings())

@app.route("/error/f") # Optional error route which doesnt re validate before showing errors
def fErrorPage():
    errors = errorHandling.getErrors()
    if not errors:
        return redirect("/")
    return render_template(f"error/{getTheme()}.html", errors=errors, startUpPrevented=errorHandling.errorPreventedStart(), settings=getSettings)

def stopApp():
    import time
    print("Stopping the application...")
    try:
        # Method 1: Send SIGINT signal like Ctrl+C
        import signal
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(1)
        raise Exception("SIGINT did not stop the application as expected.")
    except Exception as exc:
        print(f"Error during SIGINT shutdown: {exc}")
        try:
            # Method 2: Force exit if SIGINT fails
            print("Attempting force exit...")
            os._exit(0)
        except Exception as exc:
            global powerCalled
            powerCalled = False
            print(f"Error during force exit: {exc}")

def restartApp():
    print("Restarting the application...")
    pythonInterpreter = sys.executable
    os.execl(pythonInterpreter, pythonInterpreter, *sys.argv)

powerCalled = False

@app.route("/power", methods=["POST"])
def power():
    global powerCalled
    if powerCalled:
        return redirect('/')
    
    action = request.form.get("action")

    if action == "stop":
        powerCalled = True
        flash("Stopping the application...", category="info")
        Timer(1, stopApp).start()
        return redirect("/")
    elif action == "restart":
        powerCalled = True
        flash("Restarting the application...", category="info")
        Timer(1, restartApp).start()
        return redirect("/")
    else:
        flash("Unknown power action. No action taken.", "warning")
        return redirect("/")

@app.context_processor
def contextProcessorFunction():
    return dict(getEntryOptions=getEntryOptions, getPictureLink=getPictureLink) # Make getEntryOptions available in templates

@app.errorhandler(404)
def unknownPage(*args):
    return redirect("/")