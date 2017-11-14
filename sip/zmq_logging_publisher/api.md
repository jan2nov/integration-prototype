# skasip/zlp: ZeroMQ Logging Publisher service

## Provided interfaces

### ZMQ PUB Socket (TCP)

* **Description**

  * This can be connected to using a ZMQ PUB socket.
    This is exposed on the python logging handlers DEFAULT_TCP_LOGGING_PORT,port 9020.

  * The SUB socket listens for data in the form of
    jsonified Python logging LogRecord objects send using a ZMQ multipart send

* **Protocol:**

  * `LogRecord.__dict__`

* **Data params:**


* **Sample Call:**

## Required interfaces

### ZMQ SUB Socket (TCP)

* **Description**

* **Protocol:**

* **Data params:**


* **Sample Call:**
