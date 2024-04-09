# logging_handler.py
import logging
import datetime
import os
import sys

# Global registry to keep track of file handlers for each filename
file_handler_registry = {}

# Custom FileHandler to add functionality for line number limitation
class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=2000, *args, **kwargs):
        # Initialize the parent class with the provided filename and any other arguments.
        super().__init__(filename, *args, **kwargs)
        # Set the maximum number of lines this log file should contain.
        self.max_lines = max_lines
        self.filename = filename

    def emit(self, record):
        # This method is called whenever a log message needs to be written to the file.
        # First, let the parent class handle the actual logging.
        super().emit(record)
        # After logging, check and enforce the max_lines constraint.
        self.ensure_max_lines()

    def ensure_max_lines(self):
        # Open the file to read lines and then truncate if necessary.
        with open(self.filename, 'r+') as file:
            lines = file.readlines()
            # If the total number of lines exceeds max_lines, remove the oldest entries.
            if len(lines) > self.max_lines:
                file.seek(0)  # Go back to the start of the file
                file.writelines(lines[-self.max_lines:])  # Write back only the allowed number of recent lines
                file.truncate()  # Remove any leftover data at the end of the file

def create_file_handler(filename, level=logging.DEBUG, max_lines=2000, print_log_messages=False):
    """
    Creates or reuses a file handler for the specified log file, ensuring it doesn't exceed a maximum number of lines.

    :param filename: The name of the log file.
    :param level: The logging level, e.g., DEBUG, INFO.
    :param max_lines: Maximum number of lines the log file should contain.
    :param print_log_messages: If True, also print log messages to stdout.
    :return: Configured file handler.
    """
    if filename in file_handler_registry:
        # If a handler for this file already exists, reuse it.
        fh = file_handler_registry[filename]
    else:
        # Otherwise, create a new CustomFileHandler with the max_lines limit.
        fh = CustomFileHandler(filename, max_lines=max_lines)
        fh.setLevel(level)
        # Set a formatter to define how log messages are structured.
        formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(name)s | %(message)s')
        # Modify the formatter to use a custom time format for timestamps.
        logging.Formatter.formatTime = lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat()
        
        if print_log_messages:
            # If requested, add a handler to also print all logs to stdout.
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        fh.setFormatter(formatter)
        # Register this handler so it can be reused for the same file name.
        file_handler_registry[filename] = fh

    return fh

def get_logger(filename, level=logging.DEBUG, max_lines=2000, print_log_messages=False):
    """
    Returns a logger configured with a specific file handler, ensuring it respects the maximum number of log lines.

    :param filename: The filename for the log file.
    :param level: The logging level.
    :param max_lines: Maximum number of lines the log file should contain.
    :param print_log_messages: If True, log messages will also be printed to stdout.
    :return: A logger instance configured with a file handler for the specified filename.
    """
    # Create a unique name for the logger based on the filename to ensure each logger is unique.
    logger_name = f"logger_{filename}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create or get the existing file handler with the specified constraints.
    file_handler = create_file_handler(filename, level, max_lines, print_log_messages)
    if file_handler not in logger.handlers:
        # Only add the handler if it's not already attached to the logger.
        logger.addHandler(file_handler)

    return logger

# Example usage
if __name__ == "__main__":
    # Get a logger instance for 'my_logging_test.log', set to log ERROR and above, and limited to 100 lines.
    logger = get_logger('my_logging_test.log', logging.ERROR, 100, True)
    # Logging a message to demonstrate the
