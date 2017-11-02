This dir contains specific options in order to have configs locally, i.e. machine-dependent.

Each config file is named after the host it is running on.
As the config files contain passwords, they are not checked-in into
GitHub by adding them to the .gitignore file.

How to make your own host-dependent config file:

- type hostname on command line and note your machine's hostname, symbolically "myhostname"
- copy the file example.args to myhostname.args
- change the values for your local situation
- add your filename to the .gitignore file

On servers like hosted via Docker the host-dependent files need to be maintained manually.
