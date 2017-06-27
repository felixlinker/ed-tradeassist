SET market=C:\Users\felix\OneDrive\Elite Dangerous\EDMarketConnector
FOR /F "delims=" %%I IN ('DIR "%market%\%~1.%~2*" /B /O:-D') DO python . "%market%\%%I" -sd %3 -bd %3 -e & GOTO STOP
:STOP
