"""
=====================
Data Loader Module
=====================
This module contains a class for loading data specific to livestock management, facilitating the retrieval
of various datasets necessary for calculations and analyses within the livestock domain.

The `Loader` class contains methods to retrieve a dataframe containing the concentrate requirements per animal specific to the ef_country,
a dataframe containing weight gain data for cattle specific to the ef_country, a dataframe containing weight gain data for sheep specific to the ef_country,
a dataframe containing cattle herd data, and a dataframe containing various parameters relevant to livestock management, filtered by the ef_country.
"""
from livestock_generation.resource_manager.database_manager import DataManager

class Loader:
    """
    A class for loading data specific to livestock management, facilitating the retrieval
    of various datasets necessary for calculations and analyses within the livestock domain.
    
    Attributes:
        dataframes (DataManager): An instance of DataManager for accessing the database.
        ef_country (str): The country code for which the data is being loaded, used to filter data.
    """
    def __init__(self, ef_country):
        self.dataframes = DataManager()
        self.ef_country = ef_country


    def concentrate_per_animal_dataframe(self):
        """
        Retrieves a dataframe containing the concentrate requirements per animal specific to the ef_country.
        
        Returns:
            DataFrame: A pandas DataFrame containing concentrate requirements per animal.
        """
        return self.dataframes.get_concentrate_per_animal_dataframe(self.ef_country)


    def weight_gain_cattle(self):
        """
        Retrieves a dataframe containing weight gain data for cattle specific to the ef_country.
        
        Returns:
            DataFrame: A pandas DataFrame containing weight gain data for cattle.
        """
        return self.dataframes.get_weight_gain_cattle(self.ef_country)
    

    def weight_gain_sheep(self):
        """
        Retrieves a dataframe containing weight gain data for sheep specific to the ef_country.
        
        Returns:
            DataFrame: A pandas DataFrame containing weight gain data for sheep.
        """
        return self.dataframes.get_weight_gain_sheep(self.ef_country)
    

    def cattle_herd_data(self):
        """
        Retrieves a dataframe containing cattle herd data.
        
        Returns:
            DataFrame: A pandas DataFrame containing cattle herd data.
        """
        return self.dataframes.get_cattle_herd_data()
    

    def parameter_data(self):
        """
        Retrieves a dataframe containing various parameters relevant to livestock management,
        filtered by the ef_country.
        
        Returns:
            DataFrame: A pandas DataFrame containing various parameters relevant to livestock management.
        """
        return self.dataframes.get_parameter_data(self.ef_country)
    

