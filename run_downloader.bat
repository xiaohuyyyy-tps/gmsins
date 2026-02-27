@echo off
echo Starting Instagram Story Downloader...
echo.

echo 1. Installing dependencies (if needed)...
call install_dependencies.bat

echo.
echo 2. Running story downloader...
python auto_story_downloader.py

echo.
echo Done! Check the 'pics' folder for downloaded stories.
pause
