#!/bin/bash

# Install the requirements
pip install -r requirements.txt

# Build the application into an executable
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data="assets/*;assets/" --clean notification.pyw

# Copy the assets folder into the dist directory
cp -r assets/ dist/assets/

# Remove the build directory
rm -rf build/

echo "Installation complete! The application is located in the dist folder."