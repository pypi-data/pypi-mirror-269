# WebCase device recognizing utility

## Installation

```sh
pip install wc-django-device-recognizer
```

It depends on `django-user-agents`, so check out [it's documentation](https://pypi.org/project/django-user-agents/) about additional installation instructions.

In `settings.py`:

```python
INSTALLED_APPS += [
  'wcd_device_recognizer',
]
```

## Usage

To get all possible information from request:

```python
from wcd_device_recognizer.services import request_resolver

interlocutor = request_resolver.resolve(request)

assert interlocutor.device.bitness == '64'
assert interlocutor.os.family == 'Linux'
assert interlocutor.os.arch == 'x86'
assert interlocutor.app.family == 'Chrome'
assert interlocutor.app.version == (101, 0, 0)
assert interlocutor.device.dpr == 1
```

And then you may save interlocutor's data to database:

```python
from wcd_device_recognizer.services import registry

# You may pass any amount of interlocutors to register here.
registry.register_interlocutors((interlocutor,))
```

## Coverage

To collect interlocutor's data package uses User-Agent info and standart HTTP headers:

- `Sec-CH-UA`
- `Sec-CH-UA-Arch`
- `Sec-CH-UA-Bitness`
- `Sec-CH-UA-Full-Version`
- `Sec-CH-UA-Full-Version-List`
- `Sec-CH-UA-Mobileser experience.`
- `Sec-CH-UA-Model`
- `Sec-CH-UA-Platform`
- `Sec-CH-UA-Platform-Version`
- `Content-DPR`
- `Device-Memory`
- `DPR`
- `Viewport-Width`
- `Width`

For details look here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#user_agent_client_hints

Also any `Sec-CH-UA-{key-name}` will be saved.

To provide some unique device identifier use: **`Sec-CH-UA-ID`** header.
