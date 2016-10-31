# Wrapper around pythons logging library to make the main api code look
# cleaner. Only two handlers supported for now.

from logging import Formatter, getLogger, DEBUG, WARN, INFO, CRITICAL
from logging.handlers import SysLogHandler, RotatingFileHandler

class Logger(object):

    # Take a RawConfigParser object as argument.
    def __init__(self, config):
        log_levels = {
            'info': INFO,
            'warning': WARN,
            'critical': CRITICAL,
            'debug': DEBUG
        }

        # Setup formatter and logger name
        formatter = Formatter(config.get('logging', 'log_format'))
        l = getLogger(config.get('logging', 'log_name'))

        if config.get('logging', 'log_handler') == 'syslog':
            syslog_address = config.get('logging', 'syslog_address')

            if syslog_address.startswith('/'):
                h = SysLogHandler(
                    address=syslog_address,
                    facility=SysLogHandler.LOG_LOCAL0
                )
            else:
                h = SysLogHandler(
                    address=(
                        config.get('logging', 'syslog_address'),
                        config.get('logging', 'syslog_port')
                    ),
                    facility=SysLogHandler.LOG_LOCAL0
                )
        else:
            h = RotatingFileHandler(
                config.get('logging', 'log_file'),
                maxBytes=config.getint('logging', 'log_max_bytes'),
                backupCount=config.getint('logging', 'log_max_copies')
            )

        # Set the formatter to the handler
        h.setFormatter(formatter)
        l.addHandler(h)

        # Set log level from a hash of available levels
        try:
            l.setLevel(log_levels[config.get('logging', 'log_level')])
        except KeyError as e:
            l.error(('Failed to set log level, please select one of '
                     '{keys}').format(
                         keys=log_levels.keys()
                     )
                   )
            l.setLevel(DEBUG)

        # Finally expose some of the logging methods as a shorthand
        self.l = l
        self.debug = l.debug
        self.info = l.info
        self.warn = l.warn
        self.error = l.error
        self.critical = l.critical
        self.exception = l.exception

