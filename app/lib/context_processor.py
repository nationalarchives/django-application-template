from datetime import datetime, timezone


def now_iso_8601():
    now = datetime.now(tz=timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")
