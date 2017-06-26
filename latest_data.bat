SET market=C:\Users\felix\OneDrive\Elite Dangerous\EDMarketConnector
FOR /F "delims=" %%I IN ('DIR "%market%\%~1.%~2*" /B /O:-D') DO python . "%market%\%%I" -sd %3 & GOTO STOP1
:STOP1
FOR /F "delims=" %%I IN ('DIR "%market%\%~1.%~2*" /B /O:-D') DO python . "%market%\%%I" -bd %3 & GOTO STOP2
:STOP2
