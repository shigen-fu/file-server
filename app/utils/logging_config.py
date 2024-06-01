import logging


def configure_logging(logging_config):
    logging.basicConfig(
        level=logging_config['level'], format=logging_config['format'])
    logging.getLogger().setLevel(logging_config['level'])
