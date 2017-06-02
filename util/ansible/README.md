## SIP Ansible playbooks

This folder contains a number of [Ansible](https://www.ansible.com/)
playbooks for provisioning SIP. These scripts aim to provide a standard way of
setting up the software enviroment required to run the SIP code.  

This folder also contains a [Vagrant](https://www.vagrantup.com/)
configuration file which can be used to create a number of VMs in
[VirtualBox](https://www.virtualbox.org/) which can be used to run SIP.


### 1. Requirements
- VirtualBox >= 5.1
- Vagrant >= 1.9.4
- Ansible >= 2.3
- Ansible galaxy roles:
    - angstwad.docker_ubuntu
    - GROG.reboot

### 2. Creating and managing VMs with Vagrant
The `Vagrantfile` provided in this folder will create one or more Ubuntu 16.04
VMs. This script iterates over the `HOSTS` array defined near the top of the
to create one or more VMs and configure a network in which the VMs can
communicate. VMs are created with an SSH key pair which is created in they
`keys` folder.  

In order to create the VMs using `Vagrant` use the command:

```bash
vagrant up
```

Once the VMs have been started it is possible to SSH into them using the
command:

```bash
ssh ubuntu@<ip> -i keys/sip
```

where `<ip>` is the address of the VM. This is defined in the `Vagrantfile`
`HOSTS` description. The current value of this IP address is `192.169.111.101`
for host `sip-default`.

***Note*** *It may be necessary to remove existing hosts from
your ~/.ssh/known_hosts file before being able to SSH into the VMs. This
can be done with a text editor or with the command:*

```bash
ssh-keygen -f ~/.ssh/known_hosts -R <ip>
```

where `<ip>` is the address of the host you want to remove.


#### 2.1 Additional useful Vagrant commands

A list of commands that can be used to manipulate VMs managed by Vagrant can
be found at [https://www.vagrantup.com/docs/cli/](). Of note:

To completely delete all SIP VMs created by Vagrant:
```bash
vagrant destroy -f
```

To suspend the SIP VMs:
```bash
vagrant suspend
```

To resume the suspend VMs:
```bash
vagrant resume
```

To shut down the SIP VMs:
```bash
vagrant halt
```

### 3. Provisioning the VMs with Ansible

The Ansible playbooks provided here provide basic provisioning scripts
for setting up the SIP code. These playbook depend on two roles that can be
obtained from Ansible galaxy with the following commands:

```bash
ansible-galaxy install angstwad.docker_ubuntu
ansible-galaxy install GROG.reboot
```

Once these roles have been installed, the following command will set up the
default SIP configuration on the hosts specified in the `default_hosts`
inventory file.

Note roles can be installed locally using the option `-p ROLES_PATH` or `--roles-path=ROLES_PATH`. For example to install the roles into the local
roles directory used in the SIP `utils/ansible` folder use the following
command:

```bash
ansible-galaxy install -p roles angstwad.docker_ubuntu
ansible-galaxy install -p roles GROG.reboot
```



```bash
ansible-playbook -i default_hosts --private-key=keys/sip default.yml
```

### 4. Known issues

- The docker_swarm.yml playbook can fail when starting to install SIP as
  immediately before this step the playbook attempts to reboot the nodes
  and may not wait long enough for them to reboot before proceeding. If this
  happens simply try to rerun the playbook.
- There is a bug in ansible for provisioning docker networks. Currently
  the docker_swarm playbook uses a workaround that avoids this problem.
- Currently there are two SIP roles to handle the docker SIP slave differences
  between the master branch and the docker swarm testing. This will be resolved
  once the docker swarm PaaS branch is merged into master. For now, SIP VMs
  can be created for testing the docker swarm paas_test branch by editing the
  Vagrantfile to select the docker_swarm HOSTS configuration and then
  provisioning the VMs with:

  ```bash
  ansible-playbook -i docker_swarm_hosts --private-key=keys/sip docker_swarm.yml
  ansible-playbook -i docker_swarm_hosts_redis --private-key=keys/sip docker_swarm_redis.yml
  ansible-playbook -i docker_swarm_hosts_redis --private-key=/home/skaprocess/.vagrant.d   insecure_private_key docker_swarm_redis.yml

  Change the mode to swarm_redis to provision both docker swarm and redis. Also input appropriate cpu and mem value
  ansible-playbook -i docker_swarm_hosts --private-key=/home/skaprocess/.vagrant.d/insecure_private_key docker_swarm.yml

  ```




