# Waylay Storage Service

Manage storage buckets and subscriptions.


This Python package is automatically generated based on the 
Waylay Storage OpenAPI specification (API version: 0.4.1)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/storage.html).

It is considered an extension of the waylay-sdk-storage package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-storage`.

## Requirements.
This package requires Python 3.9+.

## Installation
Typically this package is installed when installing the [waylay-sdk-core](https://pypi.org/project/waylay-sdk/) package to enable the service's functionality.
When the service api methods are required, waylay-sdk-storage is included in:
- ```pip install waylay-sdk-core[storage]``` to install `waylay-sdk-core` along with only this service, or
- ```pip install waylay-sdk-core[services]``` to install `waylay-sdk-core` along with all services.
When the typed models are required, both waylay-sdk-storage and waylay-sdk-storage-types are included in:
- ```pip install waylay-sdk-core[storage,storage-types]``` to install `waylay-sdk-core` along with only this service including the typed models, or
- ```pip install waylay-sdk-core[services,services-types]``` to install `waylay-sdk-core` along with all services along with the typed models.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-storage-types` is installed
try:
    # Version
    # calls `GET /storage/v1/`
    api_response = await waylay_client.storage.about.version(
    )
    print("The response of storage.about.version:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling storage.about.version: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).
