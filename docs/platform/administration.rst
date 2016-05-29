.. _admin:

==============
Administration
==============

This chapter describes the operation and maintenance aspects for the Smart Emission platform. For example:

* how to start stop servers
* managing the ETL
* where to find logfiles
* troubleshooting

Data Management
===============

TBS

Web Services
============

TBS

Troubleshooting
===============

Various issues found and their solutions.

Docker won't start
------------------

In syslog ``"[graphdriver] prior storage driver \"aufs\" failed: driver not supported" ``.
Solution: https://github.com/docker/docker/issues/14026. Removed ``/var/lib/docker/aufs``.

