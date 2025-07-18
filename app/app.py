from flask import Flask, render_template
from yamlServices import loadEntriesYaml

app = Flask(__name__, template_folder="../themes")

@app.route("/")
def home():
    entries = loadEntriesYaml()
    return render_template("main/standard.html", entries=entries)

@app.route("/error")
def errorPage(error=None):
    return render_template("error/standard.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)