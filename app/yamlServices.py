import yaml

import os

def loadEntriesYaml():
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entriesPath = os.path.join(baseDir, "entries.yaml")
    with open(entriesPath, "r") as file:
        try:
            entries = yaml.safe_load(file)
            return entries
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")
            return None