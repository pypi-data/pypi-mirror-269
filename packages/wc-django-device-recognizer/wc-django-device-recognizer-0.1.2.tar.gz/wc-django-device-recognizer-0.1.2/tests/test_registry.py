import pytest
from ipaddress import IPv6Address, IPv4Address

from wcd_device_recognizer.services import registry, request_resolver


@pytest.mark.django_db
def test_interocutor_register(rf, UA, django_assert_num_queries):
    linux = request_resolver.resolve(rf.get('/', HTTP_USER_AGENT=UA['linux-chrome']))

    with django_assert_num_queries(10):
        linux_i, = registry.register_interlocutors((linux,))

    with django_assert_num_queries(5):
        linux_i2, = registry.register_interlocutors((linux,))

    assert linux_i[0].id == linux_i2[0].id
    assert linux_i[0].app_id is not None
    assert linux_i[0].device_id is not None
    assert linux_i[0].os_id is not None


@pytest.mark.django_db
def test_interocutor_register_ipv4(rf, UA, django_assert_num_queries):
    linux = request_resolver.resolve(rf.get(
        '/',
        HTTP_USER_AGENT=UA['linux-chrome'],
        HTTP_X_FORWARDED_FOR='168.5.1.1',
    ))
    assert isinstance(linux.ip, IPv4Address)

    with django_assert_num_queries(10):
        linux_i, = registry.register_interlocutors((linux,))

    with django_assert_num_queries(5):
        linux_i2, = registry.register_interlocutors((linux,))

    assert linux_i[0].id == linux_i2[0].id
    assert linux_i[0].app_id is not None
    connections = list(linux_i[0].network_connections.all())
    assert len(connections) == 1
    assert connections[0].ip == '168.5.1.1'


@pytest.mark.django_db
def test_interocutor_register_ipv6(rf, UA, django_assert_num_queries):
    linux = request_resolver.resolve(rf.get(
        '/',
        HTTP_USER_AGENT=UA['linux-chrome'],
        HTTP_X_FORWARDED_FOR='2a0d:9886:f:700:508c:48c2:31ba:f227',
    ))
    assert isinstance(linux.ip, IPv6Address)

    with django_assert_num_queries(10):
        linux_i, = registry.register_interlocutors((linux,))

    with django_assert_num_queries(5):
        linux_i2, = registry.register_interlocutors((linux,))

    assert linux_i[0].id == linux_i2[0].id
    assert linux_i[0].app_id is not None
    connections = list(linux_i[0].network_connections.all())
    assert len(connections) == 1
    assert connections[0].ip == '2a0d:9886:f:700:508c:48c2:31ba:f227'


@pytest.mark.django_db
def test_interocutor_register_multiple(rf, UA, django_assert_num_queries):
    linux = request_resolver.resolve(rf.get('/', HTTP_USER_AGENT=UA['linux-chrome']))
    android = request_resolver.resolve(rf.get('/', HTTP_USER_AGENT=UA['android-chrome']))

    with django_assert_num_queries(10):
        linux_i, android_i = registry.register_interlocutors((linux, android))

    assert linux_i[0].id != android_i[0].id

    with django_assert_num_queries(5):
        linux_i2, android_i2 = registry.register_interlocutors((linux, android))

    assert linux_i2[0].id != android_i2[0].id
    assert linux_i[0].id == linux_i2[0].id
    assert android_i[0].id == android_i2[0].id
