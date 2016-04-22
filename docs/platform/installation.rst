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

Fiware Lab NL
-------------

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

Local - Vagrant
---------------

Docker can be run in various ways. On Linux it can be installed directly (see next). On Mac and Windows
Docker needs to be run within a VM itself. On these
platforms `Docker Toolbox <https://docs.docker.com/engine/installation/mac/>`_ needs to be installed. This
basically installs a small (Linux) VM (with a ``boot2docker`` iso) that runs in VirtualBox.
Within this Linux VM the actual Docker Engine runs. A sort
of `Matroska` construction. Via local commandline tools like ``docker-machine`` and ``docker``, Docker images
can be managed.

However, the above setup creates some hard-to-solve issues when combining Docker images and especially when
trying to use local storage and networking. Also the setup will be different than the actual deployment
on the Fiware platform. For these reasons we will run a local standard Ubuntu VM via VirtualBox. On this VM
we will install Docker, run our Docker images etc. To facilitate working with VirtualBox VMs we will
use `Vagrant <https://www.vagrantup.com/>`_. Via Vagrant it is very easy to setup a "Ubuntu Box" and integrate this
with the local environment. A further plus is that within the Ubuntu Box, the installation steps
will (mostly) be identical to those on the Fiware platform.

Docker with Vagrant
~~~~~~~~~~~~~~~~~~~

The following steps are performed after having `VirtualBox <https://www.virtualbox.org>`_
and `Vagrant <https://www.vagrantup.com/>`_ installed. ::

   # Create a UbuntuBox
   $ vagrant init ubuntu/trusty64
   A `Vagrantfile` has been placed in this directory. You are now
   ready to `vagrant up` your first virtual environment! Please read
   the comments in the Vagrantfile as well as documentation on
   `vagrantup.com` for more information on using Vagrant.

This creates a default ``Vagrantfile`` within the directory of execution, here with some mods for port mapping:  ::

   # -*- mode: ruby -*-
   # vi: set ft=ruby :

   # All Vagrant configuration is done below. The "2" in Vagrant.configure
   # configures the configuration version (we support older styles for
   # backwards compatibility). Please don't change it unless you know what
   # you're doing.
   Vagrant.configure(2) do |config|
     # The most common configuration options are documented and commented below.
     # For a complete reference, please see the online documentation at
     # https://docs.vagrantup.com.

     # Every Vagrant development environment requires a box. You can search for
     # boxes at https://atlas.hashicorp.com/search.
     config.vm.box = "ubuntu/trusty64"

     # Disable automatic box update checking. If you disable this, then
     # boxes will only be checked for updates when the user runs
     # `vagrant box outdated`. This is not recommended.
     # config.vm.box_check_update = false

     # Create a forwarded port mapping which allows access to a specific port
     # within the machine from a port on the host machine. In the example below,
     # accessing "localhost:8081" will access port 80 on the guest machine.
     config.vm.network "forwarded_port", guest: 80, host: 8081

     # Create a private network, which allows host-only access to the machine
     # using a specific IP.
     # config.vm.network "private_network", ip: "192.168.33.10"

     # Create a public network, which generally matched to bridged network.
     # Bridged networks make the machine appear as another physical device on
     # your network.
     # config.vm.network "public_network"

     # Share an additional folder to the guest VM. The first argument is
     # the path on the host to the actual folder. The second argument is
     # the path on the guest to mount the folder. And the optional third
     # argument is a set of non-required options.
     # config.vm.synced_folder "../data", "/vagrant_data"

     # Provider-specific configuration so you can fine-tune various
     # backing providers for Vagrant. These expose provider-specific options.
     # Example for VirtualBox:
     #
     # config.vm.provider "virtualbox" do |vb|
     #   # Display the VirtualBox GUI when booting the machine
     #   vb.gui = true
     #
     #   # Customize the amount of memory on the VM:
     #   vb.memory = "1024"
     # end
     #
     # View the documentation for the provider you are using for more
     # information on available options.

     # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
     # such as FTP and Heroku are also available. See the documentation at
     # https://docs.vagrantup.com/v2/push/atlas.html for more information.
     # config.push.define "atlas" do |push|
     #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
     # end

     # Enable provisioning with a shell script. Additional provisioners such as
     # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
     # documentation for more information about their specific syntax and use.
     # config.vm.provision "shell", inline: <<-SHELL
     #   sudo apt-get update
     #   sudo apt-get install -y apache2
     # SHELL
   end

