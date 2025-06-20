import sys
from datetime import datetime
from functools import wraps

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class logger_class:
    """ This Logger class provides a simple logging mechanism with adjustable log levels and date/time formats. Also contains different methods for logging messages at various levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). The date/time format can be customized with preset styles (YYYY-MM-DD, DD-MM-YYYY, MM/DD/YYYY) or set to custom formats. Critical messages will terminate the program."""

    def __init__(self, level="INFO"):
        self.format = "%Y-%m-%d  %H:%M:%S"
        self.loglevel = level.upper()

    def set_loglevel(self, level: str):
        """
        Set the default log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
        
        Only messages at or above this level will be printed.

        Parameters:
            level (str): The log level to set. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL.
        """
        level = level.upper()
        if level not in LOG_LEVELS:
            raise ValueError(
                f"Invalid log level '{level}'. Choose from: {', '.join(LOG_LEVELS)}")
        self.loglevel = level

    def __should_log(self, level):
        """
        Check if the message should be logged based on the current log level.
        Parameters:
            level (str): The log level of the message to check.
        Returns:
            bool: True if the message should be logged, False otherwise.
        """
        return LOG_LEVELS.index(level) >= LOG_LEVELS.index(self.loglevel)

    def __log(self, level, message):

        # Store datetime object, not formatted string
        timestamp = datetime.now()
        if self.__should_log(level):
            formatted_time = timestamp.strftime(f"{self.format}")
            print(f"{formatted_time} [{level}]: {message}")
            if level == "CRITICAL":
                sys.exit(1)

    def debug(self, message: str) -> None:
        """
        Debug messages are usually used for development and debugging purposes.They provide detailed information about the program's execution, which can help developers identify issues or understand the flow of the application.
        """
        self.__log("DEBUG", message)

    def info(self, message: str) -> None:
        """
        Info messages provide general information about the program's operation, such as startup messages, configuration details, or other significant events that are not errors.
        """
        self.__log("INFO", message)

    def warning(self, message: str) -> None:
        """
        Warning messages indicate potential issues or situations that may require attention but do not necessarily stop the program's execution.
        """
        self.__log("WARNING", message)

    def error(self, message: str) -> None:
        """
        Error messages indicate that something has gone wrong, such as a failed operation or an exception that was caught. These messages are more serious than warnings and may require immediate attention."""
        self.__log("ERROR", message)

    def critical(self, message: str) -> None:
        """
        Critical messages indicate a severe error that has caused the program to terminate or will cause it to terminate. These messages are the most serious and usually require immediate action.
        """
        self.__log("CRITICAL", message)

    def __call__(self, func):
        """
        A decorator that will wrap the function its called over to log the calling of function and provide the execution duration for that particular function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            arg_list = [repr(a) for a in args] + \
                [f"{k}={v!r}" for k, v in kwargs.items()]
            arg_str = ", ".join(arg_list)

            self.info(f"Calling {func_name}({arg_str})")
            start = datetime.now()
            try:
                result = func(*args, **kwargs)
                self.info(f"{func_name} returned {result!r}")
                return result
            except Exception as e:
                self.error(f"Error in {func_name}: {e}")
                raise
            finally:
                end = datetime.now()
                elapsed = (end - start).total_seconds()
                self.debug(f"{func_name} execution time: {elapsed:.4f}s ")
        return wrapper
