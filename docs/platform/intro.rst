.. _intro:

=====
Intro
=====

This is the main (technical) documentation for the Smart Emission Data Platform.
It can always be found at `smartplatform.readthedocs.org <http://smartplatform.readthedocs.org/>`_.
A somewhat lighter introduction can be found in `this series of blogs <https://justobjects.nl/category/smartemission/>`_.

The home page for the Smart Emission project and data platform is http://data.smartemission.nl

The home page for the Smart Emission Nijmegen project is http://smartemission.ruhosting.nl

The project GitHub repository is at https://github.com/smartemission/smartemission.

This is document version |release| generated on |today|.

History
=======

The Smart Emission Platform was initiated and largely developed within
the `Smart Emission Nijmegen project <http://smartemission.ruhosting.nl>`_ (2015-2017, see also below).

The Geonovum/RIVM `SOSPilot Project <http://sensors.geonovum.nl>`_ (2014-2015) , where RIVM LML
(Dutch national Air Quality Data) data was harvested and serviced via the OGC Sensor Observation Service (SOS), was
a precursor for the architecture and approach to ETL with sensor data.

In and after 2017 several other projects, web-clients and sensor-types started utilizing the platform hosted at
`data.smartemission.nl <http://data.smartemission.nl>`_. These include:

* the `Smart City Living Lab <https://slimstestad.nl/programma-2017-2018/>`_: around 7 major cities within NL deployed Intemo sensor stations
* `AirSensEUR <http://www.airsenseur.org/>`_ - a EU JRC initiative for an Open Sensor HW/SW platform

This put more strain on the platform and required a more structural development and
maintenance approach (than project-based funding).

In 2018, the SE Platform was migrated to the Dutch National GDI infrastructure `PDOK <https://pdok.nl>`_ maintained
by the `Dutch Kadaster <https://www.kadaster.nl/>`_.
This gives a tremendous opportunity for long-term evolution and stability of the platform beyond the initial
and project-based fundings. This migration targeted hosting within a `Docker Kubernetes <https://kubernetes.io/>`_ environment.
All code was migrated to a dedicated `Smart Emission GitHub Organization <https://github.com/smartemission>`_ and
hosting of all Docker Images on an `SE DockerHub Organization <https://hub.docker.com/r/smartemission/>`_.

Smart Emission Nijmegen
=======================

The Smart Emission Platform was largely developed during the Smart Emission Nijmegen project
started in 2015 and still continuing.

Read all about the Smart Emission Nijmegen project via: `smartemission.ruhosting.nl/ <http://smartemission.ruhosting.nl>`_.

An introductory presentation:
http://www.ru.nl/publish/pages/774337/smartemission_ru_24juni_lc_v5_smallsize.pdf

In the paper `Filling the feedback gap of place-related externalities in smart cities <http://www.ru.nl/publish/pages/774337/carton_etall_aesop-2015_v11_filling_thefeedback_gap_ofexternalities_insmartcities.pdf>`_
the project is described extensively.

*"...we present the set-up of the pilot experiment in project “Smart Emission”,*
*constructing an experimental citizen-sensor-network in the city of Nijmegen. This project, as part of*
*research program ‘Maps 4 Society,’ is one of the currently running Smart City projects in the*
*Netherlands. A number of social, technical and governmental innovations are put together in this*
*project: (1) innovative sensing method: new, low-cost sensors are being designed and built in the*
*project and tested in practice, using small sensing-modules that measure air quality indicators,*
*amongst others NO2, CO2, ozone, temperature and noise load. (2) big data: the measured data forms*
*a refined data-flow from sensing points at places where people live and work: thus forming a ‘big*
*picture’ to build a real-time, in-depth understanding of the local distribution of urban air quality (3)*
*empowering citizens by making visible the ‘externality’ of urban air quality and feeding this into a*
*bottom-up planning process: the community in the target area get the co-decision-making control over*
*where the sensors are placed, co-interpret the mapped feedback data, discuss and collectively explore*
*possible options for improvement (supported by a Maptable instrument) to get a fair and ‘better’*
*distribution of air pollution in the city, balanced against other spatial qualities. ...."*

The data from the Smart Emission sensors is converted and published as standard web services: OGC WMS(-Time), WFS, SOS
and SensorThings APIs. Some web clients
(SmartApp, Heron) are developed to visualize the data. All this is part of the Smart Emission Data Platform whose technicalities
are the subject of this document.

SE Nijmegen Project Partners
----------------------------

.. figure:: _static/se-partners.jpg
   :align: center

   *Smart Emission Nijmegen Project Partners*

More on: http://smartemission.ruhosting.nl/over-ons/

Documentation Technology
========================

Writing technical documentation using standalone documents like Word can be tedious especially for joint
authoring, publication on the web and integration with code.

Luckily there are various
open (web) technologies available for both document (joint) authoring and publication.

We use a combination of three technologies to automate documentation production, hence to produce this document:

#. `Restructured Text (RST) <http://docutils.sourceforge.net/rst.html>`_ as the document format
#. `GitHub <https://github.com/smartemission/smartemission>`_ to allow joint authoring, versioning and safe storage of the raw (RST) document
#. `ReadTheDocs.org (RTD) <http://ReadTheDocs.org>`_ for document generation (on GH commits) and hosting on the web

This triple makes maintaining actualized documentation comfortable.

This document is written in `Restructured Text (rst) <http://docutils.sourceforge.net/rst.html>`_
generated by `Sphinx <http://sphinx-doc.org/index.html>`_ and hosted by `ReadTheDocs.org (RTD) <http://ReadTheDocs.org>`_.

The sources
of this document are (.rst) text files maintained in the Project's GitHub: https://github.com/smartemission/smartemission/docs/platform

You can also download a `PDF version of this document <https://media.readthedocs.org/pdf/smartplatform/latest/smartplatform.pdf>`_
and even an `Ebook version <https://media.readthedocs.org/epub/smartplatform/latest/smartplatform.epub>`_.

This document is automatically generated whenever a commit is performed on the
above GitHub repository (via a "Post-Commit-Hook")

Using Sphinx with RTD one effectively has a living document like a Wiki
but with the structure and versioning characteristics of a real document or book.

Basically we let "The Cloud" (GitHub and RTD) work for us!
