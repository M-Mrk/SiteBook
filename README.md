# SiteBook

# What is it?
SiteBook is a webApp you self host in which you can list websites/services.

## So why should I use it?
If you have alot of self hosted applications or webSites you access frequently and can not or dont want to remember all of their IPs/URLs use SiteBook, so you only have to remember 1!

## Features
- Yaml configuration, for both the entries and the settings, which can be edited via the built in editor.
- Strict Yaml validation
- You can also add Entries via the UI.
- Clear error description to what happend, if something happend.
- Robust (Hopefully) Error Handling, most errors especially non critical ones do not require a restard just a refresh!
- Theme System, this allows other users (or you) to create your own html view too tweak SiteBook to your liking.

## Dependencies
- Flask
- pyYAML
- pydantic
- waitress

# Installation
- Download the latest release zip and unzip it where you want SiteBook to stay and **start your cmd/powershell there**.
- Install dependencies and start SiteBook:
    - Linux:
        1. Run the install script in the install folder `bash install/install.sh`
        2. Activate the venv `source venv/bin/activate`
        3. Done! Now run start.py to start SiteBook `python3 start.py`

    - Windows:
        *Install Script coming soon*
        1. Create and activate a venv. `python -m venv venv` and `.\venv\activate.ps1`
        2. Install the dependencies `pip install -r .\install\requirements.txt`
        3. Done! Now run start.py to start SiteBook `py start.py`
            
# Theme Guide
*Maybe Tailwind support coming soon*

### Structure
- We will need 4 html files.
- 1 per folder in themes/ (base, edit, error, main)
- The files will all need to be named like this: "*YourThemeName*.html"
- Finally set ```` yaml
theme:
  name: *YourThemeName*
```

### How it works
- Note that most of this can be ignored if you just tweak the standard theme and you can probably still get what you want
- SiteBook uses Jinja2 to get data, which allows us to use python logic in our html files.
