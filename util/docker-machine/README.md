# Utility scripts for use with `docker-machine`

## 1. Script `swarm.sh`

This is a script which can be used to create a 2 node Docker Swarm cluster.
The script creates the nodes, initialises the swarm and sets environment
variables in the terminal it is run from on the host so that the Docker
daemon in the manager node VM is exposed to the host terminal. The
environment variables are set by starting a new shell session in the terminal
from which the commands are run. To return to the Docker environment of the
host use the `exit` command.

To create the VMs and set up the Docker Swarm cluster:

```bash
./swarm.sh start
```

To set up environment variables in the current terminal needed to expose
the Docker daemon of the Swarm manager VM to the host terminal.  

```bash
./swarm.sh connect
```

To remove all VMs created by this script

```bash
./swarm.sh rm
```


