from datetime import datetime, timezone

from ..ads_device_notification import ADSDeviceNotificationResponse


def test_device_notification_response() -> None:
    raw_data = bytes.fromhex("1a00000001000000f0bc3475337bda0101000000ab000000020000000200")

    request = ADSDeviceNotificationResponse.from_bytes(data=raw_data)
    assert len(request.samples) == 1
    sample = request.samples[0]
    assert sample.timestamp == 0x01DA7B337534BCF0
    assert sample.handle == 0xAB
    assert sample.data == bytes.fromhex("02 00")
    assert sample.update_time == datetime(
        year=2024, month=3, day=21, hour=1, minute=59, second=50, microsecond=79000, tzinfo=timezone.utc
    )
