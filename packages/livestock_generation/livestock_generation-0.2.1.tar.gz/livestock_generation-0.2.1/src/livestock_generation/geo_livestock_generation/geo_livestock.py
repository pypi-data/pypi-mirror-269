"""
===============================
Geo Livestock Generation Module
===============================

This module is responsible for generating geographic-specific livestock data,
including the management of cohorts, animal data calculations, and scenario-based
projections for agricultural systems. It utilizes various data sources and
models to compute exports, productivity, and sustainability metrics for livestock
production under different environmental and management scenarios.
"""
from livestock_generation.resource_manager.data_loader import Loader
from livestock_generation.resource_manager.livestock_data_manager import DataManager
from livestock_generation.resource_manager.scenario_fetcher import ScenarioDataFetcher
from catchment_data_api.cohorts import Cohorts as CatchmentCohorts
import pandas as pd
import numpy as np

    
class Cohorts:
    """
    A class for managing cohorts within a livestock system. It generates dictionaries
    for cohorts and baseline cohorts, handles name conversions, and computes population
    coefficients and population in scenarios for a given year.
    
    Attributes:
        sc_class (ScenarioDataFetcher): Instance for fetching scenario data.
        loader_class (Loader): Instance for loading necessary data.
        data_manager_class (DataManager): Instance for managing livestock data.
        calibration_year (int): Calibration year for the analysis.
    """
    def __init__(self, ef_country, calibration_year, target_year, scenario_inputs_df):
        self.sc_class = ScenarioDataFetcher(scenario_inputs_df)
        self.scenario_inputs_df = self.sc_class.get_scenario_dataframe()
        self.loader_class = Loader(ef_country)
        self.data_manager_class = DataManager(ef_country, calibration_year, target_year)
        self.calibration_year = calibration_year


    def generate_cohorts_dictionary(self):
        """
        Generates a dictionary of cohorts from cattle herd data with aggregated values.
        
        Returns:
            dict: A dictionary with cohort names as keys and aggregated data as values.
        """
        data_frame = self.loader_class.cattle_herd_data()

        cohort_output = {}

        for _, row in data_frame.iterrows():

            cohort = row.get(str("Cohorts"))

            if cohort not in cohort_output.keys():

                cohort_output[cohort] = (
                    row[1:] 
                )

            else:

                cohort_output[cohort] += (
                    row[1:] 
                )
    
        return cohort_output


    def generate_baseline_cohorts_dictionary(self):
        """
        Generates a baseline dictionary of cohorts using the calibration year or a default
        if data for the calibration year is not available.
        
        Returns:
            dict: A dictionary with cohort names as keys and population data as values for the baseline year.
        """
        calibration_year = str(self.calibration_year)
        default_calibration_year = str(self.data_manager_class.default_calibration_year)

        data_frame = self.loader_class.cattle_herd_data()
        cohort_output = {}

        for _, row in data_frame.iterrows():
            cohort = row.get(str("Cohorts"))

            try:
                cohort_output[cohort] = row[calibration_year]
            except KeyError:
                cohort_output[cohort] = row[default_calibration_year]

        return cohort_output

        
    def cohort_name_conversion(self, df):
        """
        Converts the cohort names in a DataFrame according to a predefined conversion dictionary.
        
        Args:
            df (pd.DataFrame): The DataFrame with cohort names to be converted.
        
        Returns:
            pd.DataFrame: The DataFrame with converted cohort names.
        """
        column_name_dict = self.data_manager_class.cohort_name_conversion_dict

        df = df.rename(columns=column_name_dict)
    
        return df


    def compute_coef_cohort_population(self):
        """
        Computes the coefficients for cohort populations based on the relationship of individual cohorts
        to the total population of beef and dairy adults.
        
        Returns:
            dict: A dictionary with cohort names as keys and their population coefficients as values.
        """
        cohort_dict = self.generate_baseline_cohorts_dictionary()

        coef ={}

        herd_relation_dict = self.data_manager_class.HERD_RELATION
        systems = self.data_manager_class.systems

        for sys in systems:   
            for cohort in herd_relation_dict[sys].keys():

                coef[cohort] = cohort_dict[cohort] / np.sum(
                    [cohort_dict[i] for i in herd_relation_dict[sys][cohort]], axis=0
                )
    
        return coef
    

    def compute_cohort_population_in_scenarios_for_year(self):
        """
        Computes the cohort populations for each scenario in the target year, adjusting for
        different animal systems and their relationships.
        
        Returns:
            pd.DataFrame: A DataFrame with cohort populations for each scenario.
        """
        cohort_list =[]
        cohort_list.extend(self.data_manager_class.COHORTS_DICT["Cattle"])
        cohort_list.extend(self.data_manager_class.COHORTS_DICT["Sheep"])

        herd_relation_dict = self.data_manager_class.HERD_RELATION
        systems = self.data_manager_class.systems
        
        scenario_df = self.cohort_name_conversion(self.scenario_inputs_df)

        scenario_herd = pd.DataFrame(columns=cohort_list)
        
        coef =self.compute_coef_cohort_population()

        for sys in systems:
            for cohort in cohort_list:
                try:
                    if cohort in herd_relation_dict[sys].keys():
                        
                        scenario_herd[cohort] = np.sum(
                            [
                                np.mean(coef[cohort]) * scenario_df[i]
                                for i in herd_relation_dict[sys][cohort]
                            ],
                            axis=0,
                        )

                    else:
                        
                        scenario_herd[cohort] = scenario_df[cohort]
                except KeyError:
                    continue
   
            
        scenario_herd["Scenarios"] = scenario_df["Scenarios"]
            
        return scenario_herd
    

    

