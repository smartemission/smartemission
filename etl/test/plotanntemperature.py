"""
 Naam:         plotanntemperature.py
 Omschrijving: plot invloed van temperature op voorspelling
 Auteurs:      Pieter Marsman
"""
import pickle
from os import path

import numpy as np
from matplotlib import pyplot as plt

FIG_FOLDER = "../../docs/platform/_static/calibration"
PIPE_FOLDER = "../calibration/model"

with open(path.join(PIPE_FOLDER, "pipeline_co.pkl"), 'rb') as f:
            co_pipeline = pickle.load(f)
with open(path.join(PIPE_FOLDER, "pipeline_no2.pkl"), 'rb') as f:
            no2_pipeline = pickle.load(f)
with open(path.join(PIPE_FOLDER, "pipeline_o3.pkl"), 'rb') as f:
            o3_pipeline = pickle.load(f)

# RIVM    O3_Waarden  NO2_Waarden     CO_Waarden
#           44.328      17.969          181.942
# Jose
# baro  humidity temperature.ambient temperature.unit s.co2 no2resistance o3resistance
nrow = 100
inputs = np.repeat([[1005.490, 80.928, 12.125, 26.187, 1133.000,  641.550, 33.408]], nrow, 0)
temperatures = np.linspace(-50, 100, nrow)
inputs[:,3] = temperatures

pred_co = co_pipeline.predict(inputs)
pred_no2 = no2_pipeline.predict(inputs)
pred_o3 = o3_pipeline.predict(inputs)

plt.plot(temperatures, pred_co, label="CO")
plt.plot(temperatures, pred_no2, label="NO2")
plt.plot(temperatures, pred_o3, label="O3")
plt.xlabel("Temperature (celcius)")
plt.ylabel("Gas component (ug/m3)")
plt.legend()
plt.savefig(path.join(FIG_FOLDER, "temperature_ambient_prediction.png"))


nrow = 100
inputs = np.repeat([[1005.490, 80.928, 12.125, 26.187, 1133.000,  641.550, 33.408]], nrow, 0)
temperatures = np.linspace(-50, 100, nrow)
inputs[:,4] = temperatures

pred_co = co_pipeline.predict(inputs)
pred_no2 = no2_pipeline.predict(inputs)
pred_o3 = o3_pipeline.predict(inputs)

plt.cla()
plt.plot(temperatures, pred_co, label="CO")
plt.plot(temperatures, pred_no2, label="NO2")
plt.plot(temperatures, pred_o3, label="O3")
plt.xlabel("Temperature (celcius)")
plt.ylabel("Gas component (ug/m3)")
plt.legend()
plt.savefig(path.join(FIG_FOLDER, "temperature_unit_prediction.png"))
