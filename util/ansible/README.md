http://docs.ansible.com/ansible/playbooks_best_practices.html

### Creating and managing VMs with Vagrant
A `vagrantfile` is provided to provision one or more
ubuntu 16.04 VirtualBox VM's using Vagrant. This is a ruby
script which iterates over the `HOSTS` array defined
at the top of the script to create one or more VMs and configure
a host only network between the VMs.

In order to create the VMs using `Vagrant` after
modifying the `HOSTS` list in the `vagrantfile`
as required, use the command:

```bash
vagrant up
```

SSH into the VM's created by Vagrant using the command:

```bash
ssh ubuntu@192.168.101.101 -i keys/private
```

or where the IP address is substituted.


#### Additional useful Vagrant commands

Destroy the VMs created by vagrant.
```bash
vagrant destroy -f
```

### Provisioning the VMs with Ansible

#### Ansible inventory (`hosts`) file
This file should reflect the nodes in the cluster of VMs


#### Running playbooks

**TODO**: variables file!!

A number of playbooks are provided which can be used to set up
the software stack used by SIP. They are run
using the following command:

```bash
ansible-playbook -i hosts playbook.yml
```

For example:
```bash
ansible-playbook -i hosts sip.yml
```
will download and install SIP on the system.


#### Useful ansible commands

```bash
ansible -i simple all -m shell -a "docker ps"
```

```bash
ansible -i simple all -m shell -a "docker version | grep Version"
```
