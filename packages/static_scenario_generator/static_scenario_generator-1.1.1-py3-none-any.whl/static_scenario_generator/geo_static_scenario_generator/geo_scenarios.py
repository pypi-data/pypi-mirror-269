"""
====================================
Geo (Catchement) Scenario Generator
====================================
A module for generating scenario dataframes from configuration files.

This module supports loading scenarios from JSON or CSV files, processing
them into pandas DataFrames based on predefined common and animal-specific
columns and systems. It leverages the DataManager for accessing data schemas
and the CatchmentDataAPI for catchment-specific information.

"""

from static_scenario_generator.resource_manager.data_manager import DataManager
from catchment_data_api.catchment_data_api import CatchmentDataAPI
import pandas as pd
import json


class ScenarioGeneration:
    """
    A class for generating scenario dataframes from configuration files.

    This class supports loading scenarios from JSON or CSV files, processing
    them into pandas DataFrames based on predefined common and animal-specific
    columns and systems. It leverages the DataManager for accessing data schemas
    and the CatchmentDataAPI for catchment-specific information.

    Attributes:
        data_manager_class (DataManager): Instance of DataManager with catchment data.
        catchment_api (CatchmentDataAPI): Instance of CatchmentDataAPI for catchment data processing.
        common_columns (list): List of common column names.
        animal_columns (list): List of animal-specific column names.
        animal_systems (list): List of animal systems.
    """
    def __init__(self):
        self.data_manager_class = DataManager(catchment=True)
        self.catchment_api = CatchmentDataAPI()
        self.common_columns = self.data_manager_class.get_common_columns()
        self.animal_columns = self.data_manager_class.get_animal_columns()
        self.animal_systems = self.data_manager_class.get_systems()


    def generate_scenario_dataframe(self, path):
        """
        Generates a DataFrame from a scenario configuration file.

        The method detects the file type (JSON or CSV) and processes it
        accordingly to create a DataFrame with scenarios based on the
        configurations provided.

        Parameters:
            path (str): Path to the configuration file (JSON or CSV).

        Returns:
            pandas.DataFrame: DataFrame containing the processed scenario data.
        """
        if path.endswith(".json"):
            print("JSON file detected")
            config =self.json_load(path)

        elif path.endswith(".csv"):
            print("CSV file detected")
            config= self.csv_load(path)

        return config


    def json_load(self, path):
        """
        Loads and processes a scenario configuration from a JSON file.

        Parameters:
            path (str): Path to the JSON configuration file.

        Returns:
            pandas.DataFrame: DataFrame containing the processed scenario data from the JSON file.
        """
        with open(path) as config_file:
            config = json.load(config_file)

        scenario_df = pd.DataFrame(columns=self.common_columns)
        rows = []  # List to store each row dictionary

        for index, sc in enumerate(config):
            for system in self.animal_systems:
                # Initialize a row with default values
                row = {"Scenarios": index, "Cattle systems": system}

                # Fetch system data which is a list of dictionaries
                system_data = self.data_manager_class.get_system(system)

                # Initialize a dictionary to hold the merged key-values from system_data list
                merged_system_data = {}
                for item in system_data:
                    merged_system_data.update(item)


                # Check if the key is in the merged system data and add them to the row
                for key in self.animal_columns:
                    row_key = merged_system_data.get(key, None)
                    if row_key:
                        row[key] = sc.get(row_key, None)  # Use 0 as default if the key is not in the scenario
                    else: 
                        row[key] = 0

                for key in self.common_columns:
                    if key not in self.animal_columns:
                        if key == "Catchment":
                            row[key] = self.catchment_api.format_catchment_name(sc.get("Catchment", None))
                        else:
                            row[key] = sc.get(key, None)

                rows.append(row)

        # Concatenate all rows into a DataFrame
        if scenario_df.empty:
            scenario_df = pd.DataFrame(rows)
        else:
            scenario_df = pd.concat([scenario_df, pd.DataFrame(rows)], ignore_index=True)

        return scenario_df


    def csv_load(self, path):
        """
        Loads and processes a scenario configuration from a CSV file.

        Parameters:
            path (str): Path to the CSV configuration file.

        Returns:
            pandas.DataFrame: DataFrame containing the processed scenario data from the CSV file.
        """
        # Read data from CSV file
        config = pd.read_csv(path)

        scenario_df = pd.DataFrame(columns=self.common_columns)
        rows = []  # List to store each row dictionary

        # Iterate over the rows of the CSV data
        for index, sc in config.iterrows():
            for system in self.animal_systems:
                # Initialize a row with default values
                row = {"Scenarios": index, "Cattle systems": system}

                # Fetch system data which is a list of dictionaries
                system_data = self.data_manager_class.get_system(system)

                # Initialize a dictionary to hold the merged key-values from system_data list
                merged_system_data = {}
                for item in system_data:
                    merged_system_data.update(item)

                # Check if the key is in the merged system data and add them to the row
                for key in self.animal_columns:
                    row_key = merged_system_data.get(key, None)
                    if row_key and row_key in sc:
                        row[key] = sc[row_key] if pd.notnull(sc[row_key]) else 0  # Use 0 as default if the key is not in the scenario or value is NaN
                    else:
                        row[key] = 0
                        
                for key in self.common_columns:
                    if key not in self.animal_columns:
                        if key == "Catchment":
                            row[key] = self.catchment_api.format_catchment_name(sc.get("Catchment", None))
                        else:
                            row[key] = sc[key] if pd.notnull(sc[key]) else 0
                        
                rows.append(row)

        # Concatenate all rows into a DataFrame
        if scenario_df.empty:
            scenario_df = pd.DataFrame(rows)
        else:
            scenario_df = pd.concat([scenario_df, pd.DataFrame(rows)], ignore_index=True)

        return scenario_df