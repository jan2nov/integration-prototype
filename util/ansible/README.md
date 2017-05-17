

### Creating and managing VMs with Vagrant
A `vagrantfile` is provided to provision one or more ubuntu 16.04
VirtualBox VM's using Vagrant. This is a ruby script which iterates over
the `HOSTS` array defined at the top of the script to create one or more
VMs and configure a host only network between the VMs.

In order to create the VMs using `Vagrant` use the command:

```bash
vagrant up
```

SSH into the VM's created by Vagrant using the command:

```bash
ssh ubuntu@<ip> -i keys/sip
```

where the <ip> address is that of the VM one wishes to connect to. This
is defined in the Vagrantfile and by default will be 192.168.111.[101-1xx]
for sip-[01-xx].

Note that is is possible that you will have to remove existing keys associated
with the host IP from your ~/.ssh/known_hosts file for this to work. This can
be done with the commands

```bash
ssh-keygen -f ~/.ssh/known_hosts -R <ip>
```

where `<ip>` is the address of the host you want to remove.


#### Additional useful Vagrant commands

Destroy the VMs created by vagrant.
```bash
vagrant destroy -f
```

### Provisioning the VMs with Ansible

Ansible allows provisioning of systems using a `playbook` YAML file. In order
to provision a basic SIP configuration on the SIP test VM's created using
Vagrant use the following command:

```bash
ansible-playbook -i default_hosts default.yml
```
