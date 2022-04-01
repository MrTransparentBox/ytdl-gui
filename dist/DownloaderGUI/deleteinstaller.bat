@echo off
echo %1
For %%A in ("%1") do (
    Set folder=%%~dpA
    Set name=%%~nxA
)
set /A count=0
:loop
set /A count+=1
echo %count%
ren %1 %name%
if %count% == 10 (
    goto fail
)
if errorlevel 1 (
    timeout /T 1 /nobreak > nul
    goto loop
)
echo "deleting..."
del %1
exit
:fail
echo "Max retries exceeded..."