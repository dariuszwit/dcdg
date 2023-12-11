@echo off
chcp 65001

:: File name and path of the script to be executed
set "target_file=config.bat"
set "target_path=%~dp0%target_file%"

:: Check if the script is running with administrator privileges
NET FILE 1>NUL 2>NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo Please wait, attempting to run the script with administrator privileges...
    echo Running file: %target_file%
    echo Path: %target_path%
    powershell -Command "Start-Process -FilePath '%target_path%' -Verb RunAs"
    exit
)

:: The rest of your script's code can go here

echo Configuration completed.
pause