class AnimalData:
    """
    A class for managing animal data within a livestock system. It handles the creation of
    animal data DataFrames for different scenarios and baseline conditions.
    
    Attributes:
        cohorts_class (Cohorts): Instance of Cohorts class for cohort management.
        catchment (str): The catchment name obtained from scenario data.
        cohorts_api_class (CatchmentCohorts): Instance of CatchmentCohorts class for catchment data.
    """
    def __init__(self, ef_country, calibration_year, target_year, scenario_inputs_df):

        self.sc_class = ScenarioDataFetcher(scenario_inputs_df)
        self.scenario_inputs_df = self.sc_class.get_scenario_dataframe()
        self.loader_class = Loader(ef_country)
        self.data_manager_class = DataManager(ef_country, calibration_year, target_year)
        self.cohorts_class = Cohorts(ef_country, calibration_year, target_year, scenario_inputs_df)
        self.catchment = self.sc_class.get_catchment_name()
        self.cohorts_api_class = CatchmentCohorts(self.catchment)
        self.target_year = target_year
        self.calibration_year = calibration_year
        self.ef_country = ef_country


    def get_element_from_productivity(self,
        lca_parameter_name,
        goblin_parameter_name,
        coef_for_parameter_from_scenario,
    ):
        """
        Retrieves a specific parameter related to animal productivity, adjusted by a coefficient.
        
        Args:
            lca_parameter_name (str): The name of the LCA parameter to retrieve.
            goblin_parameter_name (str): The name of the Goblin parameter to match.
            coef_for_parameter_from_scenario (float): The coefficient to adjust the parameter value.
        
        Returns:
            float: The adjusted parameter value.
        """
        parameter_data_base = self.loader_class.parameter_data()

        lca_parameter_mask = parameter_data_base["LCAparameter"] == lca_parameter_name
        goblin_parameter_mask = parameter_data_base["Goblinparameter"].str.contains(
            goblin_parameter_name
        )

        parameter_output = (
            float(
                parameter_data_base.loc[
                    lca_parameter_mask & goblin_parameter_mask, "Min"
                ].item()
            )
            + (
                float(
                    parameter_data_base.loc[
                        lca_parameter_mask & goblin_parameter_mask, "Max"
                    ].item()
                )
                - float(
                    parameter_data_base.loc[
                        lca_parameter_mask & goblin_parameter_mask, "Min"
                    ].item()
                )
            )
            * coef_for_parameter_from_scenario
        )

        return parameter_output


    def compute_concentrate(self, cohort, milk, weight):
        """
        Computes the concentrate requirement for a given cohort based on milk production and weight.
        
        Args:
            cohort (str): The cohort for which to compute concentrate.
            milk (float): The milk production value.
            weight (float): The weight of the animals in the cohort.
        
        Returns:
            float: The concentrate requirement.
        """
        con_dict = self.data_manager_class.COHORTS_CONCENTRATE
        df = self.loader_class.concentrate_per_animal_dataframe()
        ef_country = self.ef_country

        if cohort == "dairy_cows":
            return milk * df.loc[ef_country, "dairy_kg_con_per_kg_milk"]

        if cohort in con_dict["FEED"]:
            return 1

        if cohort in con_dict["NO_FEED"]:
            return 0

        return df.loc[ef_country, "total_dry_cow_concentrate_kg_per_LU"] / weight

    

    def create_animal_dataframe(self):
        """
        Creates a DataFrame containing detailed animal data for each scenario.
        
        Returns:
            pd.DataFrame: A DataFrame with animal data for scenarios.
        """
        scenario_data_frame = self.scenario_inputs_df
        cohort_dict = self.data_manager_class.COHORTS_DICT
        cohort_name_dict = self.data_manager_class.COHORT_NAME_DICT
        target_year = self.target_year
        herd_data_frame = self.cohorts_class.compute_cohort_population_in_scenarios_for_year()

        weight_gain_cattle = self.loader_class.weight_gain_cattle()
        calf_weight_gains = self.data_manager_class.calf_weight_gain_lookup #Daniel
        steer_heifer_weight_gains = self.data_manager_class.steer_heifer_weight_gain_lookup #Daniel
        weight_gain_sheep = self.loader_class.weight_gain_sheep()

        sheep_system_dict = self.data_manager_class.sheep_system_dict

        cattle_cohort_time_indoors_2015 = self.data_manager_class.COHORT_TIME_INDOORS

        systems = self.data_manager_class.systems
        cattle_systems = self.data_manager_class.cattle_systems
        sheep_systems = self.data_manager_class.sheep_systems
        cohort_weight = self.data_manager_class.CATTLE_COHORT_WEIGHT

        productivity_mapping = self.data_manager_class.ANIMAL_SYSTEM_MAPPING 
        system_params = self.data_manager_class.system_parameters

        ef_country = self.ef_country


        data = pd.DataFrame()

        new_index = 0

        for animal_type in systems:

            if animal_type == "Cattle":
                animal_name_list = cattle_systems
            else:
                animal_name_list = sheep_systems

            index_to_mask = scenario_data_frame["Cattle systems"].isin(animal_name_list)

            for index, row in scenario_data_frame.loc[index_to_mask, :].iterrows():

                if row["Cattle systems"] in cattle_systems:
                    animal_type = "Cattle"
                elif "sheep" in row["Cattle systems"]:
                    animal_type = "Sheep"

                for animal_category in cohort_dict[animal_type]:
                    for animal_system, productivity in productivity_mapping.items():
                        if animal_system in row["Cattle systems"]:
                            animal_system_for_productivity = productivity
                            break

                    data.loc[new_index, "ef_country"] = ef_country
                    data.loc[new_index, "farm_id"] = int(index)
                    data.loc[new_index, "Scenarios"] = int(row["Scenarios"])
                    data.loc[new_index,"Catchment"] = row["Catchment"]
                    data.loc[new_index, "year"] = int(target_year)
                    data.loc[new_index, "cohort"] = cohort_name_dict[
                        animal_category
                    ]
                    data.loc[new_index, "pop"] = herd_data_frame.loc[
                        index, animal_category
                    ]

                    # Colm changed
                    if data.loc[new_index, "cohort"] == "dairy_cows":
                        data.loc[
                            new_index, "daily_milk"
                        ] = self.get_element_from_productivity(
                            "daily_milk",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ]
                        )
                    elif data.loc[new_index, "cohort"] == "suckler_cows":
                        data.loc[
                            new_index, "daily_milk"
                        ] = (
                            self.data_manager_class.suckler_daily_milk_baseline
                        )  # equates to 515 kg milk per year
                    else:
                        data.loc[new_index, "daily_milk"] = 0

                    if animal_type == "Cattle":
                        #Weights
                        weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                        weight_gain = weight_gain_cattle.loc[ef_country, weight_col]
                        age = cohort_weight[data.loc[new_index, "cohort"]]["age"]
                        genetics = cohort_weight[data.loc[new_index, "cohort"]]["genetics"]
                        gender = cohort_weight[data.loc[new_index, "cohort"]]["gender"]

                        if age == "mature":
                            weight = weight_gain

                        elif age == "calf":

                            weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + (weight_gain * 365) / 2

                        elif age == "less_than_2_yr":

                            weight_gain_calves = weight_gain_cattle.loc[ef_country, calf_weight_gains[(genetics, gender)]]
                            weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + weight_gain_calves * 365 + \
                                     (weight_gain * 365) / 2

                        elif age == "more_than_2_yr":

                            weight_gain_calves = weight_gain_cattle.loc[ef_country, calf_weight_gains[(genetics, gender)]]
                            weight_gain_steers_heifers = weight_gain_cattle.loc[ef_country, steer_heifer_weight_gains[(genetics, gender)]]
                            weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + weight_gain_calves * 365 + \
                                     weight_gain_steers_heifers * 365 + (weight_gain * 365) / 2

                        data.loc[new_index, "weight"] = weight



                    else:
                        weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                        weight_gain = weight_gain_sheep.loc[ef_country, weight_col]
                        if cohort_weight[data.loc[new_index, "cohort"]]["age"] == "mature":
                            weight = weight_gain
                        else: 
                            weight = weight_gain_sheep.loc[ef_country, "lamb_weight_at_birth"] + weight_gain

                        data.loc[new_index, "weight"] = weight



                    data.loc[new_index, "forage"] = system_params[animal_type]["forage"]

                    if animal_type == "Cattle":
                        data.loc[new_index, "grazing"] = system_params[animal_type]["grazing"]
                    else:
                        data.loc[new_index, "grazing"] = (
                            sheep_system_dict[animal_category.split(" ")[0]] + system_params[animal_type]["grazing"]
                        )
                    data.loc[new_index, "con_type"] = system_params[animal_type]["con_type"]

                    if animal_type == "Sheep":
                        data.loc[new_index, "con_amount"] = system_params[animal_type]["concentrate"]
                        data.loc[new_index, "wool"] = system_params[animal_type]["wool"]

                    elif animal_type == "Cattle":

                        con_amount = self.compute_concentrate(
                            data.loc[new_index, "cohort"],
                            data.loc[new_index, "daily_milk"],
                            data.loc[new_index, "weight"],
                        )
                        data.loc[new_index, "con_amount"] = con_amount
                        data.loc[new_index, "wool"] = 0

                    if animal_type == "Cattle":
                        if (
                            data.loc[new_index, "cohort"]
                            in cattle_cohort_time_indoors_2015["t_indoors"].keys()
                        ):
                            data.loc[
                                new_index, "t_outdoors"
                            ] = cattle_cohort_time_indoors_2015["t_outdoors"][
                                data.loc[new_index, "cohort"]
                            ]
                            data.loc[
                                new_index, "t_indoors"
                            ] = cattle_cohort_time_indoors_2015["t_indoors"][
                                data.loc[new_index, "cohort"]
                            ]
                            data.loc[new_index, "t_stabled"] = 0
                    else:
                        data.loc[
                            new_index, "t_outdoors"
                        ] = self.get_element_from_productivity(
                            "t_outdoors",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ],
                        )
                        data.loc[
                            new_index, "t_indoors"
                        ] = self.get_element_from_productivity(
                            "t_indoors",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ],
                        )
                        data.loc[
                            new_index, "t_stabled"
                        ] = self.get_element_from_productivity(
                            "t_stabled",
                            row["Cattle systems"],
                            scenario_data_frame.loc[
                                index, animal_system_for_productivity
                            ],
                        )

                    data.loc[new_index, "mm_storage"] = row.loc["Manure management"]
                    data.loc[new_index, "daily_spreading"] = system_params[animal_type]["daily_spread"]
                    data.loc[new_index, "n_sold"] = 0
                    data.loc[new_index, "n_bought"] = 0
                    
                    new_index += 1
        return data


    def create_baseline_animal_dataframe(self):
        """
        Creates a DataFrame containing detailed animal data for the baseline condition.
        
        Returns:
            pd.DataFrame: A DataFrame with baseline animal data.
        """
        cohort_dict = self.data_manager_class.COHORTS_DICT
        cohort_name_dict = self.data_manager_class.COHORT_NAME_DICT

        calibration_year = self.calibration_year
        herd_data_frame = self.cohorts_api_class.compute_cohort_population_in_catchment()

        weight_gain_cattle = self.loader_class.weight_gain_cattle()
        calf_weight_gains = self.data_manager_class.calf_weight_gain_lookup #Daniel
        steer_heifer_weight_gains = self.data_manager_class.steer_heifer_weight_gain_lookup #Daniel
        weight_gain_sheep = self.loader_class.weight_gain_sheep()

        sheep_system_dict = self.data_manager_class.sheep_system_dict

        cattle_cohort_time_indoors_2015 = self.data_manager_class.COHORT_TIME_INDOORS

        cohort_weight = self.data_manager_class.CATTLE_COHORT_WEIGHT

        system_params = self.data_manager_class.system_parameters

        ef_country = self.ef_country


        data = pd.DataFrame()

        new_index = 0

        for animal in herd_data_frame.columns:


            data.loc[new_index, "ef_country"] = ef_country
            data.loc[new_index, "farm_id"] = int(calibration_year)
            data.loc[new_index, "Scenarios"] = -1
            data.loc[new_index,"Catchment"] = self.catchment
            data.loc[new_index, "year"] = int(calibration_year)
            data.loc[new_index, "cohort"] = cohort_name_dict[animal]
            data.loc[new_index, "pop"] = herd_data_frame.loc[calibration_year,animal]
                    # Colm changed
            if data.loc[new_index, "cohort"] == "dairy_cows":
                data.loc[new_index, "daily_milk"] = self.data_manager_class.dairy_daily_milk_baseline
            elif data.loc[new_index, "cohort"] == "suckler_cows":
                data.loc[new_index, "daily_milk"] = self.data_manager_class.suckler_daily_milk_baseline
        
            else:
                data.loc[new_index, "daily_milk"] = 0

            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                #Weights
                weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                weight_gain = weight_gain_cattle.loc[ef_country, weight_col]
                age = cohort_weight[data.loc[new_index, "cohort"]]["age"]
                genetics = cohort_weight[data.loc[new_index, "cohort"]]["genetics"]
                gender = cohort_weight[data.loc[new_index, "cohort"]]["gender"]


                if age == "mature":
                    weight = weight_gain

                elif age == "calf":

                    weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + (weight_gain * 365) / 2

                elif age == "less_than_2_yr":

                    weight_gain_calves = weight_gain_cattle.loc[ef_country, calf_weight_gains[(genetics, gender)]]
                    weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + weight_gain_calves * 365 + \
                            (weight_gain * 365) / 2

                elif age == "more_than_2_yr":

                    weight_gain_calves = weight_gain_cattle.loc[ef_country, calf_weight_gains[(genetics, gender)]]
                    weight_gain_steers_heifers = weight_gain_cattle.loc[ef_country, steer_heifer_weight_gains[(genetics, gender)]]
                    weight = weight_gain_cattle.loc[ef_country, "birth_weight"] + weight_gain_calves * 365 + \
                            weight_gain_steers_heifers * 365 + (weight_gain * 365) / 2

                data.loc[new_index, "weight"] = weight

            else:
                weight_col = cohort_weight[data.loc[new_index, "cohort"]]["weight_column"]
                weight_gain = weight_gain_sheep.loc[ef_country, weight_col]
                if cohort_weight[data.loc[new_index, "cohort"]]["age"] == "mature":
                    weight = weight_gain
                else:
                    weight = weight_gain_sheep.loc[ef_country, "lamb_weight_at_birth"] + weight_gain

                data.loc[new_index, "weight"] = weight

            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                data.loc[new_index, "forage"] = system_params["Cattle"]["forage"]
                data.loc[new_index, "grazing"] = system_params["Cattle"]["grazing"]
                data.loc[new_index, "con_type"] = system_params["Cattle"]["con_type"]

            else:
                data.loc[new_index, "forage"] = system_params["Sheep"]["forage"]
                data.loc[new_index, "grazing"] = (
                            sheep_system_dict[animal.split(" ")[0]] + system_params["Sheep"]["grazing"]
                        )
                data.loc[new_index, "con_type"] = system_params["Sheep"]["con_type"]

            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:

                con_amount = self.compute_concentrate(
                    data.loc[new_index, "cohort"],
                    data.loc[new_index, "daily_milk"],
                    data.loc[new_index, "weight"],
                )

                data.loc[new_index, "con_amount"] = con_amount
                data.loc[new_index, "wool"] = 0

            else:
                
                data.loc[new_index, "con_amount"] = system_params["Sheep"]["concentrate"]
                data.loc[new_index, "wool"] = system_params["Sheep"]["wool"]



            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                if (
                    data.loc[new_index, "cohort"]
                    in cattle_cohort_time_indoors_2015["t_indoors"].keys()
                ):
                    data.loc[
                        new_index, "t_outdoors"
                    ] = cattle_cohort_time_indoors_2015["t_outdoors"][
                        data.loc[new_index, "cohort"]
                    ]
                    data.loc[
                        new_index, "t_indoors"
                    ] = cattle_cohort_time_indoors_2015["t_indoors"][
                        data.loc[new_index, "cohort"]
                    ]
                    data.loc[new_index, "t_stabled"] = 0
            else:
                data.loc[
                    new_index, "t_outdoors"
                ] = cattle_cohort_time_indoors_2015["t_outdoors"][
                        data.loc[new_index, "cohort"]]
                data.loc[
                    new_index, "t_indoors"
                ] = cattle_cohort_time_indoors_2015["t_indoors"][
                        data.loc[new_index, "cohort"]]
                data.loc[
                    new_index, "t_stabled"
                ] =0
                
            if data.loc[new_index, "cohort"] in cohort_dict["Cattle"]:
                    data.loc[new_index, "mm_storage"] = system_params["Cattle"]["baseline_manure_management"]
                    data.loc[new_index, "daily_spreading"] = system_params["Cattle"]["daily_spread"]
            else:
                data.loc[new_index, "mm_storage"] = system_params["Sheep"]["manure_management"]
                data.loc[new_index, "daily_spreading"] = system_params["Sheep"]["daily_spread"]
            
            data.loc[new_index, "n_sold"] = 0
            data.loc[new_index, "n_bought"] = 0

            new_index += 1

        return data


