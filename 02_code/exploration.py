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

halt_info = stations.loc[:, ["halt_kurz", "halt_lang"]]
vbz_rich = vbz.merge(halt_info, how="left", left_on="halt_kurz_von1", right_on="halt_kurz")
vbz_rich = vbz_rich.merge(halt_info, how="left", left_on="halt_kurz_nach1", right_on="halt_kurz")

vbz_rich.drop(["halt_kurz_x", "halt_kurz_y"], axis=1, inplace=True)
vbz_rich.rename(columns={"halt_lang_x": "halt_lang_von",
                         "halt_lang_y": "halt_lang_nach"}, inplace=True)



line13 = vbz_rich.loc[(vbz_rich["linie"] == 13)]

sorted(line13.halt_kurz_von1.value_counts().index)

line13.fahrzeug.value_counts()
check = line13.loc[(line13["fahrzeug"] == 3002) & (line13["betriebsdatum"] == "2020-03-04")]
check.sort_values(by=["fahrt_id", "seq_von"], inplace=True)

delta = check["soll_an_von"] - check["ist_an_von"]
fig, ax = plt.subplots()
ax.plot(np.arange(599), delta/60)
ax.scatter(np.arange(599), delta/60, c=check.fahrt_id)
ax.axhline(y=0, c="r")
plt.show()


check[["soll_an_von", "ist_an_von"]] / sec_conversion
check

single_ride = check.loc[check["fahrt_id"] == 30810]

single_ride.sort_values(by="seq_von", inplace=True)

fig, ax = plt.subplots()
ax.scatter(single_ride["soll_an_von"], single_ride["ist_an_von"])
ax.set_xlabel("Soll")
ax.set_ylabel("Ist")
plt.show()

single_ride[["soll_an_von", "ist_an_von"]]
delta = single_ride["soll_an_von"] - single_ride["ist_an_von"]

fig, ax = plt.subplots()
ax.plot(np.arange(30), delta)
ax.axhline(y=0, c="r")
ax.set_ylabel("Soll - Ist")
plt.show()


sec_conversion = 60*60
single_ride["soll_an_von"]/sec_conversion
single_ride["ist_an_von"]/sec_conversion
single_ride["soll_ab_von"]/sec_conversion
single_ride["ist_ab_von"]/sec_conversion