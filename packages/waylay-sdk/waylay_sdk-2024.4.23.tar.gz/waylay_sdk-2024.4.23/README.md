# Waylay Python SDK

Python SDK for the Waylay Platform.

This `waylay-sdk` package is the main entrypoint to install the python SDK client for the [Waylay REST apis](https://docs.waylay.io/#/api/?id=openapi-docs).

It includes api support for the most relevant services, as extensions for the `waylay-sdk-core` base SDK client.

Alternatively:
* use the [`waylay-sdk-core`](https://pypi.org/project/waylay-sdk-core) package for a minimal SDK client
* use any of the `waylay-sdk-{service}` packages to install an SDK client that has api support for the selected service(s) only.


See [Waylay Docs](https://docs.waylay.io/#/api/sdk/python) for extensive documentation.

## Installation

This package requires a python runtime `3.9` or higher.

The basic client with api support for the [common services](#service-packages), can be installed with
```bash
pip install waylay-sdk
```

To additionally [typing](#service-packages) support for a given service, e.g. for the `alarms` service:
```bash
pip install waylay-sdk[types-alarms]
```
... or for all services:
```bash
pip install waylay-sdk[types]
```

## Service packages

Support for a specific Waylay REST api comes as a separate _service package_.
Each _service_ provides two packages:
* an _api_ package `waylay-<service>-sdk` that describes all resources and actions for that service. JSON request and responses are represented as basic python data (_dict_, _list_, primitives)
* a _types_ package `waylay-<service>-sdk-types` that provides [pydantic](https://docs.pydantic.dev/) models to represent JSON request and responses.

The _types_ package is optional. When installed, its _pydantic_ models are used to serialize requests and deserialize responses. When used in a python IDE, code completion will help you navigate the attributes of request and responses.
This makes it easier to interact with the API as a developer. 
But as the underlying REST api evolves, the _types_ package might require regular dependency updates.

Use the _types_ package for interactive cases (python notebooks), or solutions that are regularly tested and maintained. 

When not installed, the SDK client does not interfere with the json representations of requests and responses, and you should check the [API documentation](https://docs.waylay.io/#/api/?id=openapi-docs) of the service for exact specifications.

The Service plugs are _generated_ from their [openapi description](https://docs.waylay.io/#/api/?id=openapi-docs).

#### Included dependencies

This release of `waylay-sdk` includes the following _api_ and (optional) _types_ packages

| name | package | api endpoint | docs | types package 
| ------- | ------------------ | ------- | --| --|
| `alarms` | [`waylay-sdk-alarms`](https://pypi.org/project/waylay-sdk-alarms) | `/alarms/v1` | [doc](https://docs.waylay.io/#/api/alarms/) [openapi](https://docs.waylay.io/openapi/public/redocly/alarms.html) | [`waylay-sdk-alarms-types`](https://pypi.org/project/waylay-sdk-alarms-types/) |
| `data` | [`waylay-sdk-data`](https://pypi.org/project/waylay-sdk-data) | `/data/v1` | [doc](https://docs.waylay.io/#/api/broker/) [openapi](https://docs.waylay.io/openapi/public/redocly/data.html) | [`waylay-sdk-data-types`](https://pypi.org/project/waylay-sdk-data-types/) |
| `registry` | [`waylay-sdk-registry`](https://pypi.org/project/waylay-sdk-registry) | `/registry/v2` | [doc](https://docs.waylay.io/#/api/registry/) [openapi](https://docs.waylay.io/openapi/public/redocly/registry.html) | [`waylay-sdk-registry-types`](https://pypi.org/project/waylay-sdk-registry-types/) |
| `resources` | [`waylay-resources-alarms`](https://pypi.org/project/waylay-sdk-resources) | `/resources/v1` | [doc](https://docs.waylay.io/#/api/resources/) [openapi](https://docs.waylay.io/openapi/public/resources/alarms.html) | [`waylay-sdk-resources-types`](https://pypi.org/project/waylay-sdk-resources-types/) |
| `rules` | [`waylay-sdk-rules`](https://pypi.org/project/waylay-sdk-rules) | `/rules/v1` | [doc](https://docs.waylay.io/#/api/rules/) [openapi](https://docs.waylay.io/openapi/public/redocly/rules.html) | [`waylay-sdk-rules-types`](https://pypi.org/project/waylay-sdk-rules-types/) |
| `storage` | [`waylay-sdk-storage`](https://pypi.org/project/waylay-sdk-storage) | `/storage/v1` | [doc](https://docs.waylay.io/#/api/storage/) [openapi](https://docs.waylay.io/openapi/public/redocly/storage.html) | [`waylay-sdk-storage-types`](https://pypi.org/project/waylay-sdk-storage-types/) |



## Basic usage

### In webscripts and plugins

The SDK client can be used in the _python_ webscripts and plugins of the Waylay platform.

In that case, the webscript or plugin _runtime_ will configure and authenticate a client, and 
provide it as a `waylay` parameter to the _webscript_ or _plugin_ callback function.

You just need to state the `waylay-sdk` dependency when authoring the _webscript_ or _plugin_.


#### webscript example
```python
async def execute(request: Request, waylay: WaylayClient):
    # list templates with the query as specified in the request body
    template_query = request.json()
    templates = await waylay.rules.templates.list(query=template_query)
    return templates
```

#### plug example
```python
from csv import DictReader
from io import StringIO
async def execute(path: str, waylay: WaylayClient):
    """Return the CSV data from a file in assets storage."""
    # use the _List Objects_ operation, using the `path` plug property
    sign_resp = await waylay.storage.objects.list('assets', path, query={"sign": "GET"})
    content_url = sign_resp._links.get_object.href
    # fetch the csv data with the generic rest client, disable waylay auth for this signed url
    csv_data = await waylay.api_client.request('GET', content_url, auth=None)
    # parse as csv and return as a (state, rawData) tuple
    return ('OK', data=[
        record for record in DictReader(StringIO(csv_data))
    ])
```

### Interactive Authentication
When used outside the Waylay platform (e.g. in a _python notebook_) the client requires you to provide
* the gateway endpoint: `api.waylay.io` for Enterprise users,
* an API key-secret pair: see [Waylay Console](console.waylay.io) at _>Settings>Authentication keys_.

```python
from waylay.sdk import WaylayClient

# this will interactively request the gateway and credentials on first usage.
client = WaylayClient.from_profile()

# list the available service packages
client.services

# use the generic api client to see the status page of the 'registry' service.
resp = await client.api_client.request('GET', '/registry/v2')
```

Credentials and endpoints are stored in a local _profile_ file (you can have multiple such profiles).
Other authentication methods are available (JWToken, pass apiKey/Secret directly)
