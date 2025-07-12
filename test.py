import csv
import random
import time
import curl_cffi.requests
import yfinance as yf

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0"
]

symbols = []
with open('data1.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'T' in row and row['T']:
            symbols.append(row['T'])

with open('yf.csv', 'w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out)
    writer.writerow(['T', 'P', 'B', 'A', 'M', 'O', 'C', 'I', 'S'])
    for symbol in symbols:
        info = None
        for retry in range(4):
            ua = random.choice(USER_AGENTS)
            session = curl_cffi.requests.Session()
            session.headers['User-Agent'] = ua
            yf.set_session(session)
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                session.close()
                break
            except:
                session.close()
                if retry < 3:
                    time.sleep(4 + retry * 2 + random.uniform(0, 0.5))
                else:
                    info = None
        row = [symbol]
        fields = ['currentPrice', 'bid', 'ask', 'targetMeanPrice', 'numberOfAnalystOpinions', 'marketCap', 'industry', 'sector']
        for field in fields:
            if info and field in info and info[field] is not None:
                row.append(str(info[field]))
            else:
                row.append('')
        writer.writerow(row)
        time.sleep(2 + random.uniform(0, 0.5))