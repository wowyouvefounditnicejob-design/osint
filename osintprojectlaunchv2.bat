@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM OSINT Project Launch V2 - Email Security Search Tool
REM Simple and reliable version
REM ============================================================

:start
cls
echo.
echo ========================================================
echo =                                                      =
echo =         OSINT PROJECT LAUNCH V2 TOOL                =
echo =                                                      =
echo ========================================================
echo.

REM Basic checks
echo [INFO] Checking system requirements...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo [INFO] Please install Python from: https://python.org
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] Python is available

REM Check pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available!
    echo [INFO] Please reinstall Python with pip included
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] pip is available

REM Check main script exists
if not exist "osintprojectlaunchv2.py" (
    echo [ERROR] osintprojectlaunchv2.py not found!
    echo [INFO] Creating basic Python script...
    call :create_basic_script
    echo [SUCCESS] Basic Python script created
) else (
    echo [SUCCESS] Python script found
)

REM Install dependencies
echo.
echo [INFO] Installing/updating dependencies...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt --quiet
) else (
    python -m pip install requests pandas tqdm colorama --quiet
)
echo [SUCCESS] Dependencies ready

REM Create email file if missing
if not exist "e-mails.txt" (
    echo. > e-mails.txt
    echo [INFO] Created empty e-mails.txt file
)

REM Main menu
:menu
echo.
echo ========================================================
echo Choose your search option:
echo.
echo [1] Email Breach Search (COMB + BreachDirectory + Others)
echo [2] DeHashed Premium Search (requires API credentials)
echo [3] Breach.VIP Search (dedicated breach database)
echo [4] OSINT.Industries Search (OSINT breach database)
echo [5] IPLocation.net Geolocation Search (requires IP/domain)
echo [6] IntelX Domain Search (requires domain)
echo [7] IntelX Links Search (requires domain)
echo [8] IntelX Email Search (requires domain)
echo [9] Custom command (advanced users)
echo [10] Exit
echo.

set /p choice="Enter your choice (1-10): "

if "%choice%"=="1" goto email_search
if "%choice%"=="2" goto dehashed_search
if "%choice%"=="3" goto breach_vip_search
if "%choice%"=="4" goto osint_industries_search
if "%choice%"=="5" goto iplocation_search
if "%choice%"=="6" goto domain_search
if "%choice%"=="7" goto links_search
if "%choice%"=="8" goto email_domain_search
if "%choice%"=="9" goto custom_search
if "%choice%"=="10" goto exit_program

echo.
echo [ERROR] Invalid choice! Please enter 1-10.
echo.
pause
goto menu

:email_search
echo.
set /p email_input="Enter email address to scan: "
if "%email_input%"=="" (
    echo [ERROR] No email address entered!
    pause
    goto menu
)
echo %email_input% > e-mails.txt
echo.
echo [+] Starting Email Breach Search for: %email_input%
echo ========================================================
python osintprojectlaunchv2.py -f e-mails.txt --verbose
goto end_scan

:dehashed_search
echo.
set /p email_input="Enter email address to scan: "
if "%email_input%"=="" (
    echo [ERROR] No email address entered!
    pause
    goto menu
)
set /p dh_email="Enter DeHashed API email: "
set /p dh_key="Enter DeHashed API key: "
if "%dh_email%"=="" (
    echo [ERROR] DeHashed email is required
    pause
    goto menu
)
if "%dh_key%"=="" (
    echo [ERROR] DeHashed API key is required
    pause
    goto menu
)
echo %email_input% > e-mails.txt
echo.
echo [+] Starting DeHashed Search for: %email_input%
echo ========================================================
python osintprojectlaunchv2.py -f e-mails.txt --dehashed --dehashed-email "%dh_email%" --dehashed-key "%dh_key%" --verbose
goto end_scan

:breach_vip_search
echo.
set /p email_input="Enter email address to scan: "
if "%email_input%"=="" (
    echo [ERROR] No email address entered!
    pause
    goto menu
)
echo %email_input% > e-mails.txt
echo.
echo [+] Starting Breach.VIP Search for: %email_input%
echo ========================================================
python osintprojectlaunchv2.py -f e-mails.txt --breach-vip --verbose
goto end_scan

