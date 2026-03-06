import pandas as pd

df = pd.read_csv("data/Reviews.csv")

print(f"Data size: {df.shape}")
print(f"\ncolumns: {df.columns.tolist()}")

print(f"\nFirst 5 rows:")
print(df.head())

print(f"\nScore:")
print(df["Score"].value_counts().sort_index())

print(f"\nEmpty values:")
print(df.isnull().sum())

df["Date"] = pd.to_datetime(df["Time"], unit="s")
print(f"Date range: from {df['Date'].min()} to {df['Date'].max()}")
print(f"\nSample review:")
print(df["Text"].iloc[0])