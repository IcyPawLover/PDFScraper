import configparser
import os
import logging 

from .logging_handler import get_logger 

class ConfigHandler:
    def __init__(self, config_file_path, logger):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.logger = logger  # Use the passed logger

        # Load existing config file if it exists, or create a new one
        if os.path.exists(config_file_path):
            self.config.read(config_file_path)
            self.logger.debug(f"ConfigHandler: Loaded configuration from {config_file_path}")
        else:
            with open(config_file_path, 'w') as config_file:
                self.config.write(config_file)
                self.logger.debug(f"ConfigHandler: Created new configuration file at {config_file_path}")

    def read_config(self, section, option):
        """Read a value from the config file."""
        try:
            value = self.config.get(section, option)
            self.logger.debug(f"ConfigHandler: Read [{section}] {option} = {value}")
            return value
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            self.logger.debug(f"ConfigHandler: Failed to read [{section}] {option}: {e}")
            raise

    def write_config(self, section, option, value):
        """Write a value to the config file."""
        if not self.config.has_section(section):
            self.config.add_section(section)
            self.logger.debug(f"ConfigHandler: Added new section [{section}]")
        self.config.set(section, option, value)
        with open(self.config_file_path, 'w') as config_file:
            self.config.write(config_file)
            self.logger.debug(f"ConfigHandler: Wrote [{section}] {option} = {value}")

    def update_config(self, section, option, value):
        """Update a value in the config file."""
        self.write_config(section, option, value)
        self.logger.debug(f"ConfigHandler: Updated config [{section}] {option} = {value}")

    def delete_option(self, section, option):
        """Delete an option from the config file."""
        if self.config.has_option(section, option):
            self.config.remove_option(section, option)
            with open(self.config_file_path, 'w') as config_file:
                self.config.write(config_file)
                self.logger.debug(f"ConfigHandler: Deleted option [{section}] {option}")

    def delete_section(self, section):
        """Delete a whole section from the config file."""
        if self.config.has_section(section):
            self.config.remove_section(section)
            with open(self.config_file_path, 'w') as config_file:
                self.config.write(config_file)
                self.logger.debug(f"ConfigHandler: Deleted section [{section}]")

def get_config(filename, logger):
    """
    Returns a logger with the given name. setup_logging must be called before getting a logger.

    :param filename: Name of the config file to read
    :param logger: The logging handler used to output any log messages
    :return: ConfigHandler instance with the configuration object.
    """
    return ConfigHandler(filename, logger)

if __name__ == "__main__":

    # Initialize the logger
    logger = get_logger('my_config_test.log', logging_level=logging.DEBUG)

    # Create a ConfigHandler instance, passing the logger as a parameter
    config_handler = get_config('example.ini', logger)

    # Example: Write some settings to the configuration file
    config_handler.write_config('UserSettings', 'theme', 'dark')
    config_handler.write_config('UserSettings', 'fontSize', '12')

    # Example: Read and log a setting
    theme = config_handler.read_config('UserSettings', 'theme')
    logger.info(f"ConfigHandler Example: Theme = {theme}")

    # Example: Update a setting
    config_handler.update_config('UserSettings', 'fontSize', '14')

    # Example: Delete an option
    config_handler.delete_option('UserSettings', 'theme')

    # Output updated settings to demonstrate the changes
    fontSize = config_handler.read_config('UserSettings', 'fontSize')
    logger.info(f"ConfigHandler Example: Updated FontSize = {fontSize}")

	# this section is not found and throws an Exception
    secret = config_handler.read_config('SectionNotFound', 'secretInfo')
