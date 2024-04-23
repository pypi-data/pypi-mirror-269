"""configuration.py"""
import configparser
from utils.logger import CustomLogger


class Configuration:
    """
    Database configuration
    """

    def __init__(self, config_file='dataflow.cfg'):

        self.logger = CustomLogger().get_logger()
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_file)

            #Database Url
            self.database_url = self.config.get('database', 'database_url')

            #Echo
            self.echo = self.config.getboolean('database', 'echo', fallback=False)

            #pool_size
            self.pool_size = self.config.getint('database', 'pool_size', fallback=5)

            #max_overflow
            self.max_overflow = self.config.getint('database', 'max_overflow', fallback=10)

            #server host
            self.server_host = self.config.get('server', 'host', fallback="0.0.0.0")

            #server_port
            self.server_port = self.config.getint('server', 'port', fallback=8000)

            #reload
            self.reload = self.config.getboolean('server', 'reload', fallback=True)

        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            self.logger.error("Error reading configuration from %s : %s",self.config_file,e)
            self.logger.info("Using default configuration values.")

            #Database URL
            self.database_url = 'sqlite:///data/backend.db'

            #Echo
            self.echo = False

            #Pool_size
            self.pool_size = 5

            #Max Overflow
            self.max_overflow = 10

            #Server Host
            self.server_host = "0.0.0.0"

            #Server Port
            self.server_port = 8000

            #Reload
            self.reload = False

        except Exception as e:
            self.logger.exception("An unexpected error occurred while reading configuration: %s",e)
            raise e


    def track_changes(self):
        """
        Module to track the changes
        """

        self.logger.info("Tracking changes from default settings:")
        self.logger.info("Database URL: %s", self.database_url)
        self.logger.info("Echo: %s", self.echo)
        self.logger.info("Pool Size: %s", self.pool_size)
        self.logger.info("Max Overflow: %s", self.max_overflow)
        self.logger.info("Server Host: %s", self.server_host)
        self.logger.info("Server Port: %s", self.server_port)
        self.logger.info("Reload: %s", self.reload)


Configuration().track_changes()
