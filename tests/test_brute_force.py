from datetime import datetime, timedelta

from app.detection.brute_force import detect_brute_force


class FakeEvent:
    def __init__(self, timestamp, source_ip, event_type):
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.event_type = event_type


def test_brute_force_detection():

    start_time = datetime(2026, 9, 9, 0, 30, 0)

    events = [
        FakeEvent(
            start_time + timedelta(seconds=i * 15),
            "192.168.1.42",
            "login_failed"
        )
        for i in range(6)
    ]

    alerts = detect_brute_force(events)

    assert len(alerts) == 1
    assert alerts[0]["type"] == "Brute Force Attack"
    assert alerts[0]["severity"] == "high"