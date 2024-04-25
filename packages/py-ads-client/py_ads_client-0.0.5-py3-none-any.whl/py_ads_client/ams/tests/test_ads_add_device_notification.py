from ...constants.index_group import IndexGroup
from ...constants.return_code import ADSErrorCode
from ...constants.transmission_mode import TransmissionMode
from ..ads_add_device_notification import ADSAddDeviceNotificationRequest, ADSAddDeviceNotificationResponse


def test_add_device_notification_request() -> None:
    raw_data = bytes.fromhex("05f000000e00804b0200000004000000010000000100000000000000000000000000000000000000")

    request = ADSAddDeviceNotificationRequest(
        index_group=IndexGroup.SYMVAL_BYHANDLE,
        index_offset=0x4B80000E,
        length=2,
        transmission_mode=TransmissionMode.ADSTRANS_SERVERONCHA,
        max_delay_ms=1,
        cycle_time_ms=1,
    )

    assert request.to_bytes() == raw_data


def test_add_device_notification_response() -> None:
    raw_data = bytes.fromhex("00000000ab000000")

    response = ADSAddDeviceNotificationResponse.from_bytes(raw_data)

    assert response.result == ADSErrorCode.ERR_NOERROR
    assert response.handle == 0x000000AB
