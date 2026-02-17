import pandas as pd

df = pd.read_csv("C:\\Users\\tasne\\Downloads\\titles.csv")
print(df.info())
print(df.isnull().sum())
