from typing import List, Optional, Sequence, Tuple

from ..models import Interlocutor, App, OS, Device, InterlocutorNetwork
from ..dtos import InterlocutorDTO, AppDTO, OSDTO, DeviceDTO
from ..utils import model_bulk_get_or_create, to_list


def register_apps(
    items: Sequence[AppDTO]
) -> List[App]:
    return model_bulk_get_or_create(App, [
        ({'family': x.family, 'version': x.version or []}, {})
        for x in items
    ])


def register_devices(
    items: Sequence[DeviceDTO]
) -> List[Device]:
    return model_bulk_get_or_create(Device, [
        ({
            'family': x.family,
            'brand': x.brand or '',
            'model': x.model or '',
            'bitness': x.bitness or '',
            'memory': x.memory,
            'dpr': x.dpr,
            'viewport_width': x.viewport_width,
        }, {})
        for x in items
    ])


def register_oss(
    items: Sequence[OSDTO]
) -> List[OS]:
    return model_bulk_get_or_create(OS, [
        ({'family': x.family, 'version': x.version or [], 'arch': x.arch or ''}, {})
        for x in items
    ])


def register_interlocutors(
    items: Sequence[InterlocutorDTO]
) -> List[Tuple[Interlocutor, Optional[InterlocutorNetwork]]]:
    items = to_list(items)
    apps_list = list({x.app for x in items})
    oss_list = list({x.os for x in items})
    devices_list = list({x.device for x in items})

    apps = dict(zip(apps_list, register_apps(apps_list)))
    oss = dict(zip(oss_list, register_oss(oss_list)))
    devices = dict(zip(devices_list, register_devices(devices_list)))

    interlocutors = model_bulk_get_or_create(Interlocutor, [
        (
            {
                'os_id': oss[x.os].id if x.os in oss else None,
                'app_id': apps[x.app].id if x.app in apps else None,
                'device_id': devices[x.device].id if x.device in devices else None,
                'outer_id': x.device.id or '',
                'user_agent': x.user_agent.ua_string or '',
            },
            {'client_hints': x.client_hints}
        )
        for x in items
    ])
    ip_definitions = [
        (items[i].ip, x.id)
        for i, x in enumerate(interlocutors) if items[i].ip
    ]
    networks_map = {}

    if len(ip_definitions) != 0:
        networks = model_bulk_get_or_create(InterlocutorNetwork, [
            ({'ip': str(ip), 'interlocutor_id': id}, {})
            for ip, id in ip_definitions
        ])
        networks_map = {x.interlocutor_id: x for x in networks}

    return [(i, networks_map.get(i.id, None)) for i in interlocutors]
