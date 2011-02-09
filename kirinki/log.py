# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

# Python general imports
from logging import handlers
import logging

class Log:
    '''This class print a message in the application log file and, if it\'s needed, rotate the file.'''

    @staticmethod
    def getLogger():
        '''Method to configure the basic logger object.'''
        # Set up a specific logger with our desired output level
        logger = logging.getLogger('logger')
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler('/var/log/kirinki.log', maxBytes=20, backupCount=5)
        logger.addHandler(handler)

        return logger

    @staticmethod
    def debug(msg):
        # Get the logger.
        logger = Log.getLogger()
        
        # Log the message
        logger.setLevel(logging.DEBUG)
        logger.debug(msg)

    @staticmethod
    def info(msg):
        # Get the logger.
        logger = Log.getLogger()
        
        # Log the message
        logger.setLevel(logging.INFO)
        logger.info(msg)

    @staticmethod
    def warning(msg):
        # Get the logger.
        logger = Log.getLogger()
        
        # Log the message
        logger.setLevel(logging.WARNING)
        logger.warning(msg)
        
    @staticmethod
    def error(msg):
        # Get the logger.
        logger = Log.getLogger()
        
        # Log the message
        logger.setLevel(logging.ERROR)
        logger.error(msg)
        
    @staticmethod
    def critical(msg):
        # Get the logger.
        logger = Log.getLogger()
        
        # Log the message
        logger.setLevel(logging.CRITICAL)
        logger.critical(msg)
