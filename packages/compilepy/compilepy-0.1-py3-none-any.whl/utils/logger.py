"""logger.py"""
import logging
import os



class CustomLogger:
    """
    Custom logger class for configuring and using logging functionality.

    Attributes:
        log_directory (str): The directory where log files will be stored.
        log_file_path (str): The full path to the log file.
        logger (logging.Logger): The logger object for logging messages.
    """


    def __init__(self):
        """
        Initialize the CustomLogger instance and configure logging.

        Args:
            log_directory (str): The directory where log files will be stored.
            log_file_path (str): The full path to the log file.
        """
        self.root_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.log_directory = os.path.join(self.root_directory, "logs")
        self.log_file_path = os.path.join(self.log_directory, "logger.log")
        self.configure_logger()


    def configure_logger(self):
        """
        Configure the logger with necessary settings.
        """

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        # Create a file handler and set its logging level to DEBUG
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it to the file handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)


    def get_logger(self):
        """
        Retrieve the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """

        return self.logger
