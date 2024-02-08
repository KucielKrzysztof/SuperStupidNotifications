@echo off

REM Install the requirements
pip install -r requirements.txt

REM Build the application into an executable
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data="assets/*;assets/" --clean notification.pyw

REM Copy the assets folder into the dist directory
xcopy /I /E assets dist\assets

REM Remove the build directory
rd /s /q build

echo Installation complete! The application is located in the dist folder.
pause