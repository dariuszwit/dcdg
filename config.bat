@echo off
chcp 65001 > nul

:: Path to the script directory and script file name
set "script_dir=C:\Scripts"
set "python_script=genscheme.py"

:: Path to the file to be copied
set "source_file=%~dp0%python_script%"

:: Check and install Python dependencies
echo Checking and installing dependencies...
pip show tqdm > nul || pip install tqdm

:: Check Python version
python --version > nul
if %errorlevel% neq 0 (
    echo Python is not installed or not available in PATH.
    echo Please install Python and rerun this script.
    pause
    exit
)

:: Check if the script is run with administrator privileges
net session > nul 2>&1
if %errorlevel% neq 0 (
    echo Administrator privileges are required.
    pause
    exit
)

:: Create a directory for scripts if it doesn't exist
if not exist "%script_dir%" (
    echo Creating directory: %script_dir%
    mkdir "%script_dir%"
)

:: Copy the Python script to the scripts directory
echo Copying file: %source_file% to %script_dir%
xcopy /y "%source_file%" "%script_dir%"

:: Check if script directory is already in PATH
echo Checking if %script_dir% is already in PATH...
for %%i in ("%PATH:;=","%") do (
    if /i "%%~i"=="%script_dir%" (
        set "path_exists=1"
        goto PathCheckEnd
    )
)
set "path_exists=0"

:PathCheckEnd
if %path_exists%==0 (
    echo %script_dir% is not in PATH. Adding to PATH...
    setx PATH "%PATH%;%script_dir%" /M
) else (
    echo %script_dir% is already in PATH. Skipping addition.
)

:: Create a batch file to run the Python script
set "batch_script=%script_dir%\genscheme.bat"
echo Creating batch file: %batch_script%
(
    echo @echo off
    echo python "%script_dir%\%python_script%" %%*
) > "%batch_script%"

echo Configuration complete. The script can now be run as an administrator.
pause
