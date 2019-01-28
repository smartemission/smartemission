# ETL - Calibration analysis

Sources and plots for some of the analysis related to SE and AirSensEUR Calibration.

* josene - plots for ANN Calibration of Intemo Jose sensors
* airsenseur - regression plots for calibrated and reference data for AirSensEUR

[airsenseurplots.py](airsenseurplots.py) draws various plots from data stored in InfluxDB.
Both calibrated and RIVM reference data are stored there. For each gas both R-squared ('R2') and the slope ('m') is
depicted. The Python `scipi.stats.linregress(x, y)` function is used.

Two periods and locations are taken:

* sept 9 to okt 9 2018 at RIVM Breukelen Snelweg (A2 highway) site where all 5 AirSensEURs were placed
* dec 25 2018 to january 24 2019 at RIVM Nijmegen Ruyterstraat where ASE_NL_01 was placed

Especially for ASE_NL_01 the calibration can be extra evaluated as this station was present at two RIVM
locations. The result is shown in a [combined plots for ASE_NL_01](airsenseur/asenl01-se-pycal-plots.png).
Upper row is in Breukelen, lower in Nijmegen (only Nijmegen has RIVM CO via SOS)


![Combined plots for ASE_NL_01](airsenseur/asenl01-se-pycal-plots-grafana.png?raw=true "Combined plots for ASE_NL_01")

For all ASEs, especially NO2 prediction is quite good: all slopes ('m') near 1 and R2 all above 0.9 (except ASE_NL_02).


![Combined plots for ASE_NL_All NO2](airsenseur/breuk-sw-no2-ASE_NL_All-2018-09-10-2018-10-09.png?raw=true "Combined plots for ASE_NL_01")
 
