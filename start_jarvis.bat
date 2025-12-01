@echo off
title Jarvis AI Assistant
echo.
echo  ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
echo  ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
echo  ██║███████║██████╔╝██║   ██║██║███████╗
echo  ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
echo  ██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║
echo  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
echo.
echo  AI Assistant - Ready to Help!
echo.

:menu
echo Choose an option:
echo 1. Quick Start with Verification
echo 2. Start Jarvis (Single Process)
echo 3. Start Jarvis with Hotword Detection (Multi-Process)
echo 4. Run Complete Tests
echo 5. Setup/Install Dependencies
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto verify
if "%choice%"=="2" goto single
if "%choice%"=="3" goto multi
if "%choice%"=="4" goto test
if "%choice%"=="5" goto setup
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto menu

:verify
echo Starting Jarvis with verification...
python verify_and_start.py
goto menu

:single
echo Starting Jarvis in single process mode...
python main.py
goto menu

:multi
echo Starting Jarvis with hotword detection...
python run.py
goto menu

:test
echo Running complete test suite...
python test_complete.py
pause
goto menu

:setup
echo Running setup...
call setup.bat
pause
goto menu

:exit
echo Goodbye!
exit
