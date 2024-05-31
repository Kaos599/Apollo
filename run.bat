@echo off

REM Check if pip is installed
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed. Please install pip first.
    exit /b 1
)

REM List of required libraries
set "libraries=faker pandas"

REM Function to check and install libraries
for %%i in (%libraries%) do (
    python -c "import %%i" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing %%i...
        pip install %%i
    ) else (
        echo %%i is already installed.
    )
)

REM Check for random library (part of Python standard library, so no installation needed)
python -c "import random" >nul 2>&1
if %errorlevel% neq 0 (
    echo There is an issue with the Python standard library.
    exit /b 1
) else (
    echo random is already part of the standard library.
)

echo All required libraries are installed.
pause
exit /b 0