Later we can modify `Vagrantfile` further, in particular to integrate with the local host (Mac/Windows)
environment, in particular with our directories (e.g. Dockerfiles from GitHub) and local ports (to test
web services). Next, we start up the Ubuntu Box (UB) with ``vagrant up``: ::

   $ vagrant up

   Bringing machine 'default' up with 'virtualbox' provider...
   ==> default: Checking if box 'ubuntu/trusty64' is up to date...
   ==> default: Clearing any previously set forwarded ports...
   ==> default: Clearing any previously set network interfaces...
   ==> default: Preparing network interfaces based on configuration...
       default: Adapter 1: nat
   ==> default: Forwarding ports...
       default: 22 (guest) => 2222 (host) (adapter 1)
   ==> default: Booting VM...
   ==> default: Waiting for machine to boot. This may take a few minutes...
       default: SSH address: 127.0.0.1:2222
       default: SSH username: vagrant
       default: SSH auth method: private key
       default: Warning: Remote connection disconnect. Retrying...
       default: Warning: Remote connection disconnect. Retrying...
   ==> default: Machine booted and ready!

We see that SSH port 22 is mapped to localhost:2222. Login to the box: ::

   ssh -p 2222 vagrant@localhost # password vagrant

   # but easier is to use vagrant
   vagrant ssh

Our local directory is also automatically mounted in the UB so we can have access to our development files (in GitHub): ::

   vagrant@vagrant-ubuntu-trusty-64:~$ ls /vagrant/
   contrib  data  doc  git  Vagrantfile

   # and our Dockerfiles within GitHub
   vagrant@vagrant-ubuntu-trusty-64:~$ ls /vagrant/git/docker
   apache2  boot2docker-fw.sh  postgis  stetl

Within the UB we are on a standard Ubuntu commandline, running a general Ubuntu upgrade first: ::

   $ sudo apt-get update
   $ sudo apt-get -y upgrade

The next steps are standard Docker install (see next section). After the setup is tested by building and running one of
our Docker files. Getting access to our Dockerfiles is easy, for example: ::

   sudo ln -s /vagrant/git ~/git
   cd ~/git/docker/apache2
   sudo docker build -t geonovum/apache2 .

Run and test: ::

   sudo docker run -p 2222:22 -p 80:80 -t -i  geonovum/apache2

Then access Apache from local system via ``localhost:8081``.

.. figure:: _static/installation/docker-vagrant-apache.jpg
   :align: center

   *Access Apache running with Docker externally*

Same for Stetl, build and test: ::

   $ cd ~/git/docker/stetl
   $ sudo docker build -t geonovum/stetl .
   $ cd test/1_copystd
   $ sudo docker run -v `pwd`:`pwd` -w `pwd`  -t -i geonovum/stetl -c etl.cfg

   2016-04-22 19:09:29,705 util INFO Found cStringIO, good!
   2016-04-22 19:09:29,774 util INFO Found lxml.etree, native XML parsing, fabulous!
   2016-04-22 19:09:29,926 util INFO Found GDAL/OGR Python bindings, super!!
   2016-04-22 19:09:29,952 main INFO Stetl version = 1.0.9rc3
   2016-04-22 19:09:29,961 ETL INFO INIT - Stetl version is 1.0.9rc3
   2016-04-22 19:09:29,965 ETL INFO Config/working dir = /home/vagrant/git/docker/stetl/test/1_copystd
   2016-04-22 19:09:29,966 ETL INFO Reading config_file = etl.cfg
   2016-04-22 19:09:29,968 ETL INFO START
   2016-04-22 19:09:29,968 util INFO Timer start: total ETL
   2016-04-22 19:09:29,969 chain INFO Assembling Chain: input_xml_file|output_std...
   2016-04-22 19:09:29,987 input INFO cfg = {'class': 'inputs.fileinput.XmlFileInput', 'file_path': 'input/cities.xml'}
   2016-04-22 19:09:29,993 fileinput INFO file_list=['input/cities.xml']
   2016-04-22 19:09:29,995 output INFO cfg = {'class': 'outputs.standardoutput.StandardXmlOutput'}
   2016-04-22 19:09:29,996 chain INFO Running Chain: input_xml_file|output_std
   2016-04-22 19:09:29,996 fileinput INFO Read/parse for start for file=input/cities.xml....
   2016-04-22 19:09:30,008 fileinput INFO Read/parse ok for file=input/cities.xml
   2016-04-22 19:09:30,014 fileinput INFO all files done
   <?xml version='1.0' encoding='utf-8'?>
   <cities>
       <city>
           <name>Amsterdam</name>
           <lat>52.4</lat>
           <lon>4.9</lon>
       </city>
       <city>
           <name>Bonn</name>
           <lat>50.7</lat>
           <lon>7.1</lon>
       </city>
       <city>
           <name>Rome</name>
           <lat>41.9</lat>
           <lon>12.5</lon>
       </city>
   </cities>

   2016-04-22 19:09:30,024 chain INFO DONE - 1 rounds - chain=input_xml_file|output_std
   2016-04-22 19:09:30,024 util INFO Timer end: total ETL time=0.0 sec
   2016-04-22 19:09:30,026 ETL INFO ALL DONE

