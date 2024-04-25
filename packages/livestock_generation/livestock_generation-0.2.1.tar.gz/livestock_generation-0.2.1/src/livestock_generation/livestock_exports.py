"""
=====================
Livestock Exports
=====================
This module contains a class to calculate exports of milk, protein, and total protein from a livestock system under different scenarios.

The class `Exports` contains methods to calculate the total kilograms of milk exported for each scenario, the total beef weight exported 
from the entire system for each scenario, and the total protein exported by the entire system, assuming specific milk and beef protein contents.

"""
import pandas as pd
from livestock_generation.resource_manager.livestock_data_manager import DataManager
from livestock_generation.resource_manager.scenario_fetcher import ScenarioDataFetcher
from livestock_generation.resource_manager.data_loader import Loader


    
class Exports:
    """
    A class to calculate exports of milk, protein, and total protein from a livestock system under different scenarios.
    
    Attributes:
        sc_class (ScenarioDataFetcher): An instance for fetching scenario data.
        loader_class (Loader): An instance for loading necessary data.
        data_manager_class (DataManager): An instance for managing livestock data.
        ef_country (str): The country code for export calculations.
    
    Args:
        ef_country (str): The country code for which the exports are being calculated.
        calibration_year (int): The year used for calibration purposes in the analysis.
        target_year (int): The year for which the exports are being calculated.
        scenario_inputs_df (DataFrame): A pandas DataFrame containing scenario inputs necessary for calculations.
    """
    def __init__(self,ef_country, calibration_year, target_year, scenario_inputs_df):
        self.sc_class = ScenarioDataFetcher(scenario_inputs_df)
        self.loader_class = Loader(ef_country)
        self.data_manager_class = DataManager(ef_country, calibration_year, target_year)
        self.ef_country = ef_country


    def compute_system_milk_exports(self, scenario_animal_data, baseline_animal_data):
        """
        Calculates the total kilograms of milk exported for each scenario.

        Args:
            scenario_animal_data (DataFrame): Animal data for different scenarios.
            baseline_animal_data (DataFrame): Baseline animal data.
        
        Returns:
            DataFrame: A DataFrame with index as scenarios and columns for total milk in kg.
        """
        df_index = list(baseline_animal_data.Scenarios.unique())
        df_index.extend(scenario_animal_data.Scenarios.unique())
        sc_herd_dataframe = pd.concat([scenario_animal_data, baseline_animal_data], ignore_index=True)


        milk_system_export = pd.DataFrame(
            index=df_index,
            columns=["Scenarios", "total_milk_kg"],
        )

        for sc in milk_system_export.index:

            mask = (
                (sc_herd_dataframe["cohort"] == "dairy_cows")
                & (sc_herd_dataframe["Scenarios"] == sc)
                & (sc_herd_dataframe["pop"] != 0)
            )

            milk_system_export.loc[sc, "total_milk_kg"] = (
                sc_herd_dataframe.loc[mask, "daily_milk"].values[0]
                * sc_herd_dataframe.loc[mask, "pop"].values[0]
                * 365
            )
            milk_system_export.loc[sc, "Scenarios"] = sc

        return milk_system_export

    def compute_system_protien_exports(self, scenario_animal_data, baseline_animal_data):
        """
        Calculates the total beef weight exported from the entire system for each scenario.

        Args:
            scenario_animal_data (DataFrame): Animal data for different scenarios.
            baseline_animal_data (DataFrame): Baseline animal data.
        
        Returns:
            DataFrame: A DataFrame with index as scenarios and columns for carcass weight in kg and by beef systems.
        """

        df_index = list(baseline_animal_data.Scenarios.unique())
        df_index.extend(scenario_animal_data.Scenarios.unique())
        sc_herd_dataframe = pd.concat([scenario_animal_data, baseline_animal_data], ignore_index=True)

        weight_gain_cattle = self.loader_class.weight_gain_cattle()
        carcass_weight_as_prop_of_LW = self.data_manager_class.carcass_weight_as_prop_of_LW
        export_weight_keys = self.data_manager_class.EXPORT_WEIGHT_KEYS
        ef_country = self.ef_country
        beef_systems = ["DxD_m", "DxD_f", "DxB_m", "DxB_f", "BxB_m", "BxB_f"]

        weight_df = pd.DataFrame(
            index=df_index,
            columns=["Scenarios", "carcass_weight_kg"] + beef_systems
        )


        for sc in weight_df.index:
            sc_weight = 0
            accumulated_weights = {beef_system: 0 for beef_system in beef_systems}
            herd_slice = sc_herd_dataframe[sc_herd_dataframe["Scenarios"] == sc]

            for beef_system in beef_systems:

                for i in herd_slice.index:

                    if herd_slice.loc[i, "cohort"] in export_weight_keys[beef_system]["Pop_Cohort"]:

                        population = sc_herd_dataframe.loc[i, "pop"]

                        if population != 0:

                            birth_weight = weight_gain_cattle.loc[ef_country, "birth_weight"]

                            wg_calves_lookup = export_weight_keys[beef_system]["Calf_LWG"]
                            weight_gain_calves = weight_gain_cattle.loc[ef_country, wg_calves_lookup]

                            wg_heifers_steers_less_2_year_lookup = export_weight_keys[beef_system]["Steer_Heifer_less_2_LWG"]
                            weight_gain_steers_heifers_less_2_year = weight_gain_cattle.loc[ef_country, wg_heifers_steers_less_2_year_lookup]

                            wg_heifers_steers_more_2_year_lookup = export_weight_keys[beef_system]["Steer_Heifer_more_2_LWG"]
                            weight_gain_steers_heifers_more_2_year = weight_gain_cattle.loc[ef_country, wg_heifers_steers_more_2_year_lookup]

                            sc_weight += (birth_weight + weight_gain_calves * 365 + \
                                         weight_gain_steers_heifers_less_2_year * 365 + \
                                         weight_gain_steers_heifers_more_2_year * 365) * population

                            accumulated_weights[beef_system] += (birth_weight + weight_gain_calves * 365 + \
                                         weight_gain_steers_heifers_less_2_year * 365 + \
                                         weight_gain_steers_heifers_more_2_year * 365) * population

            weight_df.loc[sc, "Scenarios"] = sc

            weight_df.loc[sc, "carcass_weight_kg"] = sc_weight * carcass_weight_as_prop_of_LW

            for beef_system in beef_systems:
                weight_df.loc[sc, beef_system] = accumulated_weights[beef_system] * carcass_weight_as_prop_of_LW

        return weight_df


    def compute_system_total_protein_exports(self, scenario_animal_data, baseline_animal_data):
        """
        Calculates the total protein exported by the entire system, assuming specific milk and beef protein contents.

        Args:
            scenario_animal_data (DataFrame): Animal data for different scenarios.
            baseline_animal_data (DataFrame): Baseline animal data.
        
        Returns:
            DataFrame: A DataFrame with index as scenarios and columns for total protein, milk protein, and beef protein in kg.
        """
        df_index = list(baseline_animal_data.Scenarios.unique())
        df_index.extend(scenario_animal_data.Scenarios.unique())

        milk_protein_content = self.data_manager_class.milk_protein_content
        beef_protein_content = self.data_manager_class.beef_protein_content

        protein_system_export = pd.DataFrame(
            index=df_index,
            columns=["total_protein", "milk_protein", "beef_protein"])

        for sc in protein_system_export.index:

            milk_output = self.compute_system_milk_exports(scenario_animal_data,baseline_animal_data)
            beef_output = self.compute_system_protien_exports(scenario_animal_data,baseline_animal_data)

            protein_system_export.loc[sc, "milk_protein"] = milk_output.loc[sc, "total_milk_kg"] * milk_protein_content
            protein_system_export.loc[sc, "beef_protein"] = beef_output.loc[sc, "carcass_weight_kg"] * beef_protein_content

            protein_system_export.loc[sc, "total_protein"] = protein_system_export.loc[sc, "milk_protein"] + protein_system_export.loc[sc, "beef_protein"]


        return protein_system_export
