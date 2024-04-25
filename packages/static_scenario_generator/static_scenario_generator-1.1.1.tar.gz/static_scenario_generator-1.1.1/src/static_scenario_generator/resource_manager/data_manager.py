"""
=============
Data Manager
=============
A class to manage data configuration for scenario generation. 
This class handles loading of configuration data from YAML files, providing access to common column names, animal systems, 
and animal-specific column names based on the selected scenario context (national or catchment).

"""

import os
import yaml
from static_scenario_generator.config import get_local_dir as national_get_local_dir
from static_scenario_generator.geo_static_scenario_generator.config import get_local_dir as catchemnt_get_local_dir


class DataManager:
    """
    A class to manage data configuration for scenario generation.

    This class handles loading of configuration data from YAML files, providing access
    to common column names, animal systems, and animal-specific column names based on
    the selected scenario context (national or catchment).

    Attributes:
        common_columns (dict): Dictionary of common column names.
        animal_systems (dict): Dictionary of animal systems configurations.
        animal_columns (dict): Dictionary of animal-specific column names.
    """
    def __init__(self, catchment=False):
        if catchment:
            self._config = self.get_config_data(os.path.join(catchemnt_get_local_dir(), "config.yaml"))
        else:
            self._config = self.get_config_data(os.path.join(national_get_local_dir(), "config.yaml"))

        self.common_columns = self._config.get("common_columns", {})
        self.animal_systems = self._config.get("systems", {})
        self.animal_columns = self._config.get("animal_columns", {})



    def get_config_data(self, config_file):
        """
        Load and return the configuration data from the specified YAML file.

        Args:
            config_file (str): The path to the configuration file.

        Returns:
            dict: The configuration data loaded from the YAML file.
        """
        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)

        return config_data
    
    def get_common_columns(self):
        """
        Returns the list of common column names from the configuration.

        Returns:
            list: A list of common column names.
        """
        return self.common_columns
    
    def get_animal_columns(self):
        """
        Returns the list of animal-specific column names from the configuration.

        Returns:
            list: A list of animal-specific column names.
        """
        return self.animal_columns
    
    def get_systems(self):
        """
        Returns the list of animal systems from the configuration.

        Returns:
            list: A list of animal systems.
        """
        return [list(system.keys())[0] for system in self.animal_systems]

    
    def get_system(self, system_name):
        """
        Retrieves the configuration data for a specific animal system.

        Args:
            system_name (str): The name of the animal system.

        Returns:
            dict: The configuration data for the specified animal system, or an
                  empty dictionary if the system name is not found.
        """
        for system in self.animal_systems:
            if system_name in system:
                return system[system_name]
        return {}  # Return an empty dictionary if the system name is not found


    def check_crop_area(self, key, sc):
        """
        Check if the crop area scenario input is set to 0.

        Args:
            key (str): The key being checked.
            sc (dict): The scenario data dictionary.

        Raises:
            ValueError: If the crop area scenario input is not set to 0.
        """
        if key == "Crop area":
            if sc.get(key, None) !=0:
                raise ValueError("Crop area scenario input is under development and should be set to 0.")
                


