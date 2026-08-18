import csv
import io
import json
import urllib.request

SHEET_ID = "1I0bKr_IZd6YKvaEtkunKDaZabW3k9MyPeCnOWAuizPA"
TAB_GID = "987923567"  # ดูเลขหลัง gid= บน URL เมื่อกดแท็บ PRINTER

print("📡 กำลังดึงข้อมูล...")
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={TAB_GID}"
response = urllib.request.urlopen(url)
data = response.read().decode("utf-8-sig")

reader = csv.reader(io.StringIO(data))
header = next(reader)

assets = {}
for row in reader:
    if len(row) < 3:
        continue
    asset_id = row[2].strip().replace("=", "").replace('"', "")
    if not asset_id or asset_id.lower() == "nan":
        continue

    assets[asset_id] = {
        "asset_id": asset_id,  # คอลัมน์ C (Index 2) หมายเลขครุภัณฑ์
        "property_no": row[3]
        if len(row) > 3
        else "",  # คอลัมน์ D (Index 3) หมายเลขสินทรัพย์
        "brand": row[4] if len(row) > 4 else "",  # คอลัมน์ E (Index 4) ตราอักษร
        "model": row[5] if len(row) > 5 else "",  # คอลัมน์ F (Index 5) รุ่น
        "sn_cpu": row[6] if len(row) > 6 else "",  # คอลัมน์ G (Index 6) S/N
        "location": (
            row[10] if len(row) > 10 else ""
        ),  # คอลัมน์ K (Index 10) สถานที่ติดตั้ง
        "status": (
            row[12] if len(row) > 12 else ""
        ),  # คอลัมน์ M (Index 12) สถานะ
        "repair_1": (
            row[13] if len(row) > 13 else ""
        ),  # คอลัมน์ N (Index 13) การซ่อมทำครั้ง1
        "repair_2": (
            row[14] if len(row) > 14 else ""
        ),  # คอลัมน์ O (Index 14) การซ่อมทำครั้ง2
        "repair_3": (
            row[15] if len(row) > 15 else ""
        ),  # คอลัมน์ P (Index 15) การซ่อมทำครั้ง3
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(assets, f, ensure_ascii=False, indent=2)

print(f"✅ สร้าง data.json เสร็จ! ({len(assets)} รายการ)")