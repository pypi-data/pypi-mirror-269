# Waylay Resources Service
This service manages 
[Waylay Resources](/#/features/resources/?id=resource) and related entities.

A _Waylay Resource_ models a real-world device or abstract entity of your IoT solution,
and provides a context when processing data in the Rule Engine.

You'll interact with the _Waylay Resources_ API to create this _Digital Twin_ model, 
a process that's also called _resource provisioning_.

This Python package is automatically generated based on the 
Waylay Resources OpenAPI specification (API version: 8.1.0)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/resources.html).

It is considered an extension of the waylay-sdk-resources package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-resources`.

## Requirements.
This package requires Python 3.9+.

## Installation
Typically this package is installed when installing the [waylay-sdk-core](https://pypi.org/project/waylay-sdk/) package to enable the service's functionality.
When the service api methods are required, waylay-sdk-resources is included in:
- ```pip install waylay-sdk-core[resources]``` to install `waylay-sdk-core` along with only this service, or
- ```pip install waylay-sdk-core[services]``` to install `waylay-sdk-core` along with all services.
When the typed models are required, both waylay-sdk-resources and waylay-sdk-resources-types are included in:
- ```pip install waylay-sdk-core[resources,resources-types]``` to install `waylay-sdk-core` along with only this service including the typed models, or
- ```pip install waylay-sdk-core[services,services-types]``` to install `waylay-sdk-core` along with all services along with the typed models.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-resources-types` is installed
from waylay.services.resources.models.version_response import VersionResponse
try:
    # Get Service Information
    # calls `GET /resources/v1/`
    api_response = await waylay_client.resources.about.get(
    )
    print("The response of resources.about.get:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling resources.about.get: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).
