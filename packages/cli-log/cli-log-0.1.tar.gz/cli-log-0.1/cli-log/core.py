import colorama
from .utils import format_time

colorama.init(autoreset=True)

LOG_FORMAT = "[{time} / {severity}]{prefix} {message}"
INFO_COLOR = colorama.Fore.BLUE
DEBUG_COLOR = colorama.Fore.GREEN
WARN_COLOR = colorama.Fore.YELLOW
ERROR_COLOR = colorama.Fore.RED

def info(message: str, prefix: str = '') -> None:
    """
    Logs an informational message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to ''.
    """
    log("INFO", message, prefix, INFO_COLOR)

def debug(message: str, prefix: str = '') -> None:
    """
    Logs a debug message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to ''.
    """
    log("DEBUG", message, prefix, DEBUG_COLOR)

def warn(message: str, prefix: str = '') -> None:
    """
    Logs a warning message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to ''.
    """
    log("WARN", message, prefix, WARN_COLOR)

def error(message: str, prefix: str = '') -> None:
    """
    Logs an error message.

    Parameters
    -----------
    `message` : :class:`str` 
        The message to log.
    `prefix` : :class:`str`, optional
        An optional prefix for the log message. Defaults to ''.
    """
    log("ERROR", message, prefix, ERROR_COLOR)

def log(severity: str, message: str, prefix: str, color: str = '') -> None:

    msg = LOG_FORMAT
    time = format_time()
    lines = message.split('\n') # Split the message into lines
    lines = [msg.format(prefix=(f"[{prefix}]" if prefix else ""), severity=severity, message=line, time=time) for line in lines if line.strip()] # Prepend each line with the timestamp and severity information
    msg_console = '\n'.join(lines) # Join the lines back together
    log_to_console(msg_console, color)

def log_to_console(message: str, color: str = ''):
    print(color + message)