@echo off
echo ============================================================
echo Creating Windows Firewall Rule for Python Backend
echo ============================================================
echo.

REM Add firewall rule to allow Python on port 5000
netsh advfirewall firewall add rule name="Python Backend - Port 5000" dir=in action=allow protocol=TCP localport=5000

echo.
echo ============================================================
echo Firewall rule created!
echo Python is now allowed to accept connections on port 5000
echo ============================================================
echo.
pause

