"""
=========================
ScenarioDataFetcher Module
=========================
This module contains the ScenarioDataFetcher class, which is responsible for fetching and manipulating scenario data from a pandas DataFrame.

"""

class ScenarioDataFetcher:
    """
    A class for fetching and manipulating scenario data from a pandas DataFrame.

    Attributes:
        scenario_data (pd.DataFrame): A pandas DataFrame containing scenario data.

    Methods:
        get_scenario_dataframe(): Returns the entire scenario data DataFrame.
        get_catchment_name(): Returns the unique catchment name from the scenario data.
        get_scenario_list(): Returns a list of unique scenarios present in the scenario data.
    """

    def __init__(self, scenario_data):
        """
        Constructs all the necessary attributes for the ScenarioDataFetcher object.

        Parameters:
            scenario_data (pd.DataFrame): The scenario data as a pandas DataFrame.
        """
        self.scenario_data = scenario_data


    def get_scenario_dataframe(self):
        """
        Returns the entire scenario data DataFrame.

        Returns:
            pd.DataFrame: The scenario data.
        """
        return self.scenario_data
    

    def get_catchment_name(self):
        """
        Returns the unique catchment name from the scenario data.

        Returns:
            str: The unique catchment name.
        """
        return self.scenario_data["Catchment"].unique().item()
    

    def get_scenario_list(self):
        """
        Returns a list of unique scenarios present in the scenario data.

        Returns:
            List[str]: A list of unique scenario names.
        """
        return self.scenario_data["Scenarios"].unique().tolist()
    