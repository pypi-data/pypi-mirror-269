"""
================
Database Manager
================

This module provides a class to manage and retrieve data from a SQLite database for livestock management purposes.
It provides methods to access data related to animal concentrate requirements, weight gain, herd numbers, and other parameters specific to a country.
"""

import sqlalchemy as sqa
import pandas as pd
from livestock_generation.database import get_local_dir
import os


class DataManager:
    """
    A class to manage and retrieve data from a SQLite database for livestock management purposes. 
    It provides methods to access data related to animal concentrate requirements, weight gain, herd numbers, 
    and other parameters specific to a country.
    
    Attributes:
        database_dir (str): Directory where the database file is located.
        engine (sqa.engine.Engine): SQLAlchemy engine object for database connection.
    """
    def __init__(self):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()

    def data_engine_creater(self):
        """
        Creates and returns a SQLAlchemy engine object connected to the livestock database.
        
        Returns:
            sqa.engine.Engine: SQLAlchemy engine for the livestock database.
        """
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "livestock_database.db")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)
    

    def get_concentrate_per_animal_dataframe(self, ef_country):
        """
        Retrieves a DataFrame with concentrate requirements per animal for the specified country.
        
        Args:
            ef_country (str): The country code to filter the data.
            
        Returns:
            pd.DataFrame: DataFrame with concentrate requirements per animal.
        """
        table = "concentrate_amounts_per_unit_output"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )

        return dataframe


    def get_weight_gain_cattle(self, ef_country):
        """
        Retrieves a DataFrame with weight gain data for cattle specific to the ef_country.
        
        Args:
            ef_country (str): The country code to filter the data.
            
        Returns:
            pd.DataFrame: DataFrame containing weight gain data for cattle.
        """
        table = "animal_features_data"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )

        return dataframe
    

    def get_weight_gain_sheep(self, ef_country):
        """
        Retrieves a DataFrame with weight gain data for sheep specific to the ef_country.
        
        Args:
            ef_country (str): The country code to filter the data.
            
        Returns:
            pd.DataFrame: DataFrame containing weight gain data for sheep.
        """
        table = "sheep_animal_features_data"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )

        return dataframe
    
    
    def get_cattle_herd_data(self):
        """
        Retrieves a DataFrame with cattle herd numbers, not specific to any country.
        
        Returns:
            pd.DataFrame: DataFrame containing cattle herd numbers.
        """
        table = "2012_to_2020_herd_numbers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        dataframe.iloc[: ,1:] *= 1000
        
        return dataframe


    def get_parameter_data(self, ef_country):
        """
        Retrieves a DataFrame with various parameters relevant to livestock management for the specified country.
        
        Args:
            ef_country (str): The country code to filter the data.
            
        Returns:
            pd.DataFrame: DataFrame containing various parameters relevant to livestock management.
        """
        table = "param_data"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, ef_country),
            self.engine,
            index_col=["ef_country"],
        )


        return dataframe