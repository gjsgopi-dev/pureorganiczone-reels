#!/usr/bin/env python3
"""Snapshot product sales signals from pureorganiczone.com.

Usage:
  python3 tools/site_sales.py            # fetch homepage, write a snapshot, print top movers
  python3 tools/site_sales.py --top 40   # also print the 40 best sellers overall

Reads ONLY public product fields (name, slug, brand/vendor name, price, discount,
order_details_count, wish_list_count, reviews, subscription flag). The page also
embeds seller account data; this script never reads, prints or stores it.

Writes insights/sales_snapshots/<YYYY-MM-DD_HHMM>.csv (IST) and prints the change
in order counts per product since the previous snapshot. order_details_count is a
running total of order lines on the site, so its change between two snapshots is
the number of new orders for that product in between.
"""
import csv, datetime, glob, html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "insights", "sales_snapshots")
FIELDS = ["id", "name", "slug", "vendor", "offer_price", "mrp", "orders", "wishlist", "reviews", "rating", "subscription"]


def fetch():
    r = subprocess.run(["curl", "-sSL", "-m", "120", "https://pureorganiczone.com/"], capture_output=True)
    if r.returncode != 0 or len(r.stdout) < 100000:
        raise SystemExit(f"could not fetch the homepage (curl exit {r.returncode}, {len(r.stdout)} bytes)")
    return r.stdout.decode("utf-8", "ignore")


def parse(page):
    s = html.unescape(page)
    dec = json.JSONDecoder()
    out = {}
    for m in re.finditer(r'\{"id":\d+,"added_by"', s):
        try:
            o, _ = dec.raw_decode(s, m.start())
        except Exception:
            continue
        if "unit_price" not in o:
            continue
        b = o.get("brand") if isinstance(o.get("brand"), dict) else {}
        price, d = o["unit_price"], o.get("discount") or 0
        offer = price - d if o.get("discount_type") == "flat" else round(price * (1 - d / 100), 2)
        out[o["id"]] = {
            "id": o["id"], "name": o["name"], "slug": o["slug"],
            "vendor": (b.get("name") or "").strip() or ("Pure Organic Zone" if o.get("added_by") == "admin" else ""),
            "offer_price": offer, "mrp": price,
            "orders": o.get("order_details_count") or 0, "wishlist": o.get("wish_list_count") or 0,
            "reviews": o.get("reviews_count") or 0, "rating": o.get("reviews_avg_rating") or "",
            "subscription": 1 if o.get("is_subscription") else 0,
        }
    if not out:
        raise SystemExit("no products found in the page; the site layout may have changed")
    return out


def main():
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 0
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    prods = parse(fetch())
    os.makedirs(OUT, exist_ok=True)
    prev_files = sorted(glob.glob(os.path.join(OUT, "*.csv")))
    path = os.path.join(OUT, now.strftime("%Y-%m-%d_%H%M") + ".csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for p in sorted(prods.values(), key=lambda p: -p["orders"]):
            w.writerow(p)
    print(f"snapshot {os.path.relpath(path, ROOT)}: {len(prods)} products, {sum(p['orders'] for p in prods.values())} order lines in total")
    if prev_files:
        prev = {int(r["id"]): r for r in csv.DictReader(open(prev_files[-1]))}
        moves = []
        for pid, p in prods.items():
            if pid in prev:
                dlt = p["orders"] - int(prev[pid]["orders"])
                if dlt:
                    moves.append((dlt, p))
        print(f"new orders since {os.path.basename(prev_files[-1])[:-4]}: {sum(m[0] for m in moves)}")
        for dlt, p in sorted(moves, key=lambda m: -m[0])[:20]:
            print(f"  +{dlt:<4} {p['name'][:60]} | {p['vendor']} | /product/{p['slug']}")
    if top:
        print("best sellers overall:")
        for p in sorted(prods.values(), key=lambda p: -p["orders"])[:top]:
            print(f"  {p['orders']:>5} {p['name'][:60]} | {p['vendor']} | ₹{p['offer_price']} | /product/{p['slug']}")


if __name__ == "__main__":
    main()
