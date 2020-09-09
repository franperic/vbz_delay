import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

files = glob.glob("01_data/raw/fahrzeit*")
haltestellen = glob.glob("01_data/raw/halte*")

# Load data
vbz = pd.concat([pd.read_csv(f) for f in files], axis=0)
vbz["betriebsdatum"] = pd.to_datetime(vbz["betriebsdatum"], format="%d.%m.%y")

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
check = line13.loc[(line13["betriebsdatum"] == "2020-03-04")]
check.sort_values(by=["fahrzeug", "fahrt_id", "seq_von"], inplace=True)

# Illustrate
# Parameter
delta = check["soll_an_von"] - check["ist_an_von"]
time = check["ist_an_von"]/(60*60)
fz = check.fahrzeug.unique()

# Setup
fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
for i in np.arange(1):
    fahrzeug = fz[3]
    # Data prep
    illust = check.loc[check["fahrzeug"] == fahrzeug]
    illust.sort_values(by=["fahrt_id", "seq_von"], inplace=True)
    delta = illust["soll_an_von"] - illust["ist_an_von"]
    time = illust["ist_an_von"]/(60*60)
    
    # Axis
    # ax.set_ylabel("Delay (Min)")
    # ax.set_xlabel("Time")

    # Plot
    ax.plot(time, delta/60)
    ax.axhline(y=0, c="r")

plt.show()

illust.sort_values("ist_an_von", inplace=True)
plt.plot(time, delta/60, zorder=-1)
plt.scatter(time, delta/60, c=illust["fahrt_id"], zorder=1)
plt.show()

illust.loc[illust["ist_an_von"] < 19800]
illust["ist_an_von"] / (60*60)


# Sanity check
check.drop(["linie", "richtung", "betriebsdatum", "fahrzeug"], axis=1)
check[["seq_von", "seq_nach", "fw_lang", "halt_lang_von", "halt_lang_nach"]].values[0:60]
check[["halt_lang_von", "halt_lang_nach"]].values.tolist()

check["fw_lang"].unique()

illust.loc[illust["fahrt_id"].isin([30155, 30944])]
illust[["betriebsdatum", "datum_von", "datum_nach"]]





delta = line13["soll_an_von"] - line13["ist_an_von"]
time = line13["ist_an_von"] / (60*60)
plt.scatter(time, delta/60)
plt.show()



single_route = line13.loc[(line13["fahrt_id"] == 30176) & (line13["betriebsdatum"] == "2020-02-11") & (line13["fahrzeug"] == 1674)]
single_route.drop(["linie", "richtung", "betriebsdatum", "fahrzeug", "kurs"], axis=1)
single_route.reset_index(inplace=True)

hours = 60*60
plt.plot(np.sin(single_route.ist_an_von * (2 * np.pi / hours)))
plt.show()


line13.fahrzeug.value_counts()
single_vehicle = line13.loc[line13["fahrzeug"] == 3002]
single_vehicle.sort_values(["betriebsdatum", "datum_von", "soll_an_von"], inplace=True)

days = 60*60*24

single_vehicle["day_sin"] = np.sin(single_vehicle.ist_an_von * (2 * np.pi / days))
single_vehicle["day_cos"] = np.cos(single_vehicle.ist_an_von * (2 * np.pi / days))

action_days = single_vehicle.betriebsdatum.unique()
for i in np.arange(len(action_days)):
    illust = single_vehicle.loc[single_vehicle["betriebsdatum"] == action_days[i]].reset_index()
    plt.plot(illust["day_sin"])
    plt.plot(illust["day_cos"])
    
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
splitting_date = "2020-03-01"

line13.betriebsdatum
line13.betriebsdatum.astype(str) + " " + line13.soll_ab_von.astype(str)  


import datetime
line13.sort_values(["fahrzeug", "betriebsdatum", "datum_von", "datum_nach", "soll_an_von"], inplace=True)
line13["delay"] = line13["soll_ab_von"] - line13["ist_ab_von"]





x = line13.soll_ab_von
time_indicator = pd.to_timedelta(x, unit="S").astype(str).str[6:]

date_time = pd.to_datetime(line13.betriebsdatum.astype(str) + time_indicator, format="%Y-%m-%d %H:%M:%S")
timestamp_s = date_time.map(datetime.datetime.timestamp)

