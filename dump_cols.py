import pandas as pd
df = pd.read_excel("equities.xlsx")
with open("cols.txt", "w", encoding='utf-8') as f:
    for c in df.columns:
        f.write(c + "\n")
