rem set var="D:\MacTools\WorkFile\WorkSpace\pyQuant\stock"
REM cd "D:\MacTools\WorkFile\WorkSpace\pyQuant\stock"
REM E:
D:
cd "D:\MacTools\WorkFile\WorkSpace\pyQuant\stock"
rem cd stock
start cmd /k python singleAnalyseUtil.py
ping -n 20 localhost > nul
REM start python sina_Monitor.py 
REM ping -n 15 localhost > nul
start cmd /k python sina_Monitor-GOLD.py
ping -n 20 localhost > nul
rem start cmd /k python sina_Monitor-Market.py
rem ping -n 20 localhost > nul
start cmd /k python sina_Monitor-Market-New.py
ping -n 20 localhost > nul
start cmd /k python sina_Monitor-Market-LH.py
ping -n 20 localhost > nul
start cmd /k python sina_Market-DurationUp.py
ping -n 20 localhost > nul 
start cmd /k python sina_Market-DurationDn.py
ping -n 20 localhost > nul 
start cmd /k python LinePower.py
rem start python LineHistogram.py
