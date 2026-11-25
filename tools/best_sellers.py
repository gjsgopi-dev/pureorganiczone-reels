#!/usr/bin/env python3
"""Top-selling products on pureorganiczone.com over the last N days, from
insights/sales_snapshots/*.csv (order counts only; no seller data).

Usage: python3 tools/best_sellers.py [days=14] [top=15]
Writes insights/best_sellers.csv (date, window_days, rank, product, vendor,
price, new_orders, all_time_orders, wishlist) and prints the table.
"""
import csv, glob, os, sys, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "insights", "sales_snapshots")
days = int(sys.argv[1]) if len(sys.argv) > 1 else 14
top = int(sys.argv[2]) if len(sys.argv) > 2 else 15

files = sorted(glob.glob(os.path.join(SNAP, "*.csv")))
if not files:
    sys.exit("no snapshots; run tools/site_sales.py first")
latest = files[-1]
ldate = dt.datetime.strptime(os.path.basename(latest)[:15], "%Y-%m-%d_%H%M")
cut = ldate - dt.timedelta(days=days)
base = next((f for f in files
             if dt.datetime.strptime(os.path.basename(f)[:15], "%Y-%m-%d_%H%M") >= cut), files[0])

def load(f):
    return {r["slug"]: r for r in csv.DictReader(open(f))}

A, B = load(base), load(latest)
rows = []
for s, r in B.items():
    now = int(r["orders"] or 0)
    before = int(A[s]["orders"] or 0) if s in A else now  # new listing: unknown start, count 0
    if now - before > 0:
        rows.append((now - before, r))
rows.sort(key=lambda x: (-x[0], -int(x[1]["orders"] or 0)))

out = os.path.join(ROOT, "insights", "best_sellers.csv")
new = not os.path.exists(out)
today = ldate.strftime("%Y-%m-%d")
existing = open(out).read() if not new else ""
with open(out, "a", newline="") as fh:
    w = csv.writer(fh)
    if new:
        w.writerow(["date", "window_days", "rank", "product", "vendor", "price",
                    "new_orders", "all_time_orders", "wishlist"])
    if f"{today},{days},1," not in existing:
        for i, (d, r) in enumerate(rows[:top], 1):
            w.writerow([today, days, i, r["name"], r["vendor"], r["offer_price"],
                        d, r["orders"], r["wishlist"]])
print(f"window {os.path.basename(base)} -> {os.path.basename(latest)}")
for i, (d, r) in enumerate(rows[:top], 1):
    print(f"{i:2}. +{d:<3} {r['name']} | {r['vendor']} | Rs {r['offer_price']}")
