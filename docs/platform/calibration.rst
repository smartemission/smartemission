.. _calibration:

===========
Calibration
===========

* Content
* Offline learning vs online predictions

Data
====

* Jose
* RIVM

Pre-processing
==============

* In R
* Remove measurements with error values
* Interpolation
* Merge Jose and RIVM data
* Save data that is used for calibration

Method
======

* Low-pass filter gas-measurements
* Neural network to predict RIVM values from Jose values

Training model
==============

* Select subset of data points because of redundancy
* Python code for learning model
* Description of learning process, how to get weights for neural network

Performance evaluation
======================

* Cross validation
* RMSE

Parameter optimization
======================

* Meta-parameters optimization
* Try random parameters from distribution

Choosing best model
===================

* complexity vs performance

Online predictions
==================

The sensorconverters.py converter has routines to refine the Jose data. Here the raw Jose measurements for meteo and
gas components are used to predict the hypothetical RIVM measurements of the gas components.

Three steps are taken to convert the raw Jose measurement to hypothetical RIVM measurements.

* The measurements are converted to the units with which the model is learned. For gas components this is kOhm, for
temperature this is Celsius, humidity is in percent and pressure in hPa.
* A roling mean removes extreme measurements. Currently the previous rolling mean has a weight of 0.995 and the new
value a weight of 0.005. Thus alpha is 0.005 in the following code: ::

    def running_mean(previous_val, new_val, alpha):
        if new_val is None:
            return previous_val

        if previous_val is None:
            previous_val = new_val
        val = new_val * alpha + previous_val * (1.0 - alpha)
        return val

* For each gas component a neural network model is used to predict the hypothetical RIVM measurements. Predictions
are only made when all gas components are available. The actual prediction is made with this code: ::

    value_array = np.array([s_barometer, s_humidity, s_temperatureambient, s_temperatureunit, o3_running_means['co'],
     o3_running_means['no2'], o3_running_means['o3']]).reshape(1, -1)
    with open(pipeline_objects['o3'], 'rb') as f:
        # s = f.read()
        o3_pipeline = pickle.load(f)
    val = o3_pipeline.predict(value_array)[0]