Install Docker
--------------

This installation is for both the local Vagrant environment or on Fiware Ubuntu VM.
See https://docs.docker.com/engine/installation/linux/ubuntulinux/.

Steps. ::

   $ sudo apt-get update
   $ sudo apt-get install apt-transport-https ca-certificates  # usually already installed

   # Add key
   sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

   # Add to repo by putting this line in /etc/apt/sources.list.d/docker.list
   deb https://apt.dockerproject.org/repo ubuntu-trusty main

   $ sudo apt-get update

   # check we get from right repo
   $ apt-cache policy docker-engine

   # The linux-image-extra package allows you use the aufs storage driver.
   $ sudo apt-get install linux-image-extra-$(uname -r)

   # If you are installing on Ubuntu 14.04 or 12.04, apparmor is required.
   # You can install it using (usually already installed)
   $ sudo apt-get install apparmor

   # install docker engine
   $ sudo apt-get install docker-engine

   # Start the docker daemon.
   $ sudo service docker start

   # test
   $ sudo docker run hello-world
   $ sudo docker run -it ubuntu bash

   # cleanup non-running images
   $ sudo docker rm -v $(sudo docker ps -a -q -f status=exited)
   $ sudo docker rmi $(sudo docker images -f "dangling=true" -q)

Install Docker-compose, for later combining Docker-images, see https://docs.docker.com/compose/install.
Easiest via Python ``pip``. ::

    $ sudo apt-get install python-pip
    $ sudo pip install docker-compose

See also CLI utils for ``docker-compose``: https://docs.docker.com/v1.5/compose/cli/
Now our system is ready to roll out Docker images.

Docker Images
-------------

PostGIS
~~~~~~~

PostGIS from Kartoza, see https://hub.docker.com/r/kartoza/postgis/ and https://github.com/kartoza/docker-postgis  ::

   $ sudo docker pull kartoza/postgis:9.4-2.1
   $ sudo docker run --name "postgis" -p 5432:5432 -d -t kartoza/postgis:9.4-2.1
   $ sudo apt-get install postgresql-client-9.3
   $ psql -h localhost -U docker  -l
   Password for user docker: (also 'docker')
                                    List of databases
          Name       |  Owner   | Encoding  | Collate | Ctype |   Access privileges
   ------------------+----------+-----------+---------+-------+-----------------------
    gis              | docker   | UTF8      | C       | C     |
    postgres         | postgres | SQL_ASCII | C       | C     |
    template0        | postgres | SQL_ASCII | C       | C     | =c/postgres          +
                     |          |           |         |       | postgres=CTc/postgres
    template1        | postgres | SQL_ASCII | C       | C     | =c/postgres          +
                     |          |           |         |       | postgres=CTc/postgres
    template_postgis | postgres | UTF8      | C       | C     |
   (5 rows)

