import pandas as pd

df = pd.read_csv(r"D:/BAITAP_Thu_vien_mo/diem.csv")

print(df.tail())

print(df.info())

df['diem_trung_binh'] = df[['Toan', 'Ly', 'Hoa']].mean(axis=1)

hoc_sinh_gioi_toan = df[df['Toan'] > 8]
print(hoc_sinh_gioi_toan)

if 'gioi_tinh' in df.columns:
    print(df.groupby('gioi_tinh')['diem_trung_binh'].mean())

df.to_excel("ket_qua.xlsx", index=False)
