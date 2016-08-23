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
* Filtering data
* Select subset because of redundancy
* Save data that is used for calibration

Neural networks
===============

* Neural network to predict RIVM values from Jose values

image of neural network

.. show image of neural network

Training neural network
=======================

A neural network is completely specified by the the weights between the nodes and the activation function of the
nodes. The latter is specified on beforehand and thus only the weights should be learned during the training phase.

There is no way of efficiently finding the optimal weights of an arbitrary neural network. Therefore, a lot of
methods are proposed to iteratively approach the global optimum.

Most of them are based on the idea of back-propagation. With *back-propagation* the error for each of the records in
the data is used to change the weights slightly. The change in weights makes the error for that specific record lower
. However, it might increase the error on other records. Therefore, only a tiny alteration is made for each error in
each record.

As an addition the used `L-BFGS method <https://en.wikipedia.org/wiki/Limited-memory_BFGS>`_ also uses the first and
second derivatives of the error function to converge faster to a solution.

Performance evaluation
======================

To evaluate the performance of the model the
`Root Mean Squared Error <https://en.wikipedia.org/wiki/Root-mean-square_deviation>`_ (RMSE) is used. In other words,
the RMSE is the average error (prediction - actual value) of the model. Lower RMSE are better.

Testing the model on the same data as it is trained on could lead to overfitting. This means that the model learn
relations that are not there in practice. Because the same data is used to asses the performance of the model this
would not be unveiled. For this reason the performance evaluation needs to be done on different data then the
learning of the model. For example, 90% of the data is used to train the model and 10% is used to test the model.
This process can be repeated when using a different 10% to test the data. With the 90%-10% ratio this process can be
repeated 10 times. This is called cross validation. In practice, cross validation with 5 different splits of the data
is used.

Parameter optimization
======================

Training a neural network optimizes the weights between the nodes. However, the training process is also susceptible
to parameters. For example, the number of hidden nodes, the activation function of the hidden nodes, the learning
rate, etc. can be set. For a complete list of all the parameters see the
`documentation of MLPRegressor <http://scikit-learn.org/dev/modules/generated/sklearn.neural_network.MLPRegressor
.html#sklearn.neural_network.MLPRegressor>`_.

Choosing different parameters for the neural network learning influences the performance and complexity of the model.
For example, using to little hidden nodes results in a model that cannot fit the pattern in the data. On the other
side, using to many hidden nodes models a relationship that is to complex and does not generalize to new data.

Parameter optimization is the process of evaluating different parameters.
`RandomizedSearchCV <http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn
.grid_search.GridSearchCV>`_
from sklearn is used to try different parameters and evaluate them using cross-validation. This method trains and
evaluates a neural network n_iter times. The actual code looks like this: ::

     gs = RandomizedSearchCV(gs_pipe, grid, n_iter, measure_rmse, n_jobs=n_jobs, cv=cv_k, verbose=verbose,
                                error_score=np.NaN)
     gs.fit(x, y)

The first argument *gs_pipe* is the pipeline that filters the data and applies a neural network, *grid* is a collection
with distributions of possible parameters, *n_iter* is the number of parameters to try, *measure_rmse* is a function
that computes the RMSE performance and *cv_k* specifies the number of cross-validations to run for each parameter
setting. The other parameters control the process.

.. show image of cross validation

Choosing best model
===================

A good model has a good performance but is also as simple as possible. Simpler models are less likely to overfit, i.e
simple models are less likely to fit relations that do not generalize to new data. For this reason, the simplest
model that performs about as well (e.g. 1 standard deviation) as the best model is selected.

For each gas component this results in models with different learning parameters. Differences are in the size of the
hidden layers, the learning rate, the regularization parameter, the momentum and the activation function. For more
information about these parameters check the
`documentation of MLPRegressor <http://scikit-learn.org/dev/modules/generated/sklearn.neural_network.MLPRegressor
.html#sklearn.neural_network.MLPRegressor>`_.
The parameters for each gas component are listed below: ::

    CO_final = {'mlp__hidden_layer_sizes': [56],
                'mlp__learning_rate_init': [0.000052997],
                'mlp__alpha': [0.0132466772],
                'mlp__momentum': [0.3377605568],
                'mlp__activation': ['relu'],
                'mlp__algorithm': ['l-bfgs'],
                'filter__alpha': [0.005]}

    O3_final = {'mlp__hidden_layer_sizes': [42],
                'mlp__learning_rate_init': [0.220055322],
                'mlp__alpha': [0.2645091504],
                'mlp__momentum': [0.7904790613],
                'mlp__activation': ['logistic'],
                'mlp__algorithm': ['l-bfgs'],
                'filter__alpha': [0.005]}

    NO2_final = {'mlp__hidden_layer_sizes': [79],
                 'mlp__learning_rate_init': [0.0045013008],
                 'mlp__alpha': [0.1382210543],
                 'mlp__momentum': [0.473310471],
                 'mlp__activation': ['tanh'],
                 'mlp__algorithm': ['l-bfgs'],
                 'filter__alpha': [0.005]}

Online predictions
==================

The sensorconverters.py converter has routines to refine the Jose data. Here the raw Jose measurements for meteo and
gas components are used to predict the hypothetical RIVM measurements of the gas components.

Three steps are taken to convert the raw Jose measurement to hypothetical RIVM measurements.

* The measurements are converted to the units with which the model is learned. For gas components this is kOhm, for
  temperature this is Celsius, humidity is in percent and pressure in hPa.

* A roling mean removes extreme measurements. Currently the previous rolling mean has a weight of 0.995 and the ne
  value a weight of 0.005. Thus alpha is 0.005 in the following code: ::

    def running_mean(previous_val, new_val, alpha):
        if new_val is None:
            return previous_val

        if previous_val is None:
            previous_val = new_val
        val = new_val * alpha + previous_val * (1.0 - alpha)
        return val

* For each gas component a neural network model is used to predict the hypothetical RIVM measurements. Prediction
  are only made when all gas components are available. The actual prediction is made with this code: ::

    value_array = np.array([s_barometer, s_humidity, s_temperatureambient, s_temperatureunit, o3_running_means['co'],
                            o3_running_means['no2'], o3_running_means['o3']]).reshape(1, -1)
    with open(pipeline_objects['o3'], 'rb') as f:
        # s = f.read()
        o3_pipeline = pickle.load(f)
    val = o3_pipeline.predict(value_array)[0]

