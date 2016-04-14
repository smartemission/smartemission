.. _installation:


============
Installation
============

This chapter describes the installation steps for the Smart Emission Data Platform within the
`Fiware Lab NL <http://fiware-lab.nl/>`_ environment.


Background
==========

The `Fiware Lab NL <http://fiware-lab.nl/>`_ provides a cloud-based computing infrastructure in particular
for "Smart City" applications. Based on the adopted "Docker-Strategy" for the
Smart Emission Data Platform as described within the :ref:`architecture` chapter,
this chapter will describe the actual "hands-on" installation steps.

Bootstrap
=========

In order to start installing Docker images and other tooling we need to "bootstrap" the system.

Create VM
---------

Creating a (Ubuntu) VM in the Fiware Lab NL goes as follows.

* login at http://login.fiware-lab.nl/
* create an SSL keypair via http://login.fiware-lab.nl/dashboard/project/access_and_security/
* create a VM-instance via http://login.fiware-lab.nl/dashboard/project/instances/ `Launch Instance` button

.. figure:: _static/installation/launch-instance.jpg
   :align: center

   *Creating a Ubuntu VM instance in Fiware Lab NL*

See the popup image above, do the following selections in the various tabs:

* `Launch Instance` tab: select `boot from image`, select ``base_ubuntu_14.04``
* `Access&Security` tab: select keypair just created and enable all `security groups`
* `Networking` tab: assign both ``floating-IP`` and ``shared-net`` to `selected networks`
* other tabs: leave as is

Install Docker
--------------

See https://docs.docker.com/installation/ubuntulinux. Install via Docker APT repo.

Steps. ::

	# Kernel version OK for Docker
	$ uname -r
	3.13.0-66-generic

	# Add key
	apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

	# Add to repo by putting this line in /etc/apt/sources.list.d/docker.list
	add deb https://apt.dockerproject.org/repo ubuntu-trusty main to

	$ apt-get update
	$ apt-cache policy docker-engine

	# install docker engine
	apt-get update
	apt-get install docker-engine

	# test
	docker run hello-world
	docker run -it ubuntu bash

	# cleanup non-running images
	docker rm -v $(docker ps -a -q -f status=exited)
	docker rmi $(docker images -f "dangling=true" -q)

Docker-compose. https://docs.docker.com/compose/install. Easiest via ``pip``. ::

	$ pip install docker-compose

See also CLI utils for ``docker-compose``: https://docs.docker.com/v1.5/compose/cli/

Docker utils.  ::

	docker ps -a

	# go into docker image named docker_iotacpp_1 to bash prompt
	docker exec -it docker_iotacpp_1 bash


