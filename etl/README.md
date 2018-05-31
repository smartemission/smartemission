# ETL - Extract, Transform, Load for sensor data

Sources for ETL of the Smart Emission Platform. Originally this ETL was developed
for the Smart Emission Project Nijmegen and the Intemo Josene Sensor Device (2015-2017). 
As to accommodate other sensor devices like the [EU JRC AirSensEUR](http://www.airsenseur.org), the ETL-framework
has been generalized (2018). 

Uses host-specific variables for databases, passwords etc (not stored in GitHub).

All ETL is developed using [Stetl](http://stetl.org). Stetl is a Python framework and programming model for any ETL
process. The essence of Stetl is that each ETL process is a chain of linked Input, Filters and Output Python classes
specified in a Stetl Config File. 

The `.sh` files each invoke a Stetl ETL process via Docker.

Additional Python files implement specific ETL modules not defined
in the Stetl Framework and are available under the 
Python [smartem](https://github.com/smartemission/docker-se-stetl/tree/master/smartem) package.
The Stetl config files for each ETL process are 
defined [here](https://github.com/smartemission/docker-se-stetl/tree/master/config).

All ETL is now migrated to the new SE GitHub repo: https://github.com/smartemission/docker-se-stetl

The scripts in this dir mainly call the Docker Image [smartemission/se-stetl from DockerHub](https://hub.docker.com/r/smartemission/se-stetl/)
with the particular ETL Process as argument.
