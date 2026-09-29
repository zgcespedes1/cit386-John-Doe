import csv
import re
from collections import Counter, defaultdict

SRC = r"C:\Users\Sophia\Downloads\orders (1).csv"
REJECTED_OUT = r"C:\Users\Sophia\Desktop\rejected.csv"
SUMMARY_OUT = r"C:\Users\Sophia\Desktop\summary.txt"

EXPECTED_FIELDS = ["order_id", "customer", "item", "qty", "price"]

def clean_price(raw):
    """Return float or None if unparseable."""
    if raw is None:
        return None
    s = raw.strip()
    if s == "":
        return None
    s = s.replace("$", "").replace(",", "")
    try:
        val = float(s)
    except ValueError:
        return None
    return val

def clean_qty(raw):
    """Return int or None if unparseable."""
    if raw is None:
        return None
    s = raw.strip()
    if s == "":
        return None
    try:
        val = int(s)
    except ValueError:
        return None
    return val

valid_rows = []
rejected_rows = []  # (line_no, raw_row_joined, reason)

with open(SRC, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # line 1
    line_no = 1

    for row in reader:
        line_no += 1

        # Blank / whitespace-only line
        if len(row) == 0 or all(cell.strip() == "" for cell in row):
            rejected_rows.append((line_no, "", "blank row"))
            continue

        raw_joined = ",".join(row)

        # Wrong number of fields
        if len(row) < 5:
            rejected_rows.append((line_no, raw_joined, f"missing field(s): expected 5 columns, got {len(row)}"))
            continue
        if len(row) > 5:
            rejected_rows.append((line_no, raw_joined, f"unexpected extra column(s): expected 5 columns, got {len(row)}"))
            continue

        order_id, customer, item, qty_raw, price_raw = row

        reasons = []

        # order_id check
        order_id_s = order_id.strip()
        if order_id_s == "":
            reasons.append("missing order_id")

        # customer check
        customer_s = customer.strip()
        if customer_s == "":
            reasons.append("missing customer name")

        # item check
        item_s = item.strip()
        if item_s == "":
            reasons.append("missing item")

        # qty check
        qty = clean_qty(qty_raw)
        if qty is None:
            reasons.append(f"non-numeric quantity ('{qty_raw.strip()}')")
        elif qty < 0:
            reasons.append(f"negative quantity ({qty})")
        elif qty == 0:
            reasons.append("zero quantity")

        # price check
        price = clean_price(price_raw)
        if price is None:
            reasons.append(f"non-numeric/missing price ('{price_raw.strip()}')")
        elif price < 0:
            reasons.append(f"negative price ({price})")

        if reasons:
            rejected_rows.append((line_no, raw_joined, "; ".join(reasons)))
            continue

        valid_rows.append({
            "line_no": line_no,
            "order_id": order_id_s,
            "customer": customer_s,
            "item": item_s,
            "qty": qty,
            "price": price,
            "total": qty * price,
        })

# ---- Build summary stats ----
total_revenue = sum(r["total"] for r in valid_rows)
num_valid = len(valid_rows)
num_rejected = len(rejected_rows)
num_total_data_lines = (line_no - 1)  # lines after header

item_counts = Counter()
item_revenue = defaultdict(float)
customer_revenue = defaultdict(float)
for r in valid_rows:
    item_counts[r["item"]] += r["qty"]
    item_revenue[r["item"]] += r["total"]
    customer_revenue[r["customer"]] += r["total"]

top_items_by_revenue = sorted(item_revenue.items(), key=lambda x: x[1], reverse=True)[:5]
top_customers = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)[5-5:5] if False else sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)[:5]

# reason category counts (first reason keyword bucket) for a quick breakdown
reason_buckets = Counter()
for _, _, reason in rejected_rows:
    first = reason.split(";")[0].strip()
    # bucket by leading phrase before any parenthetical/quoted detail
    bucket = re.split(r"[\(']", first)[0].strip()
    reason_buckets[bucket] += 1

avg_order_value = (total_revenue / num_valid) if num_valid else 0

# ---- Write rejected.csv ----
with open(REJECTED_OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["line_number", "raw_row", "reason"])
    for line_no_r, raw, reason in rejected_rows:
        writer.writerow([line_no_r, raw, reason])

# ---- Write summary.txt ----
lines = []
lines.append("ORDERS DATA QUALITY REPORT")
lines.append("=" * 40)
lines.append("")
lines.append(f"Source file rows processed (excluding header): {num_total_data_lines}")
lines.append(f"Valid orders:                                  {num_valid}")
lines.append(f"Rejected rows:                                 {num_rejected}")
lines.append("")
lines.append(f"Total revenue (valid orders only): ${total_revenue:,.2f}")
lines.append(f"Average order value:                ${avg_order_value:,.2f}")
lines.append("")
lines.append("-" * 40)
lines.append("Top 5 items by revenue")
lines.append("-" * 40)
for item, rev in top_items_by_revenue:
    lines.append(f"  {item:<12} ${rev:,.2f}  ({item_counts[item]} units)")
lines.append("")
lines.append("-" * 40)
lines.append("Top 5 customers by spend")
lines.append("-" * 40)
for cust, rev in top_customers:
    lines.append(f"  {cust:<20} ${rev:,.2f}")
lines.append("")
lines.append("-" * 40)
lines.append("Rejected row breakdown (by primary reason)")
lines.append("-" * 40)
for bucket, count in sorted(reason_buckets.items(), key=lambda x: x[1], reverse=True):
    lines.append(f"  {count:>3}  {bucket}")
lines.append("")
lines.append(f"See rejected.csv for the full list of {num_rejected} rejected rows with line numbers and reasons.")

with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
print()
print(f"valid={num_valid} rejected={num_rejected} total_lines={num_total_data_lines}")
