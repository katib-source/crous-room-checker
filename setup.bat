@echo off
echo ===============================================
echo CROUS Room Checker - Setup Script
echo ===============================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating configuration file...
if not exist config.json (
    copy config_sample.json config.json
    echo Configuration file created as config.json
    echo Please edit config.json with your Telegram credentials before running the script.
) else (
    echo Configuration file already exists.
)

echo.
echo ===============================================
echo Setup completed!
echo ===============================================
echo.
echo Next steps:
echo 1. Edit config.json with your Telegram bot token and chat ID
echo 2. Run: python crous-checker.py
echo.
echo For detailed instructions, see README.md
echo.
pause
