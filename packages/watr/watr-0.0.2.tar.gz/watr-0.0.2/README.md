# Watr Python 1.0.0

A python library for the Watr API.

## Installation

```pip3 install watr```

## Requirements

- Python 3.6+

## Usage

```python
from watr import WatrApi

# some await things here...
watrApi = WatrApi("your@email.com", "yourpassword123")
# or if you have tokens already
watrApi = WatrApi(access_token="youraccesstoken", refresh_token="yourrefreshtoken")
watrSystem = WatrSystem({}, watrApi)
sprinkler_systems = watrSystem.get_systems()
home_system = sprinkler_systems[0]
if home_system.enabled():
    sprinkler_systems[0].toggle()
sprinkler_systems[0].zones[0].toggle()
```

## Documentation

More indepth documentation is available
at [https://watr.peasenet.com/docs/python](https://watr.peasenet.com/docs/python)