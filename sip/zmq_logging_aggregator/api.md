# ZMQ Logging aggregator _<`skasip/zla`>_

## API Version
`ZLA API version 0.1.0`

*The API version is useful to avoid forcing people to used a specific API 
version. This could be tied to the SIP version however rather than per service.*

see <https://gist.github.com/iros/3426278>

## Changes (Changelog for the API)

### `0.1.0`

#### Added
* Initial API version

## Provided interfaces

<hr>

### ZMQ SUB Socket (TCP Socket?)

* **Description**

  * This can be connected to using a ZMQ PUB socket.
    This is exposed on the python logging handlers DEFAULT_TCP_LOGGING_PORT,port 9020.

  * The SUB socket listens for data in the form of
    jsonified Python logging LogRecord objects send using a ZMQ multipart send

* **Protocol:**

  * `LogRecord.__dict__`

* **Data params:**


* **Sample Call:**



<hr>

### Healthcheck (REST)

Returns json data about the health of the service.

* **URL**

  `/healthcheck`

* **Method**

  `GET`

* **URL Params**

  None

* **Data params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content** `{ id : 12 }`

* **Error Response:**

* **Sample Call:**

  `curl http://localhost:5555/healtcheck`

<hr>

### Logging configuration server (Socket)

* **Description:**

  x

* **Protocol:**

  x

* **Data:**

  x

## Required interfaces:

### None
