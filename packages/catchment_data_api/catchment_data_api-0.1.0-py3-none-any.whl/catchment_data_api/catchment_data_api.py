"""
Catchment Data API
------------------
A Python package for interfacing with various catchment-related data. This includes accessing, formatting, 
and aggregating data related to livestock, forests, cultivated areas, peat, and LUCAS survey data within different catchment areas.

This module provides a class, CatchmentDataAPI, that acts as an interface to the catchment data. 
It allows users to retrieve data for livestock, forests, cultivated areas, peat, and LUCAS survey data for all catchments 
or for a specific catchment. 

The class also provides methods to calculate the total population of livestock by type for a specified catchment
and to format catchment names for consistency.
"""
import pandas as pd 
import re
from catchment_data_api.database_manager import DataManager
from catchment_data_api.static_data import StaticData

class CatchmentDataAPI:
    """
    A class to interface with various catchment-related data. This includes
    accessing, formatting, and aggregating data related to livestock, forests,
    cultivated areas, peat, and LUCAS survey data within different catchment areas.
    
    Attributes:
        data_manager (DataManager): An instance of DataManager for database operations.
        static_data (StaticData): An instance of StaticData for accessing static, reference data.
        known_catchments (list): A list of known catchment names retrieved from the database.
    """
    def __init__(self):
        self.data_manager = DataManager()
        self.static_data = StaticData()
        self.known_catchments = self.get_catchment_names()

    def normalize_text(self, text):
        """
        Normalizes a given text string by converting to lowercase, removing special characters,
        and replacing '&' with 'and'.
        
        Parameters:
            text (str): The text to normalize.
        
        Returns:
            str: The normalized text.
        """
        # Lowercase, remove special characters, replace &/and
        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        text = text.replace(' & ', ' and ')
        return text


    def format_catchment_name(self, catchment_name):
        """
        Formats a catchment name by finding the best match among known catchments based on
        the overlap of words after normalization.
        
        Parameters:
            catchment_name (str): The catchment name to format.
        
        Returns:
            str: The best matching catchment name or the original name if no match is found.
        """
        normalized_input = self.normalize_text(catchment_name)
        input_words = set(normalized_input.split())

        best_match = None
        highest_word_match_count = 0

        for known_catchment in self.known_catchments:
            normalized_catchment = self.normalize_text(known_catchment)
            catchment_words = set(normalized_catchment.split())

            common_words_count = len(input_words.intersection(catchment_words))

            if common_words_count > highest_word_match_count:
                highest_word_match_count = common_words_count
                best_match = known_catchment

        return best_match if best_match else catchment_name


    def get_catchment_names(self):
        """
        Retrieves a list of unique catchment names from the database.
        
        Returns:
            numpy.ndarray: An array of unique catchment names.
        """
        df = self.data_manager.get_catchment_livestock_data()
        catchment_names = df['Catchment'].unique()
        return catchment_names
    

    def get_national_herd_raw(self):
        """
        Retrieves the raw national herd data from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing the raw national herd data.
        """
        df = self.data_manager.get_national_herd_raw()
        return df

    def get_catchment_livestock_data(self):
        """
        Retrieves livestock data for all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing livestock data for all catchments.
        """
        df = self.data_manager.get_catchment_livestock_data()
        return df


    def get_catchment_livestock_data_by_catchment_name(self, catchment_name):
        """
        Retrieves livestock data for a specific catchment, identified by its name.
        
        Parameters:
            catchment_name (str): The name of the catchment for which livestock data is requested.
        
        Returns:
            pandas.DataFrame: A DataFrame containing livestock data for the specified catchment.
        """
        catchment = self.format_catchment_name(catchment_name)

        df = self.data_manager.get_catchment_livestock_data()

        catchment_data = df[df['Catchment'] == catchment]

        return catchment_data


    def get_catchment_livestock_total_pop_by_catchment_name(self, catchment_name):
        """
        Calculates the total population of livestock by type for a specified catchment.
        
        Parameters:
            catchment_name (str): The name of the catchment for which total livestock population is requested.
        
        Returns:
            pandas.DataFrame: A DataFrame with the total population of different livestock types in the specified catchment.
        """
        # Format the catchment name to ensure consistency
        catchment = self.format_catchment_name(catchment_name)

        # Retrieve the full dataset
        df = self.data_manager.get_catchment_livestock_data()

        # Group by the 'Catchment' column and sum up the populations
        grouped_data = df.groupby('Catchment').sum(numeric_only=True)

        # Check if the specified catchment exists and create a DataFrame
        if catchment in grouped_data.index:
            sheep_population = int(grouped_data.loc[catchment, 'Sheep pop'])
            ewe_prop = self.static_data.get_global_ewe_prop()
            upland_ewes_split = self.static_data.get_ewe_split_dict()['Upland ewes']
            lowland_ewes_split = self.static_data.get_ewe_split_dict()['Lowland ewes']

            catchment_data = pd.DataFrame({
                'Catchment': [catchment],
                'dairy_cows': [int(grouped_data.loc[catchment, 'Dairy pop'])],
                'suckler_cows': [int(grouped_data.loc[catchment, 'Beef pop'])],
                'Upland ewes': [int((sheep_population * ewe_prop) * upland_ewes_split)],
                'Lowland ewes': [int((sheep_population * ewe_prop)* lowland_ewes_split)]
            })
        else:

            # If catchment is not found, return an empty DataFrame with the same columns
            catchment_data = pd.DataFrame(columns=['Catchment', 'Dairy pop', 'Beef pop', 'Sheep pop'])

        return catchment_data


    def get_catchment_forest_data(self):
        """
        Retrieves forest data for all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing forest data for all catchments.
        """
        df = self.data_manager.get_catchment_forest_data()
        return df
    
    def get_catchment_forest_data_by_catchment_name(self, catchment_name):
        """
        Retrieves forest data for a specific catchment, identified by its name.
        
        Parameters:
            catchment_name (str): The name of the catchment for which forest data is requested.
        
        Returns:
            pandas.DataFrame: A DataFrame containing forest data for the specified catchment.
        """           
        catchment = self.format_catchment_name(catchment_name)

        df = self.data_manager.get_catchment_forest_data()

        catchment_data = df[df['catchment'] == catchment]

        return catchment_data
    

    def get_catchment_grass_data(self):
        """
        Retrieves grassland data for all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing grassland data for all catchments.
        """
        df = self.data_manager.get_catchment_grass_data()
        return df
    

    def get_catchment_cultivated_data(self):
        """
        Retrieves cultivated land data for all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing cultivated land data for all catchments.
        """       
        df = self.data_manager.get_catchment_cultivated_data()
        return df
    
    def get_catchment_cultivated_data_by_catchment_name(self, catchment_name):
        """
        Retrieves cultivated land data for a specific catchment, identified by its name.
        
        Parameters:
            catchment_name (str): The name of the catchment for which cultivated land data is requested.
        
        Returns:
            pandas.DataFrame: A DataFrame containing cultivated land data for the specified catchment.
        """                
        catchment = self.format_catchment_name(catchment_name)

        df = self.data_manager.get_catchment_cultivated_data()

        catchment_data = df[df['catchment'] == catchment]

        return catchment_data
    

    def get_catchment_peat_data(self):
        """
        Retrieves peatland data for all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing peatland data for all catchments.
        """        
        df = self.data_manager.get_catchment_peat_data()
        return df 
    
    
    def get_catchment_peat_data_by_catchment_name(self, catchment_name):
        """
        Retrieves peatland data for a specific catchment, identified by its name.
        
        Parameters:
            catchment_name (str): The name of the catchment for which peatland data is requested.
        
        Returns:
            pandas.DataFrame: A DataFrame containing peatland data for the specified catchment.
        """                        
        catchment = self.format_catchment_name(catchment_name)

        df = self.data_manager.get_catchment_peat_data()

        catchment_data = df[df['catchment'] == catchment]

        return catchment_data   


    def get_catchment_lucas_data(self):
        """
        Retrieves LUCAS (Land Use and Coverage Area frame Survey) data for all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing LUCAS data for all catchments.
        """
        df = self.data_manager.get_catchment_lucas_data()
        return df
    

    def get_catchment_lucas_data_by_catchment_name(self, catchment_name):
        """
        Retrieves LUCAS data for a specific catchment, identified by its name.
        
        Parameters:
            catchment_name (str): The name of the catchment for which LUCAS data is requested.
        
        Returns:
            pandas.DataFrame: A DataFrame containing LUCAS data for the specified catchment.
        """                                
        catchment = self.format_catchment_name(catchment_name)

        df = self.data_manager.get_catchment_lucas_data()

        catchment_data = df[df['catchment'] == catchment]

        return catchment_data

    def get_catchment_grass_in_use(self):
        """
        Retrieves data for grasslands in use across all catchments from the database.
        
        Returns:
            pandas.DataFrame: A DataFrame containing data for grasslands currently in use.
        """
        df = self.data_manager.get_catchment_grass_data()
        
        mask = (df["cover_type"] == "Improved Grassland") | (df["cover_type"] == "Wet Grassland") | (df["cover_type"] == "Dry Grassland")

        grass_df = df.loc[mask]

        return grass_df


    def get_formatted_catchment_grass_in_use(self):
        """
        Retrieves and formats data for grasslands in use, organizing it by catchment, cover type, and soil type.
        
        Returns:
            pandas.DataFrame: A DataFrame containing organized and formatted data for grasslands in use.
        """
        df = self.get_catchment_grass_in_use()

        # Create a pivot table with MultiIndex columns
        grouped_data = df.pivot_table(index='catchment',
                                    columns=['cover_type', 'soil_type'],
                                    values='total_hectares',
                                    aggfunc='sum',
                                    fill_value=0)

        # Identify unique soil types
        soil_types = df['soil_type'].unique()

        # For each soil type, create 'Pasture' and 'Rough_grazing_in_use' columns
        for soil_type in soil_types:
            grouped_data[('Pasture', soil_type)] = grouped_data[('Improved Grassland', soil_type)]
            grouped_data[('Rough_grazing_in_use', soil_type)] = (
                grouped_data[('Wet Grassland', soil_type)] + grouped_data[('Dry Grassland', soil_type)]
            )

        # Drop the original grassland type columns for each soil type
        for soil_type in soil_types:
            for grassland_type in ['Improved Grassland', 'Wet Grassland', 'Dry Grassland']:
                if (grassland_type, soil_type) in grouped_data.columns:
                    grouped_data.drop(columns=(grassland_type, soil_type), inplace=True)

        # Reset index if required
        grouped_data.reset_index(inplace=True)

        return grouped_data


    def get_catchment_grass_data_by_catchment_name(self, catchment_name):
        """
        Retrieves and formats grassland data for a specific catchment, identified by its name, focusing on grasslands currently in use.
        
        Parameters:
            catchment_name (str): The name of the catchment for which grassland data
        
        Returns:
            pandas.DataFrame: A DataFrame containing formatted data for grasslands in use in the specified catchment.
        """
        catchment = self.format_catchment_name(catchment_name)

        df = self.get_formatted_catchment_grass_in_use()

        catchment_data = df[df['catchment'] == catchment]

        return catchment_data