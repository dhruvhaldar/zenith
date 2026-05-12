import datetime
time = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
print(time.timestamp())
print(time.replace(tzinfo=datetime.timezone.utc).timestamp())
