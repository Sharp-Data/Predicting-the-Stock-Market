import pandas as pd
from datetime import datetime

df = pd.read_csv("sphist.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df = df.reset_index(drop=True)


x=0
y=5
last_5_test = df["Close"].iloc[x:y].mean()

Past_5_ave_list = []
Past_5_std_list = []
Past_5_ave_vol_list = []
Past_30_ave_list = []
Past_30_ave_vol_list = []
for index, row in df.iterrows():
    if index < 5:
        Past_5_ave_list.append(0)
        Past_5_std_list.append(0)
        Past_5_ave_vol_list.append(0)
    if index < 30:
        Past_30_ave_list.append(0)
        Past_30_ave_vol_list.append(0)
    if index >= 5:
        i_5 = index - 5
        last_5_ave = df["Close"].iloc[i_5:index].mean()
        last_5_std = last_5_ave = df["Close"].iloc[i_5:index].std()
        last_5_ave_vol = df["Volume"].iloc[i_5:index].mean()
        Past_5_ave_list.append(last_5_ave)
        Past_5_std_list.append(last_5_std)
        Past_5_ave_vol_list.append(last_5_ave_vol)
    if index >= 30:
        i_30 = index - 30
        last_30_ave = df["Close"].iloc[i_30:index].mean()
        Past_30_ave_list.append(last_30_ave)
        last_30_ave_vol = df["Volume"].iloc[i_30:index].mean()
        Past_30_ave_vol_list.append(last_30_ave_vol)
        
df["Past 5 Ave"] = Past_5_ave_list
df["Past 30 Ave"] = Past_30_ave_list
df["Past 5 Std"] = Past_5_std_list
df["Past 5 Ave Volume"] = Past_5_ave_vol_list
df["Past 30 Ave Volume"] = Past_30_ave_list

df = df[df["Date"] > datetime(year=1951, month=1, day=2)]
df = df.dropna()

train = df[df["Date"] < datetime(year=2013, month=1, day=1)]
test = df[df["Date"] >= datetime(year=2013, month=1, day=1)]
                                
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
cols = ["Past 5 Ave", "Past 30 Ave", "Past 5 Std", "Past 5 Ave Volume", "Past 30 Ave Volume"]

lr.fit(train[cols], train["Close"])
predictions = lr.predict(test[cols])

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(test["Close"], predictions)

if __name__ == "__main__":
    print(mae)
