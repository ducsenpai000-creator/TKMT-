import sqlite3
    
db = r"C:/GIT/selenium/SQLite/longchau_db.sqlite"
conn = sqlite3.connect(db)
cursor = conn.cursor()

# Kiểm tra trùng lặp theo product_url hoặc product_name
print("1) Kiểm tra trùng lặp (URL hoặc Name):")

cursor.execute("""
SELECT product_url, product_name, COUNT(*)
FROM sanpham
GROUP BY product_url, product_name
HAVING COUNT(*) > 1
""")
dupes = cursor.fetchall()

if dupes:
    for d in dupes:
        print(" -", d)
else:
    print("Không có trùng lặp.",dupes)

# Kiểm tra dữ liệu thiếu giá bán
cursor.execute("""
SELECT COUNT(*)
FROM sanpham
WHERE price IS NULL 
   OR price = '' 
   OR price = '0'
   OR price = 'Không có giá'
""")
missing = cursor.fetchone()[0]

print("Số sản phẩm thiếu giá:", missing)

# Giá bán > Giá gốc
cursor.execute("""
SELECT product_name, price, original_price
FROM sanpham
WHERE 
    price != '' AND original_price != '' AND
    CAST(REPLACE(price, '.', '') AS INTEGER) >
    CAST(REPLACE(original_price, '.', '') AS INTEGER)
""")
wrong_prices = cursor.fetchall()

if wrong_prices:
    for p in wrong_prices:
        print(" -", p)
else:
    print("Không có bất thường.",wrong_prices)

# Liệt kê tất cả unit duy nhất
cursor.execute("SELECT DISTINCT unit FROM sanpham")
units = cursor.fetchall()
for u in units:
    print(" -", u[0])


# Tổng số bản ghi
cursor.execute("SELECT COUNT(*) FROM sanpham")
total = cursor.fetchone()[0]
print("Tổng số sản phẩm:", total)

conn.close()
