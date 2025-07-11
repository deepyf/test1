import csv
import time
import random
from curl_cffi import Session
import yfinance as yf

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (X11; Linux x86_64)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)...",
    "Mozilla/5.0 (Android 10; Mobile; rv:79.0)...",
    "Mozilla/5.0 (Windows NT 6.1; WOW64)...",
    "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_6_8)...",
    "Mozilla/5.0 (Linux; Android 9; SM-G960U)...",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0)...",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3)..."
]

def get_session():
    s = Session()
    s.headers.update({"User-Agent": random.choice(USER_AGENTS)})
    return s

def fetch(symbol):
    delays = [(2,2.5),(4,4.5),(6,6.5),(8,8.5)]
    for low,high in delays:
        try:
            session = get_session()
            ticker = yf.Ticker(symbol, session=session)
            info = ticker.info
            return {
                "T": symbol,
                "P": info.get("currentPrice") or "",
                "B": info.get("bid") or "",
                "A": info.get("ask") or "",
                "M": info.get("targetMeanPrice") or "",
                "O": info.get("numberOfAnalystOpinions") or "",
                "C": info.get("marketCap") or "",
                "I": info.get("industry") or "",
                "S": info.get("sector") or ""
            }
        except Exception:
            time.sleep(random.uniform(low, high))
    return {"T": symbol, "P": "", "B": "", "A": "", "M": "", "O": "", "C": "", "I": "", "S": ""}

def main():
    with open("data.csv", newline="", encoding="utf-8") as inf, \
         open("yf.csv", "w", newline="", encoding="utf-8") as outf:
        reader = csv.DictReader(inf)
        fieldnames = ["T","P","B","A","M","O","C","I","S"]
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            rec = fetch(row["T"])
            writer.writerow(rec)
            time.sleep(random.uniform(2,2.5))

if __name__ == "__main__":
    main()