from datetime import datetime


def log_activity(activity):
    with open("activity_log.txt", "a") as log:
        log.write(f"{datetime.now()}: {activity}\n")
