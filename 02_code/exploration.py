import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

files = glob.glob("01_data/raw/*")
vbz = pd.concat([pd.read_csv(f) for f in files], axis=0)

vbz["betriebsdatum"] = pd.to_datetime(vbz["betriebsdatum"], format="%d.%m.%y")

line13 = vbz.loc[(vbz["linie"] == 13) & (vbz["richtung"] == 2)]

line13.fahrzeug.value_counts()
check = line13.loc[(line13["fahrzeug"] == 3002) & (line13["betriebsdatum"] == "2020-03-04")]
single_ride = check.loc[check["fahrt_id"] == 30810]

single_ride.sort_values(by="seq_von", inplace=True)

fig, ax = plt.subplots()
ax.scatter(single_ride["soll_an_von"], single_ride["ist_an_von"])
ax.set_xlabel("Soll")
ax.set_ylabel("Ist")
plt.show()

delta = single_ride["soll_an_von"] - single_ride["ist_an_von"]

fig, ax = plt.subplots()
ax.plot(np.arange(30), delta)
plt.show()


sec_conversion = 60*60
single_ride["soll_an_von"]/sec_conversion
single_ride["soll_ab_von"]/sec_conversion