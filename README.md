### main
-- fetcher.py

### nb directory
-- has some interactive notebooks you can play with

### how to run?
1. go to https://www.nseindia.com/reports-indices-historical-vix,
2. make a request to get VIX data,
3. find the request in network panel in your browser's devtools
4. copy cookie header
5. paste cookie header in the code
6. run the script `python3 fetcher.py`

Note: you need to replace cookie header for both Nifty data API and VIX data API
