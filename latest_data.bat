SET market=C:\Users\felix\OneDrive\Elite Dangerous\EDMarketConnector
FOR /F "delims=" %%I IN ('DIR "%market%\%~1.%~2*" /B /O:-D') DO python . "%market%\%%I" %~3 -f %4 -t %5 & GOTO STOP
:STOP
