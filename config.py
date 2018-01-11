"""Loads configuration (mostly directory locations) from disk or
environment variables. Can set configuration for testing purposes."""

import os

import yaml


DEFAULT_CONFIG_FILE = '~/config/shepherd.yaml'
SHEPHERD_CONFIG_FILE = 'SHEPHERD_CONFIG_FILE'
REQUIRED_CONFIG_KEYS = 'pm_root sub_root'.split()


def get_config(config_path=None):
    """Return an object with all the configuration."""
    if config_path:
        config_yaml_path = config_path
    elif SHEPHERD_CONFIG_FILE in os.environ:
        config_yaml_path = os.environ[SHEPHERD_CONFIG_FILE]
    else:
        config_yaml_path = DEFAULT_CONFIG_FILE
    config = Config(config_yaml_path)
    return config


class Config:
    def __init__(self, config_yaml_path):
        with open(config_yaml_path) as fin:
            config_data = yaml.load(fin)
        missing = set(REQUIRED_CONFIG_KEYS) - set(config_data)
        if missing:
            raise ConfigError('Missing: {}'.format(sorted(missing)))
        self.__dict__.update(config_data)


class ConfigError(Exception):
    """Some configuration data is missing."""
