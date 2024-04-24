from datetime import datetime

def str_isoformat(date:datetime) -> str:
    return  f"{date.isoformat(timespec='milliseconds')}Z"