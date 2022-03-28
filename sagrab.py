#!/usr/bin/env python3

import os, sys, urllib.request
from datetime import datetime
import pandas as pd
import numpy as np

#baselink = "http://nemlog.com.au/api/co2e/sa1/{0}/{1}/csv -O {2}"
baselink = "http://nemlog.com.au/api/co2e/sa1/{0}/{1}/csv"
start = sys.argv[1]
end = sys.argv[2]
timestamp = datetime.now()
newnames = {"SETTLEMENTDATE": "date", "DIESEL_OIL": "Distillate -  MW", "NATURAL_GAS_PIPELINE": "Gas -  MW",
   "SOLAR": "Solar (Utility) -  MW", "WIND": "Wind -  MW", "BATTERY_DISCHARGE": "Battery (Discharging) -  MW",
   "BATTERY_CHARGE": "Battery (Charging) -  MW", "ROOFTOP_SOLAR": "Solar (Rooftop) -  MW",
   "NETINTERCHANGE_IMPORT": "Imports -  MW", "NETINTERCHANGE_EXPORT": "Exports -  MW"}

#download source data
savedata = "nemlog-{0}.csv".format(timestamp.strftime("%d%b%Y%H%M"))
path = os.getcwd()
fullpath = os.path.join(path, savedata)
#os.system("wget " + baselink.format(start, end, fullpath))
urllib.request.urlretrieve(baselink.format(start, end), fullpath)

#load into python
df = pd.read_csv(fullpath)

#filter out excess columns
df = df.filter(items=newnames.keys())

#covert & save (as 'output.csv')
df.rename(newnames, axis=1, inplace=True)
df = df[["date", "Battery (Charging) -  MW", "Exports -  MW", "Imports -  MW", "Distillate -  MW", "Gas -  MW",
   "Battery (Discharging) -  MW", "Wind -  MW", "Solar (Utility) -  MW", "Solar (Rooftop) -  MW"]]
df[["Temperature - C", "Emissions Intensity - kgCO₂e/MWh", "Price - AUD/MWh"]] = np.nan
df.to_csv("output.csv", index=False)
