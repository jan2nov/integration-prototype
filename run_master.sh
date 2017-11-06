#!/bin/sh
if [ -z "$SIP_IMAGE_LABEL" ]; then
	SIP_IMAGE_LABEL="latest"
fi

echo "Running with tag $SIP_IMAGE_LABEL"

docker image ls | grep sip-master | grep $SIP_IMAGE_LABEL >/dev/null

if [ "$?" -eq 0 ]; then
	echo "Found suitable Docker master image. Running sip-master:$SIP_IMAGE_LABEL."
	docker run -v /var/run/docker.sock:/var/run/docker.sock -e SIP_IMAGE_LABEL=$SIP_IMAGE_LABEL -p 12345:12345 sip-master:$SIP_IMAGE_LABEL
	if [ "$?" -eq 0 ]; then
		echo "Exited successfully."
	else
		echo "Exited in failed state, exit code: $?"
	fi
else
	echo "No suitable Docker images found. Please build SIP with docker-compose"
	echo "using \$SIP_IMAGE_LABEL=$SIP_IMAGE_LABEL, or using setup.py:"
	echo "python setup.py build_containers --label=$SIP_IMAGE_LABEL"
fi
