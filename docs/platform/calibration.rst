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

Two steps:

* Filter data
* Use neural network to make prediction