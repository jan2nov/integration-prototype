# Vagrant and Ansible scripts for SIP clusters

These scripts will create and provision a number of
VirtualBox VMs as a development environment for SIP.

In order to run these scripts you will need:
- VirtualBox (https://www.virtualbox.org)
- Vagrant (https://www.vagrantup.com)
- Ansible (https://www.ansible.com)

## Setting up VMs with Vagrant

These scripts require that the vagrant hostmanager plugin is installed
this can be done with the following command:

```vagrant plugin install vagrant-hostmanager```


In order to create the SIP VMs, from the `vagant-ansible` folder type the following command:

```vagrant up```

This will create a number Ubuntu 16.04 VMs in VirtualBox.

Once they are created, the command 

```vagrant status```

will list the VMs

It is possible to SSH into these VMs with the command

```vagrant ssh [hostname]```

To clean up and destroy the VMs use the command

```vagrant destroy```

## Provisioning VMs with Ansible

The scripts depend on an Ansible Galaxy (https://galaxy.ansible.com) role to 
install Docker on the nodes This can be obtained with the following command:

```ansible-galaxy install angstwad.docker_ubuntu```

The following command will then provision the VMs:

```ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts playbook.yml```

This can take quite a while as installing the SIP dependencies (notably spead2)
takes a long time on VMs with very modest CPU and RAM allocation.

###Notes
1. For some reason, the provisioning script can fail half way though.
If this happens re-running the ```ansible-playbook``` command above
often allows the script to proceed to the end.*

