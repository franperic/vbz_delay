import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

import tensorflow as tf

files = glob.glob("01_data/raw/fahrzeit*")
haltestellen = glob.glob("01_data/raw/halte*")

# Load data
vbz = pd.concat([pd.read_csv(f) for f in files], axis=0)

datum_cols = ["betriebsdatum", "datum_von", "datum_nach"]
vbz[datum_cols] = vbz[datum_cols].apply(pd.to_datetime, format="%d.%m.%y")


stations = pd.read_csv(haltestellen[0])

# Verification
stops = stations.halt_kurz.unique()
vbz_stops = vbz.halt_kurz_von1.unique()
stop_check = [stop for stop in stops if stop in vbz_stops]

# Data prep
halt_info = stations.loc[:, ["halt_kurz", "halt_lang"]]
vbz_rich = vbz.merge(halt_info, how="left", left_on="halt_kurz_von1", right_on="halt_kurz")
vbz_rich = vbz_rich.merge(halt_info, how="left", left_on="halt_kurz_nach1", right_on="halt_kurz")

vbz_rich.drop(["halt_kurz_x", "halt_kurz_y"], axis=1, inplace=True)
vbz_rich.rename(columns={"halt_lang_x": "halt_lang_von",
                         "halt_lang_y": "halt_lang_nach"}, inplace=True)

relevant_vars = ["linie", "richtung", "betriebsdatum", "fahrzeug", "kurs", "fw_lang", "soll_an_nach", "soll_ab_nach"]
vbz_rich.drop_duplicates(subset=relevant_vars, inplace=True)


line13 = vbz_rich.loc[(vbz_rich["linie"] == 13) & 
                      vbz_rich["fw_lang"].isin(["ALBG - FRAN", "FRAN - ALBG"])]



delta = line13["soll_an_von"] - line13["ist_an_von"]
time = line13["ist_an_von"] / (60*60)
plt.scatter(time, delta/60)
plt.show()

line13.sort_values(["fahrzeug", "betriebsdatum", "datum_von", "datum_nach", "soll_an_von"], inplace=True)
line13["delay"] = line13["soll_ab_von"] - line13["ist_ab_von"]

plt.scatter(line13.betriebsdatum, line13.delay/60)
plt.show()


agg_total_daily = line13.groupby("betriebsdatum", as_index=False)["delay"].mean()
plt.plot(agg_total_daily.betriebsdatum, agg_total_daily.delay)
plt.show()

agg_fz_daily = line13.groupby(["fahrzeug", "betriebsdatum"], as_index=False)["delay"].mean()
fzs = line13.fahrzeug.unique()
for i in np.arange(len(fzs)):
    fz = fzs[i]
    illust = agg_fz_daily.loc[agg_fz_daily["fahrzeug"] == fz]
    plt.plot(illust.betriebsdatum,illust.delay)
plt.show()

agg_fz_daily.groupby("fahrzeug", as_index=False).size().sort_values("size")

agg_fz_daily.loc[agg_fz_daily["fahrzeug"] == 2094]
single = line13.loc[line13["fahrzeug"] == 2094].reset_index(drop=True)
plt.plot(single.delay)
plt.show()


# Data Prep
line13.betriebsdatum.describe()
line13.betriebsdatum
line13.betriebsdatum.astype(str) + " " + line13.soll_ab_von.astype(str)  


import datetime
line13.sort_values(["fahrzeug", "betriebsdatum", "datum_von", "datum_nach", "soll_an_von"], inplace=True)
line13["delay"] = line13["soll_ab_von"] - line13["ist_ab_von"]





x = line13.soll_ab_von
time_indicator = pd.to_timedelta(x, unit="S").astype(str).str[6:]

date_time = pd.to_datetime(line13.betriebsdatum.astype(str) + time_indicator, format="%Y-%m-%d %H:%M:%S")
timestamp_s = date_time.map(datetime.datetime.timestamp)

day = 24*60*60
line13["day_sin"] = np.sin(timestamp_s * (2 * np.pi / day))
line13["day_cos"] = np.cos(timestamp_s * (2 * np.pi / day))

# delay
line13["delay_lag1"] = line13.groupby(["fahrzeug", "betriebsdatum"])["delay"].shift(1)
line13["delay_lag2"] = line13.groupby(["fahrzeug", "betriebsdatum"])["delay"].shift(2)
line13["delay_lag3"] = line13.groupby(["fahrzeug", "betriebsdatum"])["delay"].shift(3)

model_col = ["linie", "richtung", "betriebsdatum", "seq_von", "delay_lag1", "delay_lag2", "delay_lag3", "day_sin", "day_cos", "delay"]
model_df = line13.loc[:, model_col]
model_df = pd.get_dummies(model_df, columns=["richtung", "seq_von"])

# Train validation test - split
training = model_df.loc[model_df["betriebsdatum"] < "2020-03-01"]
validation = model_df.loc[(model_df["betriebsdatum"] >= "2020-03-01") &
                          (model_df["betriebsdatum"] <= "2020-03-11")]
test = model_df.loc[model_df["betriebsdatum"] > "2020-03-11"]

training.shape