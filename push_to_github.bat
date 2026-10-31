@echo off
cd /d "%~dp0"

echo ========================================================
echo Pushing TravelApp to GitHub repository...
echo Remote: https://github.com/TRIPUROSUNDAROOBEHERA/TravelApp.git
echo ========================================================
echo.

git push -u origin main

echo.
echo ========================================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: TravelApp has been uploaded to GitHub!
    echo Check it at: https://github.com/TRIPUROSUNDAROOBEHERA/TravelApp
) else (
    echo NOTE: If the repository doesn't exist yet, create it first at:
    echo https://github.com/new (Name: TravelApp)
)
echo ========================================================
echo.
pause
