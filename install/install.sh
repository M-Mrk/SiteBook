#!/bin/bash

set -e

cd "$(dirname "$0")/../"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
else
  echo "Virtual environment already exists."
fi

source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing required packages..."
pip install -r install/requirements.txt

echo "Done!"
echo "To start SiteBook, run:"
echo "source venv/bin/activate && python3 start.py"
