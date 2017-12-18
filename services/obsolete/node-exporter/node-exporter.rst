OBSOLETE: using node-exporter as Docker image.

Node Exporter can be installed on the host to gather Linux/Ubuntu metrics.

Steps to install in `/usr/bin/node_exporter`: ::

	mkdir -p /var/smartem/prometheus/archive
	cd /var/smartem/prometheus/archive
	wget https://github.com/prometheus/node_exporter/releases/download/v0.15.2/node_exporter-0.15.2.linux-amd64.tar.gz
	cd /var/smartem/prometheus
	tar -xvzf archive/node_exporter-0.15.2.linux-amd64.tar.gz
	ln -s /var/smartem/prometheus/node_exporter-0.15.2.linux-amd64/node_exporter /usr/bin

Run as service via `/etc/init/node_exporter.conf` and listen on IP-address `docker0` (so metrics not exposed to world): ::

    # Run node_exporter  - place in /etc/init/node_exporter.conf

    start on startup

    script
      /usr/bin/node_exporter --web.listen-address="`ip route show | grep docker0 | awk '{print \$9}'`:9100"
    end script

Start/stop etc ::

	service node_exporter start
	service node_exporter status

Challenge is to access Node Exporter on host from within Prometheus Docker container.
See http://phillbarber.blogspot.nl/2015/02/connect-docker-to-service-on-parent-host.html
In `run.sh` for Apache2:  ::

    PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`
    $ docker run -d --restart=always --add-host=parent-host:${PARENT_HOST} .... etc

Extend Apache2 config:  ::

	<Location /prom-node-metrics>
		ProxyPass http://parent-host:9100/metrics
		ProxyPassReverse http://parent-host:9100/metrics
	</Location>

Add node config in `prometheus.yml`: ::

	- job_name: 'node'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: '/prom-node-metrics'
    scheme: http
    static_configs:
      - targets: ['test.smartemission.nl', 'data.smartemission.nl']

In Grafana import Dashboard `1860`: https://grafana.com/dashboards/1860 to view Node Exporter stats.
