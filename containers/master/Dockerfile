ARG tag=latest
FROM sip-base:$tag

# Copy the SIP
ADD sip/master/ sip/master
ADD sip/common/ sip/common

ENTRYPOINT python3 -m sip.master
