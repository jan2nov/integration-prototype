# Redis-Cluster using Vagrant and Ansible
Setup Redis Cluster using Vagrant and Ansible

The github branch local_telescope_state contains the scripts.

cd integration-prototype/sip/local_telescope_state/redis_vagrant_ansible

#Install VM's

vagrant up

#Provision using Ansible

ansible-playbook -i hosts -vvvv --private-key=/home/skaprocess/.vagrant.d/insecure_private_key ansible-redis.yml

(Make sure to change the directory for the insecure_private_key)

Note. It might hang or show an error message when an ssh is established. Either cancel it and re-run the playbook or type "yes" and it might continue.
      Not sure about the reason why this happens. Will be looking into it.

#To login into Vm's

vagrant ssh <hosts>

e.g vagrant ssh redismaster

#To use the redis-cli in VM's

/opt/redis/bin/redis-cli

#To Install Redis to your machine

wget http://download.redis.io/releases/redis-3.2.6.tar.gz

tar xzf redis-3.2.6.tar.gz

cd redis-3.2.6

make

#Redis for Python

sudo pip3 install redis

#To run the redis client

execute python3 redis_client.py

This is a simple redis client. It will write, read, delete some sample variables.

