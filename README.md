# SiteBook
<img width="1868" height="998" alt="Banner" src="https://github.com/user-attachments/assets/2da758ac-ff44-4835-b12d-920b82af44be" />


# What is it?
SiteBook is a webApp you self host in which you can list websites/services, so that you dont have to remember them yourself.
<img height="248.5" alt="image" src="https://github.com/user-attachments/assets/c2cdbe08-d806-41ba-bcf3-3877345c52a7" />
<img height="248.5" alt="image" src="https://github.com/user-attachments/assets/3290d44a-be17-4623-aa7e-390c1ffd9eb8" />
<img height="248.5" height="994" alt="image" src="https://github.com/user-attachments/assets/c5870417-f52e-4084-b660-a02c3035c519" />


## So why should I use it?
If you have alot of self hosted applications or webSites you access frequently and can not or dont want to remember all of their IPs/URLs use SiteBook (and you can add descriptions for other related stuff which you cant remember), so you only have to remember 1!

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
- 1 per folder in themes/ (base, edit, error, main):
``` text
.
└── SiteBook
    ├── themes
        └── base
        │   └── ThemeName.html
        └── edit
        │   └── ThemeName.html
        └── error
        │   └── ThemeName.html
        └── main
            └── ThemeName.html
```
- The files will all need to be named like this: "*YourThemeName*.html"
- Finally set:
``` yaml
theme:
  name: *YourThemeName*
```

### How it works
- Note that most of this can be ignored if you just tweak the standard theme and you can probably still get what you want
- SiteBook uses Jinja2 to get data, which allows us to use python logic in our html files.
