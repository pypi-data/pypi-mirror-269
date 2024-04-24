# [Logstash API](http://logstash-api.hive.pt)

Simple Python API client for [Logstash](https://www.elastic.co/products/logstash).

## Configuration

| Name                     | Type  | Description                                                                                                                                          |
| ------------------------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LOGSTASH_BASE_URL**    | `str` | The base URL value to be used to communicate using the Logstash API, should include username and password if HTTP Auth is used (defaults to `None`). |
| **LOGSTASH_BUFFER_SIZE** | `int` | The size of the buffer (in number of entries) until the buffer is flushed (defaults to `128`).                                                       |
| **LOGSTASH_TIMEOUT**     | `int` | The timeout in seconds in seconds until the buffer is flushed (defaults to `30`).                                                                    |

## License

Logstash API is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://app.travis-ci.com/hivesolutions/logstash-api.svg?branch=master)](https://travis-ci.com/github/hivesolutions/logstash-api)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/logstash-api/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/logstash-api?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/logstash-api.svg)](https://pypi.python.org/pypi/logstash-api)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
