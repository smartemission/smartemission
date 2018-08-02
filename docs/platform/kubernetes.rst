.. _kubernetes:

==========
Kubernetes
==========

This chapter describes the installation and maintenance for the Smart Emission Data Platform in a Kubernetes environment.
Note that installation and maintenance on regular Docker is described in a separate chapter.

Principles
==========

These are requirements and principles to understand and install an instance of the SE platform.
It is required to have an understanding of `Docker <https://www.docker.com>`_ and Kubernetes (K8s)
as that is the main environment in which the SE Platform is run.

Services
========

InfluxDB
--------

Creation
~~~~~~~~

Create volumes via `PersistentVolumeClaim` (pvc.yml) , one for staorage, one for backup/restore: ::

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