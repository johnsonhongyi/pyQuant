rem set var="E:\Johnson\Quant"
REM cd "E:\Johnson\Quant"
REM E:
cd stock
start python singleAnalyseUtil.py
ping -n 5 localhost > nul
start python sina_Monitor.py 
ping -n 5 localhost > nul
start python sina_Monitor-GOLD.py
ping -n 5 localhost > nul
start python sina_Monitor-Market.py
ping -n 5 localhost > nul
start python sina_Monitor-Market-New.py
ping -n 5 localhost > nul
start python sina_Monitor-Market-LH.py
ping -n 5 localhost > nul
start python LineHistogram.py