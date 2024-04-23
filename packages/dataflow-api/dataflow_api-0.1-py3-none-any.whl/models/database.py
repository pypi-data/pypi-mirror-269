"""database.py"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configuration import Configuration
from utils.logger import CustomLogger
from utils.exception import DatabaseConnectionError



class Database:
    """
    Class to establish database connection and manage database operations.
    """

    def __init__(self):
        """
        Initializes the Database class instance.
        """

        self.config = Configuration()
        self.logger = CustomLogger().get_logger()
        self.database_url = self.config.database_url
        self.engine = None


    def create_database_engine(self):
        """
        Creates and returns a database engine.

        Returns:
            engine: SQLAlchemy database engine.
        
        Raises:
            DatabaseConnectionError: If unable to create the database engine.
        """

        try:
            self.engine = create_engine(self.database_url)
            self.logger.info("Engine Created Successfully")
            return self.engine

        except (TypeError, AttributeError, SQLAlchemyError) as e:
            error_message = f"Failed to create database engine: {str(e)}"
            self.logger.error(error_message)
            raise DatabaseConnectionError(error_message) from e


    def create_sessionlocal(self):
        """
        Creates and returns a session local.

        Returns:
            SessionLocal: SQLAlchemy session local.
        
        Raises:
            DatabaseConnectionError: If unable to create the session local.
        """

        try:
            sessionlocal = sessionmaker(autocommit=False, autoflush=False,
                                        bind=self.engine or self.create_database_engine())
            self.logger.info("SessionLocal Created Successfully")
            return sessionlocal

        except SQLAlchemyError as e:
            error_message = f"Failed to create session: {str(e)}"
            self.logger.error(error_message)
            raise DatabaseConnectionError(error_message) from e


    def create_base(self):
        """
        Creates and returns a declarative base.

        Returns:
            Base: SQLAlchemy declarative base.
        """

        return declarative_base()
