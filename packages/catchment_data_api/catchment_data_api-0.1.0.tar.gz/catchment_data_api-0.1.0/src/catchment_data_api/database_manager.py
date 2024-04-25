"""
Database Manager Module
-----------------------

This module contains the DataManager class, which is responsible for managing database connections and queries for the catchment data API.
"""
import sqlalchemy as sqa
import pandas as pd
from catchment_data_api.database import get_local_dir
import os


class DataManager:
    """
    A class to manage database connections and queries for the catchment data API. 
    It provides methods to access environmental and agricultural data stored in 
    a SQLite database.

    Attributes:
        database_dir (str): The directory path where the database file is located.
        engine (sqa.engine.base.Engine): The SQLAlchemy engine instance for database connections.
    """
    def __init__(self):
        """
        Initializes the DataManager class, setting up the database directory and creating
        the database engine for SQLite connections.
        """
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()

    def data_engine_creater(self):
        """
        Creates a SQLAlchemy engine for connecting to the SQLite database.

        Returns:
            sqa.engine.base.Engine: An engine instance connected to the SQLite database.
        """
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "livestock_land_cover_database")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)
    
    def get_national_herd_raw(self):
        """
        Retrieves raw national herd numbers from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing raw national herd numbers, indexed by cohorts.
        """
        table = "2012_to_2020_herd_numbers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
            index_col=["Cohorts"]
        )

        dataframe.iloc[: ,1:] *= 1000

        return dataframe

    def get_catchment_livestock_data(self):
        """
        Retrieves livestock data for catchments from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing livestock data for various catchments.
        """
        table = "livestock_data_table"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )

        return dataframe
    

    def get_catchment_forest_data(self):
        """
        Retrieves forest data for catchments from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing forest data for various catchments.
        """
        table = "forest_database_table"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )

        return dataframe
    

    def get_catchment_grass_data(self):
        """
        Retrieves grassland data for catchments from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing grassland data for various catchments.
        """
        table = "grass_database_table"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )

        return dataframe
    

    def get_catchment_cultivated_data(self):
        """
        Retrieves cultivated land data for catchments from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing cultivated land data for various catchments.
        """        
        table = "cult_database_table"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )

        return dataframe
    

    def get_catchment_peat_data(self):
        """
        Retrieves peatland data for catchments from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing peatland data for various catchments.
        """
        table = "peat_database_table"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )

        return dataframe
    

    def get_catchment_lucas_data(self):
        """
        Retrieves LUCAS data for catchments from the database.

        Returns:
            pandas.DataFrame: A DataFrame containing LUCAS survey data for various catchments.
        """        
        table = "lucas_database_table"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )

        return dataframe