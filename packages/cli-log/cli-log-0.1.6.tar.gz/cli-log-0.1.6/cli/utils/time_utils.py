import datetime

def format_time(timestamp: float = 0) -> str:
    """
    Format given timestamp, uses current time if no timestamp is provided
    """
    
    if timestamp:
        return datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
    return datetime.datetime.now().strftime("%H:%M:%S")