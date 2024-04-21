# SAP IQ Provider for Apache Airflow

[![PyPI - Version](https://img.shields.io/pypi/v/airflow-provider-sapiq.svg)](https://pypi.org/project/airflow-provider-sapiq)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/airflow-provider-sapiq.svg)](https://pypi.org/project/airflow-provider-sapiq)

-----

**Table of Contents**

- [Installation](#installation)
- [Configuration](#configuration)
- [License](#license)

## Installation

```console
pip install airflow-provider-sapiq
```

## Configuration

In the Airflow user interface, configure a connection with the `Conn Type` set to SAP IQ.
Configure the following fields:

- `Conn Id`: How you wish to reference this connection.
    The default value is `sapiq_default`.
- `userid`: Login for the SAP IQ server.
- `password`: Password for the SAP IQ server.,
- `port`: Port for the SAP IQ server, typically 2638.
- `host`: Host of the SAP IQ server.

## Modules

### SAP IQ Operator

The `SapIqOperator` exequtes SQL query on SAP IQ server.

Import into your DAG using:

```Python
from sapiq_provider.operators.SapIqOperator import SapIqOperator
```

## License

`airflow-provider-sapiq` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
