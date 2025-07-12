import csv
import random
import time
from itertools import cycle
import pandas as pd
import yfinance as yf
from curl_cffi.requests import RequestsSession

guids = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 '
    '(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
    '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) '
    'Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:78.0) '
    'Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
]
session = RequestsSession()
agent_cycle = cycle(guids)
symbols = pd.read_csv('data1.csv', usecols=['T'])['T'].dropna().tolist()
with open('yf.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['T', 'P', 'B', 'A', 'M', 'O', 'C', 'I', 'S'])
    for symbol in symbols:
        for attempt in range(4):
            session.headers.update({'User-Agent': next(agent_cycle)})
            try:
                ticker = yf.Ticker(symbol, session=session)
                info = ticker.get_info()
                values = [
                    symbol,
                    info.get('currentPrice') or '',
                    info.get('bid') or '',
                    info.get('ask') or '',
                    info.get('targetMeanPrice') or '',
                    info.get('numberOfAnalystOpinions') or '',
                    info.get('marketCap') or '',
                    info.get('industry') or '',
                    info.get('sector') or ''
                ]
                writer.writerow(values)
                break
            except Exception:
                if attempt < 3:
                    delay = random.uniform(2*(attempt+2), 2*(attempt+2)+0.5)
                    time.sleep(delay)
                else:
                    writer.writerow([symbol] + ['']*8)
                    break
        time.sleep(random.uniform(2, 2.5))