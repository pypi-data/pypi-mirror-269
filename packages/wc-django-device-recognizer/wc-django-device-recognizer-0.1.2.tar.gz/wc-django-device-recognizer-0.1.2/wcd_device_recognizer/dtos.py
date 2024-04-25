from typing import *
from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address
from decimal import Decimal
from user_agents.parsers import UserAgent

from .const import DEFAULT_DPR


__all__ = 'AppDTO', 'OSDTO', 'DeviceDTO', 'InterlocutorDTO',


DEFAULT_DPR = Decimal(1)


@dataclass(frozen=True, eq=True)
class AppDTO:
    family: str
    version: Tuple[int, ...]
    version_string: str


@dataclass(frozen=True, eq=True)
class OSDTO:
    family: str
    version: Tuple[int, ...]
    version_string: str
    arch: Optional[str] = None


@dataclass(frozen=True, eq=True)
class DeviceDTO:
    id: Optional[str] = None
    family: str = 'Other'
    brand: Optional[str] = None
    model: Optional[str] = None
    bitness: Optional[str] = None
    memory: Optional[Decimal] = None
    dpr: Decimal = DEFAULT_DPR
    viewport_width: Optional[int] = None


@dataclass(frozen=True, eq=True)
class InterlocutorDTO:
    os: OSDTO
    app: AppDTO
    device: DeviceDTO

    user_agent: UserAgent
    client_hints: Dict[str, str] = field(default_factory=dict)
    ip: Optional[Union[IPv4Address, IPv6Address]] = None
