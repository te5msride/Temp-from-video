# import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# plot time vs temperature of output, eliminate nan
df = pd.read_csv("output.csv")
df = df.dropna()
df["Time"] = df["Time"].astype(int)
df["Temperature"] = df["Temperature"].astype(float)
sns.lineplot(x="Time", y="Temperature", data=df)
plt.show()

# smooth and plot, delete outliers
df["Temperature"] = df["Temperature"].rolling(5).mean()
df = df.dropna()
sns.lineplot(x="Time", y="Temperature", data=df)
plt.show()

# plot histogram
sns.histplot(df["Temperature"], bins=20)
plt.show()

# plot boxplot
sns.boxplot(x=df["Temperature"])
plt.show()
