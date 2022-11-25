from datetime import datetime, timedelta

def extract_time(time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            return None

        if unit == "s":
            bantime = datetime.now() + timedelta(seconds=int(time_num))
        elif unit == "m":
            bantime = datetime.now() + timedelta(minutes=int(time_num))
        elif unit == "h":
            bantime = datetime.now() + timedelta(hours=int(time_num))
        elif unit == "d":
            bantime = datetime.now() + timedelta(days=int(time_num))
        else:
            # how even...?
            return None
        return bantime
    else:
        return None
