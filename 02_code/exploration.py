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



line13 = vbz_rich.loc[(vbz_rich["linie"] == 13)]
check = line13.loc[(line13["fahrzeug"] == 3002) & (line13["betriebsdatum"] == "2020-03-04")]
check.sort_values(by=["fahrt_id", "seq_von"], inplace=True)

# Illustrate
# Parameter
delta = check["soll_an_von"] - check["ist_an_von"]
time = check["ist_an_von"]/(60*60)

# Setup
fig, ax = plt.subplots()
ax.set_ylabel("Delay (Min)")
ax.set_xlabel("Time")

# Plot
ax.plot(time, delta/60, zorder=-1)
ax.scatter(time, delta/60, c=check.fahrt_id, zorder=1, s=7)
ax.axhline(y=0, c="r")

plt.show()


# Sanity check
check.drop(["linie", "richtung", "betriebsdatum", "fahrzeug"], axis=1)
check[["halt_lang_von", "halt_lang_nach"]].values.tolist()