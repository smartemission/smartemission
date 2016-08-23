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

A good model has a good performance but is also as simple as possible. Simpler models are less likely to overfit, i.e
 simple models are less likely to fit relations that do not generalize to new data. For this reason, the simplest
 model that performs about as well (e.g. 1 standard deviation) as the best model is selected.

For each gas component this results in models with different learning parameters. Differences are in the size of the
hidden layers, the learning rate, the regularization parameter, the momentum and the activation function. For more
information about these parameters check the documentation of MLPRegressor: http://scikit-learn.org/dev/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor
The parameters for each gas component are listed below: ::

    CO_final = {'mlp__hidden_layer_sizes': [56], 'mlp__learning_rate_init': [0.000052997], 'mlp__alpha': [0.0132466772],
            'mlp__momentum': [0.3377605568], 'mlp__activation': ['relu'], 'mlp__algorithm': ['l-bfgs'],
            'filter__alpha': [0.005]}

    O3_final = {'mlp__hidden_layer_sizes': [42], 'mlp__learning_rate_init': [0.220055322], 'mlp__alpha': [0.2645091504],
                'mlp__momentum': [0.7904790613], 'mlp__activation': ['logistic'], 'mlp__algorithm': ['l-bfgs'],
                'filter__alpha': [0.005]}

    NO2_final = {'mlp__hidden_layer_sizes': [79], 'mlp__learning_rate_init': [0.0045013008], 'mlp__alpha': [0.1382210543],
                 'mlp__momentum': [0.473310471], 'mlp__activation': ['tanh'], 'mlp__algorithm': ['l-bfgs'],
                 'filter__alpha': [0.005]}

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

