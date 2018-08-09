.. _kubernetes:

==========
Kubernetes
==========

This chapter describes the installation and maintenance for the Smart Emission Data Platform in a
`Kubernetes (K8s) <https://kubernetes.io/>`_ environment.
Note that installation and maintenance in a Docker environment is described in
the :ref:`installation` chapter. SE was initially (2016-2018) deployed as Containers on a single "bare Docker" machine.
Later with the use of `docker-compose` and Docker Hub but still "bare Docker". In spring 2018 migration within Kadaster-PDOK
to K8s started, deploying in the K8s environment on Azure.

Principles
==========

These are requirements and principles to understand and install an instance of the SE platform.
It is required to have an understanding of `Docker <https://www.docker.com>`_ a
nd `Kubernetes (K8s) <https://kubernetes.io/>`_
as that is the main environment in which the SE Platform is run.

Most Smart Emission services are deployed as follows in K8s:

* deployment.yml - specifies (`Pods` for) a K8s `Deployment`
* service.yml - describes a K8s `Service` (internal network proxy access) for the `Pods` in the `Deployment`
* ingress.yml - rules how to route outside requests to `Service` (only if the `Service` requires outside access)

Only for InfluxDB instances, as it requires local
storage a `StatefulSet` is deployed i.s.o. a regular `Deployment`.

Postgres/PostGIS is not deployed within K8s but accessed as an external
`Azure Database for PostgreSQL server` service from MS Azure.

Links
=====

Links to the main artefacts related to Kubernetes deployment:

* K8s deployment specs and Readme: https://github.com/smartemission/kubernetes-se
* GitHub repositories for all SE Docker Images: https://github.com/smartemission
* Docker Images repo: https://hub.docker.com/r/smartemission

Namespaces
==========

The main two operational K8s `Namespaces` are:

* `smartemission` - the main SE service stack and ETL
* `collectors` - Data Collector services and Dashboards (see global :ref:`architecture` Chapter)

Additional, supporting, `Namespaces` are:

* `monitoring` - Monitoring related
* `cert-manager` - (Let's Encrypt) SSL certificate management
* `ingress-nginx` - Ingress services based on nginx-proxying (external/public access)
* `kube-system` - mainly K8s Dashboard related


Namespace smartemission
=======================

Below are the main K8s artefacts related under the `smartemission` operational `Namespace`.


InfluxDB
--------

Links
~~~~~

* K8s deployment specs: https://github.com/smartemission/kubernetes-se/tree/master/smartemission/services/influxdb
* GitHub repo/var specs: https://github.com/smartemission/docker-se-influxdb

Creation
~~~~~~~~

Create two volumes via `PersistentVolumeClaim` (pvc.yml) , one for storage, one for backup/restore: ::

	# Run this once to make volumes
	apiVersion: apps/v1beta2
	kind: PersistentVolumeClaim
	metadata:
	  name: influxdb-backup
	spec:
	  accessModes:
	  - ReadWriteOnce
	  storageClassName: default
	  resources:
	    requests:
	      storage: 2Gi

	---

	apiVersion: apps/v1beta2
	kind: PersistentVolumeClaim
	metadata:
	  name: influxdb-storage
	spec:
	  accessModes:
	  - ReadWriteOnce
	  storageClassName: default
	  resources:
	    requests:
	      storage: 5Gi


Use these in `StatefulSet` deployment: ::

	apiVersion: apps/v1beta2
	kind: StatefulSet
	metadata:
	  name: influxdb
	  namespace: smartemission
	spec:
	  selector:
	    matchLabels:
	      app: influxdb
	  serviceName: "influxdb"
	  replicas: 1
	  template:
	    metadata:
	      labels:
	        app: influxdb
	    spec:
	      terminationGracePeriodSeconds: 10
	      containers:
	      - name: influxdb
	        image: influxdb:1.5.3
	        ports:
	        - containerPort: 8086
	        volumeMounts:
	        - mountPath: /var/lib/influxdb
	          name: influxdb-storage
	        - mountPath: /backup
	          name: influxdb-backup
	  volumeClaimTemplates:
	  - metadata:
	      name: influxdb-storage
	    spec:
	      accessModes: [ "ReadWriteOnce" ]
	      storageClassName: default
	      resources:
	        requests:
	          storage: 5Gi
	  - metadata:
	      name: influxdb-backup
	    spec:
	      accessModes: [ "ReadWriteOnce" ]
	      storageClassName: default
	      resources:
	        requests:
	          storage: 2Gi

Backup and Restore
~~~~~~~~~~~~~~~~~~

Restore based on
`this medium.com article <https://medium.com/innocode-stories/restore-influxdb-from-backup-in-kubernetes-c5b71ddbd825>`_

Restoring in these steps:

* copy backup files into `influxdb-backup` volume
* stop/delete  `influxdb` container
* run `job-restore` Job
* re-create influxdb

Here are the commands: ::

	# All backup files are contained in local dir influxdb
    # influxdb/smartemission.autogen.00101.00
    # influxdb/meta.00
    # influxdb/smartemission.autogen.00079.00
    # etc
	kubectl cp influxdb  smartemission/influxdb-0:/backup/
    # NB files will reside remotely under /backup/influxdb/*.00 etc !

	# Delete in Kubernetes the StateFulSet influxdb, YES DELETE!

	# Job must run on specific node
	$ kubectl get nodes
	NAME                       STATUS    ROLES     AGE       VERSION
	aks-agentpool-34284374-0   Ready     agent     35d       v1.10.3
	aks-agentpool-34284374-1   Ready     agent     35d       v1.10.3
	aks-agentpool-34284374-2   Ready     agent     35d       v1.10.3

	$ kubectl -n smartemission get pvc
	NAME                          STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
	influxdb-backup-influxdb-0    Bound     pvc-f127f07a-958d-11e8-beac-0a58ac1f1ed2   2Gi        RWO            default        1h
	influxdb-storage-influxdb-0   Bound     pvc-6c3a3d85-63fb-11e8-8f98-0a58ac1f0043   5Gi        RWO            default        63d

CronJobs
--------

K8s `Cronjobs` are applied for all SE ETL.
CronJobs run jobs on a time-based schedule. These automated jobs run like Cron tasks on a Linux or UNIX system.

Links
~~~~~

* GitHub repository: https://github.com/smartemission/docker-se-stetl
* Docker Image: https://hub.docker.com/r/smartemission/se-stetl
* K8s `CronJobs`: https://github.com/smartemission/kubernetes-se/tree/master/smartemission/cronjobs

Implementation
~~~~~~~~~~~~~~

All ETL is based on `the Stetl ETL framework <http://stetl.org>`_.
A single Docker Image based on the official Stetl Docker Image
contains all ETL processes. A start-up parameter determines the specific ETL process to run.
Design of the ETL is described in the :ref:`data` chapter.


