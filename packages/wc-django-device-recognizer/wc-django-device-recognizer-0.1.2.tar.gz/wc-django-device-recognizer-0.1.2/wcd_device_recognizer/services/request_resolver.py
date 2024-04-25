from decimal import Decimal
from ipaddress import ip_address
from django.http import HttpRequest

from django_user_agents.utils import get_user_agent
from user_agents.parsers import UserAgent, parse_version
from ua_parser.user_agent_parser import ParseUserAgent

from ..const import DEFAULT_DPR
from ..dtos import InterlocutorDTO, AppDTO, OSDTO, DeviceDTO
from ..utils import stringify_version


HEADER_PREFIX = 'HTTP_'

UA_CLIENT_HINT_HEADER_PREFIX = f'{HEADER_PREFIX}SEC_CH_UA'
UA_CLIENT_HINT_GENERIC_KEY = 'generic'

DEVICE_CLIENT_HIT_HEADERS = {'DEVICE_MEMORY', 'DPR', 'VIEWPORT_WIDTH', 'WIDTH'}
NETWORK_CLIENT_HIT_HEADERS = {'DOWNLINK', 'ECT', 'RTT', 'SAVE_DATA'}

BITNESS_MAPPER = {
    '64': ('x64', 'x86_64'),
    '32': ('x32', 'x86_32'),
}
ARCH_MAPPER = {
    'x86': ('x86_32', 'x86_64'),
}

EMPTY = {None, ''}
EMPTY_FAMILIES = {'other'} | EMPTY

# Since wer'e going to use this to calculate the amount of RAM it should
# be defined the same as RAM manufactures does it. Not the truthful power of 2.
RAM_GIGABYTE = 10 ** 9


def get(source: dict, key: str, convertor: callable = None, default=None, empty=EMPTY):
    value = source.get(key, None)

    if value is None or value in empty or (isinstance(value, str) and value.lower() in empty):
        return default

    return value if convertor is None else convertor(value)


def mapper_resolver(value, mapper: dict):
    for key, values in mapper.items():
        for sub in values:
            if sub in value:
                return key


def collect_client_hints(request: HttpRequest) -> dict:
    strip = len(UA_CLIENT_HINT_HEADER_PREFIX)
    meta = request.META

    # Collecting all user agent's provided data
    client_hints = {
        (key[strip:].lstrip('_') or UA_CLIENT_HINT_GENERIC_KEY).lower(): value
        for key, value in meta.items()
        if key.startswith(UA_CLIENT_HINT_HEADER_PREFIX)
    }

    for key in DEVICE_CLIENT_HIT_HEADERS | NETWORK_CLIENT_HIT_HEADERS:
        header = HEADER_PREFIX + key
        value = meta.get(header)

        if value:
            client_hints.setdefault(key.lower(), value)

    return client_hints


def collect_app_data(ua: UserAgent, hints: dict) -> AppDTO:
    browser = ua.browser
    version = browser.version
    family = browser.family

    agent = (
        get(hints, 'full_version_list')
        or
        get(hints, UA_CLIENT_HINT_GENERIC_KEY)
        or
        get(hints, 'full_version')
    )
    if agent:
        # FIXME: This parser wouldn't work here. Should write your own.
        data = ParseUserAgent(agent)

        if data['family'].lower() not in EMPTY_FAMILIES:
            family = data['family']
            version = parse_version(
                major=data['major'], minor=data['minor'], patch=data['patch']
            )

    return AppDTO(
        family=family, version=version,
        version_string=stringify_version(version),
    )


def collect_os_data(ua: UserAgent, hints: dict) -> OSDTO:
    os = ua.os
    version = os.version
    family = os.family

    family = get(hints, 'platform', default=family, empty=EMPTY_FAMILIES)

    if 'platform_version' in hints:
        version = parse_version(
            *get(hints, 'platform_version', default='').split('.')
        )

    return OSDTO(
        family=family, version=version,
        version_string=stringify_version(version),
        arch=get(hints, 'arch') or mapper_resolver(ua.ua_string, ARCH_MAPPER),
    )


def collect_device_data(ua: UserAgent, hints: dict) -> DeviceDTO:
    device = ua.device
    model = device.model
    brand = device.brand
    family = device.family

    family = get(hints, 'platform', default=family, empty=EMPTY_FAMILIES)
    brand = brand or family
    model = get(hints, 'model', default=model)

    return DeviceDTO(
        id=(
            get(hints, 'id')
            or
            get(hints, 'identificator')
        ),
        family=family, model=model, brand=brand,
        bitness=get(hints, 'bitness') or mapper_resolver(ua.ua_string, BITNESS_MAPPER),
        memory=get(hints, 'memory', convertor=lambda x: Decimal(x) * RAM_GIGABYTE),
        dpr=get(hints, 'dpr', convertor=Decimal, default=DEFAULT_DPR),
        viewport_width=(
            get(hints, 'viewport_width', convertor=int)
            or
            get(hints, 'width', convertor=int)
        ),
    )


def resolve(request: HttpRequest) -> InterlocutorDTO:
    client_hints = collect_client_hints(request)
    ua = get_user_agent(request)
    ip = request.META.get('HTTP_X_FORWARDED_FOR')

    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if ip:
        try:
            ip = ip_address(ip)
        except ValueError:
            ip = None

    return InterlocutorDTO(
        ip=ip if ip else None,
        os=collect_os_data(ua, client_hints),
        app=collect_app_data(ua, client_hints),
        device=collect_device_data(ua, client_hints),

        user_agent=ua,
        client_hints=client_hints,
    )