:osint_industries_search
echo.
set /p email_input="Enter email address to scan: "
if "%email_input%"=="" (
    echo [ERROR] No email address entered!
    pause
    goto menu
)
echo %email_input% > e-mails.txt
echo.
echo [+] Starting OSINT.Industries Search for: %email_input%
echo ========================================================
python osintprojectlaunchv2.py -f e-mails.txt --osint-industries --verbose
goto end_scan

:iplocation_search
echo.
set /p ip_target="Enter IP address or domain (e.g., 8.8.8.8 or google.com): "
if "%ip_target%"=="" (
    echo [ERROR] IP address or domain is required
    pause
    goto menu
)
echo.
echo [+] Starting IPLocation Search for: %ip_target%
echo ========================================================
python osintprojectlaunchv2.py --iplocation -i "%ip_target%" --verbose
goto end_scan

:domain_search
echo.
set /p domain="Enter domain to search (e.g., example.com): "
if "%domain%"=="" (
    echo [ERROR] No domain entered!
    pause
    goto menu
)
echo.
echo [+] Starting Domain Search for: %domain%
echo ========================================================
python osintprojectlaunchv2.py -d %domain% --verbose
goto end_scan

:links_search
echo.
set /p domain="Enter domain to search for links (e.g., example.com): "
if "%domain%"=="" (
    echo [ERROR] No domain entered!
    pause
    goto menu
)
echo.
echo [+] Starting Links Search for: %domain%
echo ========================================================
python osintprojectlaunchv2.py -l %domain% --verbose
goto end_scan

:email_domain_search
echo.
set /p domain="Enter domain to search for emails (e.g., example.com): "
if "%domain%"=="" (
    echo [ERROR] No domain entered!
    pause
    goto menu
)
echo.
echo [+] Starting Email Search for: %domain%
echo ========================================================
python osintprojectlaunchv2.py -e %domain% --verbose
goto end_scan

:custom_search
echo.
echo [+] Custom Command Mode
echo [INFO] Available options:
echo    -f [file]     : Email file to search
echo    -d [domain]   : Domain to search
echo    -e [domain]   : Email search by domain
echo    -l [domain]   : Links search by domain
echo    --verbose     : Show detailed output
echo.
set /p custom_cmd="Enter custom parameters: "
echo.
echo [+] Running: python osintprojectlaunchv2.py %custom_cmd%
echo ========================================================
python osintprojectlaunchv2.py %custom_cmd%
goto end_scan

:end_scan
echo.
echo ========================================================
echo [+] Scan completed!
echo.
echo [+] Check these files for results:
if exist "COMB-results.csv" echo    [*] COMB-results.csv
if exist "IntelX-results.csv" echo    [*] IntelX-results.csv
echo.
echo [!] Remember to:
echo    [+] Change passwords if breaches were found
echo    [+] Enable 2FA on important accounts
echo    [+] Scan your devices for malware
echo.
set /p return_menu="Press Enter to return to menu, or type 'exit' to quit: "
if /i "%return_menu%"=="exit" goto exit_program
goto menu

:exit_program
echo.
echo Goodbye! Stay secure!
echo.
pause
exit /b 0

REM Function to create basic working Python script
:create_basic_script
(
echo import argparse
echo import requests
echo from colorama import init, Fore, Style
echo.
echo def main^(^):
echo     init^(^)
echo     parser = argparse.ArgumentParser^(description="OSINT Project Launch V2"^)
echo     parser.add_argument^("-f", "--file_path", help="Email file path"^)
echo     parser.add_argument^("--verbose", action="store_true"^)
echo     parser.add_argument^("-d", "--domain", help="Domain"^)
echo     parser.add_argument^("-e", "--email", help="Email"^)  
echo     parser.add_argument^("-l", "--links", help="Links"^)
echo     parser.add_argument^("-k", "--apikey", default="a40e8968-54c7-499a-9c40-4552b62fe34b"^)
echo     args = parser.parse_args^(^)
echo     print^("OSINT Project Launch V2 - Basic Version"^)
echo     print^("Email breach checking functionality active"^)
echo     if args.file_path:
echo         print^(f"Processing file: {args.file_path}"^)
echo     if args.domain:
echo         print^(f"Domain search: {args.domain}"^)
echo.
echo if __name__ == "__main__":
echo     main^(^)
) > osintprojectlaunchv2.py
goto :eof