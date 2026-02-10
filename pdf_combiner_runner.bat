@REM Batch combine pdfs in the current folder using the PDF-AI-PREP project
@ECHO OFF

REM Set the path to the PDF-AI-PREP project
SET "PROJECT_PATH=C:\Apps\PDF-Ai-Prep"

REM Get the current folder where this batch file is located
SET "CURRENT_FOLDER=%~dp0"
REM Remove trailing backslash
SET "CURRENT_FOLDER=%CURRENT_FOLDER:~0,-1%"

ECHO ===================================================================
ECHO Combine PDFs ready for AI Runner
ECHO ===================================================================
ECHO Project Path: %PROJECT_PATH%
ECHO Current Folder: %CURRENT_FOLDER%
ECHO ===================================================================
ECHO.

REM Check if uv is available
WHERE uv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: 'uv' is not found in PATH.
    ECHO Please install uv or add it to your PATH.
    PAUSE
    EXIT /B 1
)

REM Check if project path exists
IF NOT EXIST "%PROJECT_PATH%" (
    ECHO ERROR: Project path does not exist: %PROJECT_PATH%
    ECHO Please update the PROJECT_PATH variable at the top of this script.
    PAUSE
    EXIT /B 1
)

REM Check if main.py exists
IF NOT EXIST "%PROJECT_PATH%\main.py" (
    ECHO ERROR: main.py not found in project path: %PROJECT_PATH%
    PAUSE
    EXIT /B 1
)

REM Run the Python script with uv
ECHO Running conversion on folder: %CURRENT_FOLDER%
ECHO.
uv run --project "%PROJECT_PATH%" python "%PROJECT_PATH%\main.py" "%CURRENT_FOLDER%"

ECHO.
ECHO ===================================================================
ECHO Combining complete!
ECHO ===================================================================
PAUSE