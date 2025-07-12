File: test.py

import csv
import random
import time
import curl_cffi.requests as requests
import yfinance as yf

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/115.0.1901.203",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5897.77 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_8) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
]

def fetch_info(symbol):
    session = requests.Session()
    retries = 4
    delay_base = 2.0
n    for attempt in range(retries):
        session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        try:
            ticker = yf.Ticker(symbol, session=session)
            info = ticker.info
            return info
        except Exception:
            wait = delay_base * (attempt + 1) + random.random() * 0.5
            time.sleep(wait)
    return {}

with open('data1.csv', newline='') as csvfile, open('yf.csv', 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(csvfile)
    fieldnames = ['T', 'P', 'B', 'A', 'M', 'O', 'C', 'I', 'S']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        symbol = row['T'].strip()
        info = fetch_info(symbol)
        out = {
            'T': symbol,
            'P': info.get('currentPrice', '') or '',
            'B': info.get('bid', '') or '',
            'A': info.get('ask', '') or '',
            'M': info.get('targetMeanPrice', '') or '',
            'O': info.get('numberOfAnalystOpinions', '') or '',
            'C': info.get('marketCap', '') or '',
            'I': info.get('industry', '') or '',
            'S': info.get('sector', '') or ''
        }
        writer.writerow(out)
        time.sleep(2 + random.random() * 0.5)


---

File: requirements.txt

yfinance
curl_cffi


---

File: .github/workflows/main.yml

name: fetch-yf-data
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run fetch script
        run: python test.py
      - name: Upload yf.csv
        uses: actions/upload-artifact@v4
        with:
          name: yf-data
          path: yf.csv

