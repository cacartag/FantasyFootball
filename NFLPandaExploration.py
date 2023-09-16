import pandas as pd

filePath = "Players/arizona-cardinals.csv"

df = pd.read_csv(filePath, encoding = "utf-8")

print(df.describe)
