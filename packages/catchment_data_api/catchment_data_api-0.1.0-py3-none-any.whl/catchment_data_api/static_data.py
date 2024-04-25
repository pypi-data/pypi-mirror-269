"""
Static Data Module
------------------

This module contains the StaticData class, which is responsible for managing and accessing static configuration data used in catchment analysis.
"""
import os 
import yaml
from catchment_data_api.config_data import get_local_dir

class StaticData:
    """
    A class for managing and accessing static configuration data used in catchment analysis.
    
    This class loads configuration data from a YAML file, including information such as
    baseline year, herd relation configurations, ewe split ratios, and ewe proportions
    for catchment data analysis.

    Attributes:
        catchment_config (dict): A dictionary containing all the configuration data loaded from the YAML file.
        baseline_year (int): The baseline year for data analysis.
        herd_relation_dict (dict): A dictionary describing the relationships between different herd types.
        ewe_split_dict (dict): A dictionary containing the split ratios for upland and lowland ewes.
        ewe_proportion (float): The global proportion of ewes in the sheep population.
    """
    def __init__(self):
        self.catchment_config = self.get_config_data(os.path.join(get_local_dir(), "config.yaml"))
        self.baseline_year = self.catchment_config.get("baseline_year", {})
        self.herd_relation_dict = self.catchment_config.get("herd_relation_dict", {})
        self.ewe_split_dict = self.catchment_config.get("ewe_split_dict", {})
        self.ewe_proportion = self.catchment_config.get("ewe_proportion", {})


    def get_config_data(self, config_file):
        """
        Load and return the configuration data from the specified file.

        Args:
            config_file (str): The path to the configuration file.

        Returns:
            dict: The configuration data loaded from the file.
        """
        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)

        return config_data
    
    def get_baseline_year(self):
        """
        Retrieves the baseline year.

        Returns:
            int: The baseline year.
        """
        return self.baseline_year

    def get_herd_relation_dict(self):
        """
        Retrieves the herd relation dictionary.

        Returns:
            dict: The herd relation dictionary.
        """
        return self.herd_relation_dict


    def get_ewe_split_dict(self):
        """
        Retrieves the ewe split dictionary.

        Returns:
            dict: The ewe split dictionary.
        """
        return self.ewe_split_dict


    def get_global_ewe_prop(self):
        """
        Retrieves the ewe proportion dict.

        Returns:
            dict: The ewe proportion dictionary.
        """
        return self.ewe_proportion