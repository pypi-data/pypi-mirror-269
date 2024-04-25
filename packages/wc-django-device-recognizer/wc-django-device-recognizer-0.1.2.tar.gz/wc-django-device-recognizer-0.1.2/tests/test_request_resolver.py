from wcd_device_recognizer.services import request_resolver

from .utils import log_interlocutor_dto


def test_basic_user_agent(rf, UA):
    linux = request_resolver.resolve(rf.get('/', HTTP_USER_AGENT=UA['linux-chrome']))
    assert linux.device.bitness == '64'
    assert linux.os.family == 'Linux'
    assert linux.os.arch == 'x86'
    assert linux.app.family == 'Chrome'
    assert linux.app.version == (101, 0, 0)
    assert linux.device.dpr == 1

    android = request_resolver.resolve(rf.get(
        '/', HTTP_USER_AGENT=UA['android-chrome'],
    ))
    assert android.device.brand == 'Samsung'
    assert android.device.model == 'SM-S906N'
    assert android.os.family == 'Android'
    assert android.os.version == (12,)
    assert android.app.family == 'Chrome Mobile WebView'
    assert android.app.version == (80, 0, 3987)

    ios = request_resolver.resolve(rf.get(
        '/', HTTP_USER_AGENT=UA['ios-safari'],
    ))
    assert ios.device.brand == 'Apple'
    assert ios.device.model == 'iPhone14,3'
    assert ios.os.family == 'iOS'
    assert ios.os.version == (15, 0)
    assert ios.app.family == 'Mobile Safari'
    assert ios.app.version == (10, 0)


def test_user_agent_with_hints(rf, UA):
    android = request_resolver.resolve(rf.get(
        '/', HTTP_USER_AGENT=UA['android-chrome'],
        HTTP_SEC_CH_UA_ID='485', HTTP_SEC_CH_UA_MEMORY='0.25',
    ))
    assert android.device.brand == 'Samsung'
    assert android.device.model == 'SM-S906N'
    assert android.device.id == '485'
    assert android.device.memory == 250000000
    assert android.os.family == 'Android'
    assert android.os.version == (12,)
    assert android.app.family == 'Chrome Mobile WebView'
    assert android.app.version == (80, 0, 3987)

    ios = request_resolver.resolve(rf.get(
        '/', HTTP_USER_AGENT=UA['ios-safari'], HTTP_SEC_CH_UA_MODEL='OtherPhone',
    ))
    assert ios.device.brand == 'Apple'
    assert ios.device.model == 'OtherPhone'
    assert ios.os.family == 'iOS'
    assert ios.os.version == (15,0)
    assert ios.app.family == 'Mobile Safari'
    assert ios.app.version == (10, 0)

    data = request_resolver.resolve(rf.get(
        '/', HTTP_USER_AGENT=UA['ps5'],
        HTTP_SEC_CH_UA='"Opera";v="81", " Not;A Brand";v="99", "Chromium";v="95"',
    ))
    # log_interlocutor_dto(data)
    # FIXME: Versions parser should be added.
    # assert data.app.family == 'Opera'
    # assert data.app.version == (81,)
