from datetime import timedelta


FAILED_LOGIN_THRESHOLD = 5
TIME_WINDOW_MINUTES = 2


def detect_brute_force(events):
    alerts = []

    events = sorted(events, key=lambda event: event.timestamp)

    for i, event in enumerate(events):

        if event.event_type != "login_failed":
            continue

        failed_attempts = [
            previous_event
            for previous_event in events[:i + 1]
            if (
                previous_event.event_type == "login_failed"
                and previous_event.source_ip == event.source_ip
                and event.timestamp - previous_event.timestamp
                <= timedelta(minutes=TIME_WINDOW_MINUTES)
            )
        ]

        if len(failed_attempts) > FAILED_LOGIN_THRESHOLD:
            alerts.append({
                "type": "Brute Force Attack",
                "severity": "high",
                "source_ip": event.source_ip,
                "attempts": len(failed_attempts),
                "description": (
                    f"Detected {len(failed_attempts)} failed login attempts "
                    f"from {event.source_ip} within "
                    f"{TIME_WINDOW_MINUTES} minutes."
                )
            })

            break

    return alerts