# cAdvisor

See https://github.com/google/cadvisor

> cAdvisor (Container Advisor) provides container users an understanding of the resource usage and performance characteristics of their 
> running containers. It is a running daemon that collects, aggregates, processes, and exports information about running containers. 
> Specifically, for each container it keeps resource isolation parameters, 
> historical resource usage, histograms of complete historical resource usage and network statistics. 
> This data is exported by container and machine-wide.

## Docker Build Local

Need custom build because of issue:
https://github.com/google/cadvisor/issues/1802
Once that is resolved we can use official Docker Image.
