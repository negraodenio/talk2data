import pandas as pd
df = pd.read_excel("equities.xlsx")
print(df.iloc[0].to_dict())


