"""
=====================
Geo Livestock Exports
=====================
This module contains the `Exports` class designed to calculate exports of milk, protein, and total protein from a 
livestock system under different scenarios. It interfaces with the `Exports` functionality from the `livestock_generation.livestock_exports` 
module to perform the calculations.

The `Exports` class utilizes methods to calculate the total kilograms of milk exported for each scenario, the total beef weight exported 
from the entire system for each scenario, and the total protein exported by the entire system, assuming specific milk and beef protein contents.
"""
from livestock_generation.livestock_exports import Exports as LivestockExports
    
class Exports:
    """
    Facilitates the calculation of exports of milk, protein, and total protein from a livestock system under different scenarios 
    by interfacing with the LivestockExports class.
    
    Attributes:
        exports_class (LivestockExports): An instance of the LivestockExports class for conducting the actual export calculations.
    
    Args:
        ef_country (str): The country code for which the exports are being calculated.
        calibration_year (int): The year used for calibration purposes in the analysis.
        target_year (int): The year for which the exports are being calculated.
        scenario_inputs_df (DataFrame): A pandas DataFrame containing scenario inputs necessary for calculations.
    """
    def __init__(self,ef_country, calibration_year, target_year, scenario_inputs_df):
        self.exports_class = LivestockExports(ef_country, calibration_year, target_year, scenario_inputs_df)


    def compute_system_milk_exports(self, scenario_animal_data, baseline_animal_data):
        """
        Calculates the total kilograms of milk exported for each scenario.

        Args:
            scenario_animal_data (DataFrame): Animal data for different scenarios.
            baseline_animal_data (DataFrame): Baseline animal data.
        
        Returns:
            DataFrame: A DataFrame with index as scenarios and columns for total milk in kg.
        """

        return self.exports_class.compute_system_milk_exports(scenario_animal_data, baseline_animal_data)
    

    def compute_system_protien_exports(self, scenario_animal_data, baseline_animal_data):
        """
        Calculates the total beef weight exported from the entire system for each scenario.

        Args:
            scenario_animal_data (DataFrame): Animal data for different scenarios.
            baseline_animal_data (DataFrame): Baseline animal data.
        
        Returns:
            DataFrame: A DataFrame with index as scenarios and columns for carcass weight in kg and by beef systems.
        """
        return self.exports_class.compute_system_protien_exports(scenario_animal_data, baseline_animal_data)


    def compute_system_total_protein_exports(self, scenario_animal_data, baseline_animal_data):
        """
        Calculates the total protein exported by the entire system, assuming specific milk and beef protein contents.

        Args:
            scenario_animal_data (DataFrame): Animal data for different scenarios.
            baseline_animal_data (DataFrame): Baseline animal data.
        
        Returns:
            DataFrame: A DataFrame with index as scenarios and columns for total protein, milk protein, and beef protein in kg.
        """
        return self.exports_class.compute_system_total_protein_exports(scenario_animal_data, baseline_animal_data)
