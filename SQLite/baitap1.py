import sqlite3

conn = sqlite3.connect("inventory.db")

cursor = conn.cursor()

sql1 = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity INTEGER
)
"""

cursor.execute(sql1)
conn.commit() 

products_data = [
    ("Laptop A100", 999.99, 15),
    ("Mouse Wireless X", 25.50, 50),
    ("Monitor 27-inch", 249.00, 10)
]

sql2 = """
INSERT INTO products (name, price, quantity) 
VALUES
(?, ?, ?)
"""

cursor.executemany(sql2, products_data)
conn.commit() 

sql3 = "SELECT * FROM products"
cursor.execute(sql3)
all_products = cursor.fetchall()


print(f"{'ID':<4} | {'Tên Sản Phẩm':<20} | {'Giá':<10} | {'Số Lượng':<10}")

for p in all_products:
    print(f"{p[0]:<4} | {p[1]:<20} | {p[2]:<10} | {p[3]:<10}")

#update
sql4 = """
UPDATE products
set price = price * 0.9
WHERE quantity < 20 
"""
cursor.execute(sql4)
conn.commit()

#delete
sql5 = "DELETE FROM products WHERE quantity = ?"
cursor.execute(sql5, (2,))  


