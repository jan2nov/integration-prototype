# coding: utf-8

from docker import Client
cli = Client(version='1.21', base_url='unix://var/run/docker.sock')

#container_id = c.create_container('telescope_state_service', '/docker-entrypoint.s', ports=[7000, 7001, 7002, 7003, 7004, 7005, 7006, 7007])
container_id = cli.create_container(
    'telescope_state_service', ports=[7000, 7001, 7002, 7003, 7004, 7005, 7006, 7007],
    host_config=cli.create_host_config(port_bindings={
        7000: 7000, 
	7001: 7001, 
	7002: 7002, 
	7003: 7003, 
	7004: 7004, 
	7005: 7005, 
	7006: 7006, 
	7007: 7007	
    })
)

cli.start(container_id)
