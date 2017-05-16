# Redis-Cluster using Vagrant and Ansible
Setup Redis Cluster using Vagrant and Ansible

#Install VM's

vagrant up

#Provision using Ansible

ansible-playbook -i hosts -vvvv --private-key=/home/skaprocess/.vagrant.d/insecure_private_key ansible-redis.yml

(Make sure to change the directory for the insecure_private_key)

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

cd integration-prototype/sip/local_telescope_state/redis_vagrant_ansible    redis-cli -c -p 7000    

execute python3 -m redis_client.py

This is a simple redis client. It will write, read, delete some sample variables.


