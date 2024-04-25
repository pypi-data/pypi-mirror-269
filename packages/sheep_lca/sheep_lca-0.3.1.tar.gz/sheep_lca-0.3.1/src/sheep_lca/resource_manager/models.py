"""
Models Module
-------------

This module contains classes for representing and manipulating dynamic data structures used in livestock data management, specifically for lifecycle assessment in sheep farming. It includes classes for handling animal data, emissions factors, grass data, concentrate data, and upstream data.

Classes:
    DynamicData: A base class for creating objects that hold dynamic data.
    AnimalCategory: Represents different categories of animals on a farm, inheriting from DynamicData.
    AnimalCollection: Represents a collection of animal categories, inheriting from DynamicData.
    Farm: Represents a farm entity, inheriting from DynamicData.
    Animal_Features: Contains all features related to animals used in lifecycle assessment.
    Emissions_Factors: Holds emissions factors data relevant to lifecycle assessment.
    Grass: Contains data about different types of grasses.
    Concentrate: Contains data about different types of animal feed concentrates.
    Upstream: Contains upstream data such as resources used and emissions released before reaching the farm.

Functions:
    load_grass_data(): Loads and returns grass data.
    load_concentrate_data(): Loads and returns concentrate data.
    load_upstream_data(): Loads and returns upstream data.
    load_emissions_factors_data(): Loads and returns emissions factors data.
    load_animal_features_data(): Loads and returns animal features data.
    load_farm_data(farm_data_frame): Takes a DataFrame and returns a dictionary of Farm objects.
    load_livestock_data(animal_data_frame): Takes a DataFrame and returns a dictionary of AnimalCollection objects mapped by farm ID.
    print_livestock_data(data): Utility function to print livestock data for debugging or logging.

The classes mainly serve as containers for the data loaded from external sources like databases or CSV files, enabling structured access and manipulation of this data within the lifecycle assessment processes.
"""
import pandas

class DynamicData(object):
    """
    A base class for creating dynamic data objects. This class is designed to create instances with attributes
    that are dynamically assigned based on input data. It allows for the easy creation and manipulation of
    data objects without needing a predefined class structure.

    Attributes are set based on two inputs: a defaults dictionary and a data dictionary. The defaults dictionary
    provides initial values for attributes, ensuring that the object has all necessary attributes with default values.
    The data dictionary contains actual values meant to override these defaults where applicable.

    Parameters:
        data (dict): A dictionary containing actual values for attributes of the instance. Keys correspond to attribute
                     names, and values correspond to the values those attributes should take.
        defaults (dict, optional): A dictionary containing default values for attributes of the instance. Keys
                                   correspond to attribute names, and values are the default values those attributes
                                   should take. Defaults to an empty dictionary if not provided.

    """
    def __init__(self, data, defaults={}):

        # Set the defaults first
        for variable, value in defaults.items():
            setattr(self, variable, value)

        # Overwrite the defaults with the real values
        for variable, value in data.items():
            setattr(self, variable, value)


class AnimalCategory(DynamicData):
    """
    A specialized data container class for animal categories, extending DynamicData. This class is designed
    to store and manage information specific to different types of animals.
    It predefines a set of attributes with default values relevant to animal data management.

    Inherits from:
        DynamicData: Inherits the capability to dynamically set attributes based on input data.

    Default Attributes (and their default values):
        pop (int): Population count of the animals in this category (default: 0).
        wool (float): Average wool produced in kg (default: 0.0).
        weight (float): Average weight per animal, in kilograms (default: 0.0).
        forage (str): Type of forage consumed by the animals (default: 'average').
        grazing (str): Type of grazing condition (default: 'pasture').
        con_type (str): Type of concentrate feed provided (default: 'concentrate').
        con_amount (float): Amount of concentrate feed provided per day, in kilograms (default: 0.0).
        t_outdoors (int): Average time spent outdoors per day, in hours (default: 24).
        t_indoors (int): Average time spent indoors per day, in hours (default: 0).
        t_stabled (int): Average time spent in stable conditions per day, in hours (default: 0).
        mm_storage (str): Type of manure management storage system (default: 'solid').
        daily_spreading (str): Type of manure spreading technique used daily (default: 'none').
        n_sold (int): Number of animals sold from this category (default: 0).
        n_bought (int): Number of animals bought into this category (default: 0).
        meat_price_kg (float): Price of meat per kilogram (default: 0.0).
        wool_price_kg (float): Price of wool per kilogram (default: 0.0).

    Parameters:
        data (dict): A dictionary containing actual values for attributes of the animal category. Keys correspond
                     to attribute names, and values correspond to the values those attributes should take.

    """
    def __init__(self, data):

        defaults = {
            "pop": 0,
            "wool": 0,
            "weight": 0,
            "forage": "average",
            "grazing": "pasture",
            "con_type": "concentrate",
            "con_amount": 0,
            "t_outdoors": 24,
            "t_indoors": 0,
            "t_stabled": 0,
            "mm_storage": "solid",
            "daily_spreading": "none",
            "n_sold": 0,
            "n_bought": 0,
            "meat_price_kg": 0,
            "wool_price_kg": 0,
        }

        super(AnimalCategory, self).__init__(data, defaults)


class AnimalCollection(DynamicData):
    """
    A data container class for a collection of animal categories. It extends the
    DynamicData class to enable dynamic attribute assignment based on input data, typically used to represent a group
    of animals categorized by species, age, or other criteria.

    Inherits from:
        DynamicData: Inherits the capability to dynamically set attributes based on input data.

    Parameters:
        data (dict): A dictionary where keys represent category names or identifiers, and values are instances of
                     AnimalCategory or similar data structures that hold information specific to each animal group.

    """
    def __init__(self, data):
        super(AnimalCollection, self).__init__(data)


class Farm(DynamicData):
    """
    A data container class representing a "farm", or similar unit, extending the DynamicData class to enable dynamic attribute assignment
    based on input data. This class is typically used to encapsulate all relevant information about a "farm", including
    details about various animal collections, resources, and management practices.

    Inherits from:
        DynamicData: Inherits the capability to dynamically set attributes based on input data.

    Parameters:
        data (dict): A dictionary containing attributes and values that represent various aspects of the farm. This
                     can include information such as the farm's ID, location, size, and any specific animal collections
                     associated with the farm.
    """
    def __init__(self, data): 
        super(Farm, self).__init__(data)


######################################################################################
# Animal Features Data
######################################################################################
class Animal_Features(object):
    """
    A class that encapsulates various features and statistical data related to different categories of farm animals.
    This class is designed to store and provide access to a wide array of information concerning animal characteristics,
    such as weight characteristics.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing animal features data.
        animal_features (dict): A dictionary storing all the animal features with keys representing the feature names
                                and values representing the corresponding data extracted from the DataFrame.

    Parameters:
        data (pandas.DataFrame): The DataFrame containing the animal features data.

    Methods:
        Various getter methods for each animal feature, such as get_mature_weight_male(), etc.
    """    
    def __init__(self, data):
        self.data_frame = data
        self.animal_features = {}

        for _, row in self.data_frame.iterrows():

            mature_weight_male = row.get("mature_weight_male")
            mature_weight_female = row.get("mature_weight_female")
            ewe_weight_after_weaning = row.get("ewe_weight_after_weaning")
            lamb_less_1_yr_weight_after_weaning = row.get(
                "lamb_less_1_yr_weight_after_weaning"
            )
            lamb_more_1_yr_weight_after_weaning = row.get(
                "lamb_more_1_yr_weight_after_weaning"
            )
            lamb_weight_gain = row.get("lamb_weight_gain")
            ram_weight_after_weaning = row.get("ram_weight_after_weaning")
            ewe_weight_1_year_old = row.get("ewe_weight_1_year_old")
            lamb_less_1_yr_weight = row.get("lamb_less_1_yr_weight")
            lamb_more_1_yr_weight = row.get("lamb_more_1_yr_weight")
            lamb_male_more_1_year_old = row.get("lamb_male_more_1_year_old")
            ram_weight_1_year_old = row.get("ram_weight_1_year_old")
            lamb_weight_at_birth = row.get("lamb_weight_at_birth")

            self.animal_features = {
                "mature_weight_male": mature_weight_male,
                "mature_weight_female": mature_weight_female,
                "ewe_weight_after_weaning": ewe_weight_after_weaning,
                "lamb_less_1_yr_weight_after_weaning": lamb_less_1_yr_weight_after_weaning,
                "lamb_more_1_yr_weight_after_weaning": lamb_more_1_yr_weight_after_weaning,
                "lamb_weight_gain": lamb_weight_gain,
                "ram_weight_after_weaning": ram_weight_after_weaning,
                "ewe_weight_1_year_old": ewe_weight_1_year_old,
                "lamb_less_1_yr_weight": lamb_less_1_yr_weight,
                "lamb_more_1_yr_weight": lamb_more_1_yr_weight,
                "lamb_male_more_1_year_old": lamb_male_more_1_year_old,
                "ram_weight_1_year_old": ram_weight_1_year_old,
                "lamb_weight_at_birth": lamb_weight_at_birth,
            }

    def get_mature_weight_male(self):
        """
        Returns the mature weight of male sheep.

        Returns:
            float: The mature weight of male sheep.
        """
        return self.animal_features.get("mature_weight_male")

    def get_mature_weight_female(self):
        """
        Returns the mature weight of female sheep.

        Returns:
            float: The mature weight of female sheep.
        """
        return self.animal_features.get("mature_weight_female")

    def get_ewe_weight_after_weaning(self):
        """
        Returns the weight of ewes after weaning.

        Returns:
            float: The weight of ewes after weaning.
        """
        return self.animal_features.get("ewe_weight_after_weaning")

    def get_lamb_less_1_yr_weight_after_weaning(self):
        """
        Returns the weight of lambs less than 1 year old after weaning.

        Returns:
            float: The weight of lambs less than 1 year old after weaning.
        """
        return self.animal_features.get("lamb_less_1_yr_weight_after_weaning")

    def get_lamb_more_1_yr_weight_after_weaning(self):
        """
        Returns the weight of lambs more than 1 year old after weaning.

        Returns:
            float: The weight of lambs more than 1 year old after weaning.
        """
        return self.animal_features.get("lamb_more_1_yr_weight_after_weaning")

    def get_lamb_weight_gain(self):
        """
        Returns the weight gain of lambs.

        Returns:
            float: The weight gain of lambs.
        """
        return self.animal_features.get("lamb_weight_gain")

    def get_ram_weight_after_weaning(self):
        """
        Returns the weight of rams after weaning.

        Returns:
            float: The weight of rams after weaning.
        """
        return self.animal_features.get("ram_weight_after_weaning")

    def get_ewe_weight_1_year_old(self):
        """
        Returns the weight of ewes at 1 year old.

        Returns:
            float: The weight of ewes at 1 year old.
        """
        return self.animal_features.get("ewe_weight_1_year_old")

    def get_lamb_less_1_yr_weight(self):
        """
        Returns the weight of lambs less than 1 year old.

        Returns:
            float: The weight of lambs less than 1 year old.
        """
        return self.animal_features.get("lamb_less_1_yr_weight")

    def get_lamb_more_1_yr_weight(self):
        """
        Returns the weight of lambs more than 1 year old.

        Returns:
            float: The weight of lambs more than 1 year old.
        """
        return self.animal_features.get("lamb_more_1_yr_weight")

    def get_lamb_male_more_1_year_old(self):
        """
        Returns the weight of male lambs more than 1 year old.

        Returns:
            float: The weight of male lambs more than 1 year old.
        """
        return self.animal_features.get("lamb_male_more_1_year_old")

    def get_ram_weight_1_year_old(self):
        """
        Returns the weight of rams at 1 year old.

        Returns:
            float: The weight of rams at 1 year old.
        """
        return self.animal_features.get("ram_weight_1_year_old")

    def get_lamb_weight_at_birth(self):
        """
        Returns the weight of lambs at birth.

        Returns:
            float: The weight of lambs at birth.
        """
        return self.animal_features.get("lamb_weight_at_birth")

    def is_loaded(self):
        """
        Checks if the data frame has been loaded successfully.

        Returns:
            bool: True if the data frame is not None, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################

######################################################################################
# Emissions Factors Data
######################################################################################
class Emissions_Factors(object):
    """
    A class that encapsulates emissions factor data for various elements related to livestock farming. This includes 
    factors for methane production, nitrogen emissions, and energy use among others. The class provides methods to 
    retrieve specific emissions factors based on livestock types and activities.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing all the emissions factors data.
        emissions_factors (dict): A dictionary mapping emissions factor names to their values.

    Parameters:
        data (pandas.DataFrame): The DataFrame containing emissions factors data. Each row represents a different 
                                 set of factors and includes columns for each type of emissions factor.

    Methods:
        Each 'get' method corresponds to a specific type of emissions factor, allowing for easy retrieval of data 
        for use in calculations. For example, get_ef_net_energy_for_maintenance_sheep_up_to_a_year() returns the 
        energy required for maintenance of a sheep up to a year old.

    """
    def __init__(self, data):

        self.data_frame = data
        self.emissions_factors = {}

        for _, row in self.data_frame.iterrows():

            ef_net_energy_for_maintenance_sheep_up_to_a_year = row.get(
                "ef_net_energy_for_maintenance_sheep_up_to_a_year"
            )
            ef_net_energy_for_maintenance_sheep_more_than_a_year = row.get(
                "ef_net_energy_for_maintenance_sheep_more_than_a_year"
            )
            ef_net_energy_for_maintenance_intact_male_up_to_year = row.get(
                "ef_net_energy_for_maintenance_intact_male_up_to_year"
            )
            ef_net_energy_for_maintenance_intact_male_more_than_a_year = row.get(
                "ef_net_energy_for_maintenance_intact_male_more_than_a_year"
            )

            ef_feeding_situation_housed_ewes = row.get(
                "ef_feeding_situation_housed_ewes"
            )
            ef_feeding_situation_grazing_flat_pasture = row.get(
                "ef_feeding_situation_grazing_flat_pasture"
            )
            ef_feeding_situation_grazing_hilly_pasture = row.get(
                "ef_feeding_situation_grazing_hilly_pasture"
            )
            ef_feeding_situation_housed_fattening_lambs = row.get(
                "ef_feeding_situation_housed_fattening_lambs"
            )

            ef_net_energy_for_growth_females_a = row.get(
                "ef_net_energy_for_growth_females_a"
            )
            ef_net_energy_for_growth_males_a = row.get(
                "ef_net_energy_for_growth_males_a"
            )
            ef_net_energy_for_growth_castrates_a = row.get(
                "ef_net_energy_for_growth_castrates_a"
            )

            ef_net_energy_for_growth_females_b = row.get(
                "ef_net_energy_for_growth_females_b"
            )
            ef_net_energy_for_growth_males_b = row.get(
                "ef_net_energy_for_growth_males_b"
            )
            ef_net_energy_for_growth_castrates_b = row.get(
                "ef_net_energy_for_growth_castrates_b"
            )

            ef_net_energy_for_pregnancy = row.get("ef_net_energy_for_pregnancy")

            ef_methane_conversion_factor_sheep = row.get(
                "ef_methane_conversion_factor_sheep"
            )
            ef_methane_conversion_factor_lamb = row.get(
                "ef_methane_conversion_factor_lamb"
            )

            ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition = row.get(
                "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"
            )

            ef3__cpp_pasture_range_paddock_sheep_direct_n2o = row.get(
                "ef3__cpp_pasture_range_paddock_sheep_direct_n2o"
            )

            ef_direct_n2o_emissions_soils = row.get("ef_direct_n2o_emissions_soils")
            ef_indirect_n2o_atmospheric_deposition_to_soils_and_water = row.get(
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
            )
            ef_indirect_n2o_from_leaching_and_runoff = row.get(
                "ef_indirect_n2o_from_leaching_and_runoff"
            )
            ef_TAN_house_liquid = row.get("ef_TAN_house_liquid")
            ef_TAN_house_solid_deep_bedding = row.get("ef_TAN_house_solid_deep_bedding")
            ef_TAN_storage_tank = row.get("ef_TAN_storage_tank")
            ef_TAN_storage_solid_deep_bedding = row.get(
                "ef_TAN_storage_solid_deep_bedding"
            )
            ef_mcf_liquid_tank = row.get("ef_mcf_liquid_tank")
            ef_mcf_solid_storage_deep_bedding = row.get(
                "ef_mcf_solid_storage_deep_bedding"
            )
            ef_mcf_anaerobic_digestion = row.get("ef_mcf_anaerobic_digestion")
            ef_n2o_direct_storage_tank_liquid = row.get(
                "ef_n2o_direct_storage_tank_liquid"
            )
            ef_n2o_direct_storage_tank_solid = row.get(
                "ef_n2o_direct_storage_tank_solid"
            )
            ef_n2o_direct_storage_solid_deep_bedding = row.get(
                "ef_n2o_direct_storage_solid_deep_bedding"
            )
            ef_n2o_direct_storage_tank_anaerobic_digestion = row.get(
                "ef_n2o_direct_storage_tank_anaerobic_digestion"
            )
            ef_nh3_daily_spreading_none = row.get("ef_nh3_daily_spreading_none")
            ef_nh3_daily_spreading_manure = row.get("ef_nh3_daily_spreading_manure")
            ef_nh3_daily_spreading_broadcast = row.get(
                "ef_nh3_daily_spreading_broadcast"
            )
            ef_nh3_daily_spreading_injection = row.get(
                "ef_nh3_daily_spreading_injection"
            )
            ef_nh3_daily_spreading_traling_hose = row.get(
                "ef_nh3_daily_spreading_trailing_hose"
            )
            ef_urea = row.get("ef_urea")
            ef_urea_and_nbpt = row.get("ef_urea_and_nbpt")
            ef_fracGASF_urea_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox"
            )
            ef_fracGASF_urea_and_nbpt_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"
            )
            ef_frac_leach_runoff = row.get("ef_frac_leach_runoff")
            ef_ammonium_nitrate = row.get("ef_ammonium_nitrate")
            ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
            )
            Frac_P_Leach = row.get("Frac_P_Leach")
            ef_urea_co2 = row.get("ef_urea_co2")
            ef_lime_co2 = row.get("ef_lime_co2")


            self.emissions_factors = {
                "ef_net_energy_for_maintenance_sheep_up_to_a_year": ef_net_energy_for_maintenance_sheep_up_to_a_year,
                "ef_net_energy_for_maintenance_sheep_more_than_a_year": ef_net_energy_for_maintenance_sheep_more_than_a_year,
                "ef_net_energy_for_maintenance_intact_male_up_to_year": ef_net_energy_for_maintenance_intact_male_up_to_year,
                "ef_net_energy_for_maintenance_intact_male_more_than_a_year": ef_net_energy_for_maintenance_intact_male_more_than_a_year,
                "ef_feeding_situation_housed_ewes": ef_feeding_situation_housed_ewes,
                "ef_feeding_situation_grazing_flat_pasture": ef_feeding_situation_grazing_flat_pasture,
                "ef_feeding_situation_grazing_hilly_pasture": ef_feeding_situation_grazing_hilly_pasture,
                "ef_feeding_situation_housed_fattening_lambs": ef_feeding_situation_housed_fattening_lambs,
                "ef_net_energy_for_growth_females_a": ef_net_energy_for_growth_females_a,
                "ef_net_energy_for_growth_males_a": ef_net_energy_for_growth_males_a,
                "ef_net_energy_for_growth_castrates_a": ef_net_energy_for_growth_castrates_a,
                "ef_net_energy_for_growth_females_b": ef_net_energy_for_growth_females_b,
                "ef_net_energy_for_growth_males_b": ef_net_energy_for_growth_males_b,
                "ef_net_energy_for_growth_castrates_b": ef_net_energy_for_growth_castrates_b,
                "ef_net_energy_for_pregnancy": ef_net_energy_for_pregnancy,
                "ef_methane_conversion_factor_sheep": ef_methane_conversion_factor_sheep,
                "ef_methane_conversion_factor_lamb": ef_methane_conversion_factor_lamb,
                "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition": ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "ef3__cpp_pasture_range_paddock_sheep_direct_n2o": ef3__cpp_pasture_range_paddock_sheep_direct_n2o,
                "ef_direct_n2o_emissions_soils": ef_direct_n2o_emissions_soils,
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water": ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "ef_indirect_n2o_from_leaching_and_runoff": ef_indirect_n2o_from_leaching_and_runoff,
                "ef_TAN_house_liquid": ef_TAN_house_liquid,
                "ef_TAN_house_solid_deep_bedding": ef_TAN_house_solid_deep_bedding,
                "ef_TAN_storage_tank": ef_TAN_storage_tank,
                "ef_TAN_storage_solid_deep_bedding": ef_TAN_storage_solid_deep_bedding,
                "ef_mcf_liquid_tank": ef_mcf_liquid_tank,
                "ef_mcf_solid_storage_deep_bedding": ef_mcf_solid_storage_deep_bedding,
                "ef_mcf_anaerobic_digestion": ef_mcf_anaerobic_digestion,
                "ef_n2o_direct_storage_tank_liquid": ef_n2o_direct_storage_tank_liquid,
                "ef_n2o_direct_storage_tank_solid": ef_n2o_direct_storage_tank_solid,
                "ef_n2o_direct_storage_solid_deep_bedding": ef_n2o_direct_storage_solid_deep_bedding,
                "ef_n2o_direct_storage_tank_anaerobic_digestion": ef_n2o_direct_storage_tank_anaerobic_digestion,
                "ef_nh3_daily_spreading_none": ef_nh3_daily_spreading_none,
                "ef_nh3_daily_spreading_manure": ef_nh3_daily_spreading_manure,
                "ef_nh3_daily_spreading_broadcast": ef_nh3_daily_spreading_broadcast,
                "ef_nh3_daily_spreading_injection": ef_nh3_daily_spreading_injection,
                "ef_nh3_daily_spreading_traling_hose": ef_nh3_daily_spreading_traling_hose,
                "ef_urea": ef_urea,
                "ef_urea_and_nbpt": ef_urea_and_nbpt,
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox": ef_fracGASF_urea_fertilisers_to_nh3_and_nox,
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox": ef_fracGASF_urea_and_nbpt_to_nh3_and_nox,
                "ef_frac_leach_runoff": ef_frac_leach_runoff,
                "ef_ammonium_nitrate": ef_ammonium_nitrate,
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox": ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox,
                "ef_Frac_P_Leach": Frac_P_Leach,
                "ef_urea_co2":ef_urea_co2,
                "ef_lime_co2":ef_lime_co2,
            }

    def get_ef_net_energy_for_maintenance_sheep_up_to_a_year(self):
        """
        Returns the net energy required for maintenance of sheep up to a year old.

        Returns:
            float: The net energy required for maintenance of sheep up to a year old.
        """
        return self.emissions_factors.get(
            "ef_net_energy_for_maintenance_sheep_up_to_a_year"
        )

    def get_ef_net_energy_for_maintenance_sheep_more_than_a_year(self):
        """
        Returns the net energy required for maintenance of sheep more than a year old.

        Returns:
            float: The net energy required for maintenance of sheep more than a year old.
        """
        return self.emissions_factors.get(
            "ef_net_energy_for_maintenance_sheep_more_than_a_year"
        )

    def get_ef_net_energy_for_maintenance_intact_male_up_to_year(self):
        """
        Returns the net energy required for maintenance of intact male up to a year old.

        Returns:
            float: The net energy required for maintenance of intact male up to a year old.
        """
        return self.emissions_factors.get(
            "ef_net_energy_for_maintenance_intact_male_up_to_year"
        )

    def get_ef_net_energy_for_maintenance_intact_male_more_than_a_year(self):
        """
        Returns the net energy required for maintenance of intact male over a year old.

        Returns:
            float: The net energy required for maintenance of intact male over a year old.
        """
        return self.emissions_factors.get(
            "ef_net_energy_for_maintenance_intact_male_more_than_a_year"
        )

    def get_ef_feeding_situation_housed_ewes(self):
        """
        Returns the coefficient for feeding situation of housed ewes.

        Returns:
            float: The coefficient for feeding situation of housed ewes.
        """
        return self.emissions_factors.get("ef_feeding_situation_housed_ewes")

    def get_ef_feeding_situation_grazing_flat_pasture(self):
        """
        Returns the coefficient for feeding situation of grazing on flat pasture.

        Returns:
            float: The coefficient for feeding situation of grazing on flat pasture.
        """
        return self.emissions_factors.get("ef_feeding_situation_grazing_flat_pasture")

    def get_ef_feeding_situation_grazing_hilly_pasture(self):
        """
        Returns the coefficient for feeding situation of grazing on hilly pasture.

        Returns:
            float: The coefficient for feeding situation of grazing on hilly pasture.
        """
        return self.emissions_factors.get("ef_feeding_situation_grazing_hilly_pasture")

    def get_ef_feeding_situation_housed_fattening_lambs(self):
        """
        Returns the coefficient for feeding situation of housed fattening lambs.

        Returns:
            float: The coefficient for feeding situation of housed fattening lambs.
        """
        return self.emissions_factors.get("ef_feeding_situation_housed_fattening_lambs")

    def get_ef_net_energy_for_growth_females_a(self):
        """
        Returns the coefficient_a for net energy required for growth for females. 

        Returns:
            float: The coefficient_a for net energy required
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_females_a")

    def get_ef_net_energy_for_growth_males_a(self):
        """
        Returns the coefficient_a for net energy required for growth for males. 

        Returns:
            float: The coefficient_a for net energy required for growth males.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_males_a")

    def ef_net_energy_for_growth_castrates_a(self):
        """
        Returns the coefficient_a for net energy required for growth for castrates.

        Returns:
            float: The coefficient_a for net energy required for growth for castrates.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_castrates_a")

    def get_ef_net_energy_for_growth_females_b(self):
        """
        Returns the coefficient_b for net energy required for growth for females.

        Returns:
            float: The coefficient_b for net energy required for growth for females.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_females_b")

    def get_ef_net_energy_for_growth_males_b(self):
        """
        Returns the coefficient_b for net energy required for growth for males.

        Returns:
            float: The coefficient_b for net energy required for growth for males.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_males_b")

    def ef_net_energy_for_growth_castrates_b(self):
        """
        Returns the coefficient_b for net energy required for growth for castrates.

        Returns:
            float: The coefficient_b for net energy required for growth for castrates.
        """
        return self.emissions_factors.get("ef_net_energy_for_growth_castrates_b")

    def get_ef_net_energy_for_pregnancy(self):
        """
        Returns the net energy required for pregnancy. 

        Returns:
            float: The net energy required for pregnancy.
        """
        return self.emissions_factors.get("ef_net_energy_for_pregnancy")

    def get_ef_methane_conversion_factor_sheep(self):
        """
        Returns the methane conversion factor for sheep.

        Returns:
            float: The methane conversion factor for sheep.
        """
        return self.emissions_factors.get("ef_methane_conversion_factor_sheep")

    def get_ef_methane_conversion_factor_lamb(self):
        """
        Returns the methane conversion factor for lamb.

        Returns:
            float: The methane conversion factor for lamb.
        """
        return self.emissions_factors.get("ef_methane_conversion_factor_lamb")

    def get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(self):
        """
        Returns the fraction of total ammonia nitrogen pasture range paddock deposition.

        Returns:
            float: The fraction of total ammonia nitrogen pasture range paddock deposition.
        """
        return self.emissions_factors.get(
            "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"
        )

    def get_ef3__cpp_pasture_range_paddock_sheep_direct_n2o(self):
        """
        Returns the direct N2O emissions factor for sheep in pasture range paddock.

        Returns:
            float: The direct N2O emissions factor for sheep in pasture range paddock.
        """
        return self.emissions_factors.get(
            "ef3__cpp_pasture_range_paddock_sheep_direct_n2o"
        )

    def get_ef_direct_n2o_emissions_soils(self):
        """
        Returns the direct N2O emissions factor for soils.

        Returns:
            float: The direct N2O emissions factor for soils.
        """
        return self.emissions_factors.get("ef_direct_n2o_emissions_soils")

    def get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(self):
        """
        Returns the indirect N2O emissions factor for atmospheric deposition to soils and water.

        Returns:
            float: The indirect N2O emissions factor for atmospheric deposition to soils and water.
        """
        return self.emissions_factors.get(
            "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
        )

    def get_ef_indirect_n2o_from_leaching_and_runoff(self):
        """
        Returns the indirect N2O emissions factor from leaching and runoff.

        Returns:
            float: The indirect N2O emissions factor from leaching and runoff.
        """
        return self.emissions_factors.get("ef_indirect_n2o_from_leaching_and_runoff")

    def get_ef_TAN_house_liquid(self):
        """
        Returns the emissions factor for total ammonia nitrogen from house liquid.

        Returns:
            float: The emissions factor for total ammonia nitrogen from house liquid.
        """
        return self.emissions_factors.get("ef_TAN_house_liquid")

    def get_ef_TAN_house_solid_deep_bedding(self):
        """
        Returns the emissions factor for total ammonia nitrogen from house solid deep bedding.

        Returns:
            float: The emissions factor for total ammonia nitrogen from house solid deep bedding.
        """
        return self.emissions_factors.get("ef_TAN_house_solid_deep_bedding")

    def get_ef_TAN_storage_tank(self):
        """
        Returns the emissions factor for total ammonia nitrogen from storage tank.

        Returns:
            float: The emissions factor for total ammonia nitrogen from storage tank.
        """
        return self.emissions_factors.get("ef_TAN_storage_tank")

    def get_ef_TAN_storage_solid_deep_bedding(self):
        """
        Returns the emissions factor for total ammonia nitrogen from storage solid deep bedding.

        Returns:
            float: The emissions factor for total ammonia nitrogen from storage solid deep bedding.
        """
        return self.emissions_factors.get("ef_TAN_storage_solid_deep_bedding")

    def get_ef_mcf_liquid_tank(self):
        """
        Returns the methane conversion factor for liquid tank.

        Returns:
            float: The methane conversion factor for liquid tank.
        """
        return self.emissions_factors.get("ef_mcf_liquid_tank")

    def get_ef_mcf_solid_storage_deep_bedding(self):
        """
        Returns the methane conversion factor for solid storage deep bedding.

        Returns:
            float: The methane conversion factor for solid storage deep bedding.
        """
        return self.emissions_factors.get("ef_mcf_solid_storage_deep_bedding")

    def get_ef_mcf_anaerobic_digestion(self):
        """
        Returns the methane conversion factor for anaerobic digestion.

        Returns:
            float: The methane conversion factor for anaerobic digestion.
        """
        return self.emissions_factors.get("ef_mcf_anaerobic_digestion")

    def get_ef_n2o_direct_storage_tank_liquid(self):
        """
        Returns the direct N2O emissions factor for storage tank liquid.

        Returns:
            float: The direct N2O emissions factor for storage tank liquid.
        """
        return self.emissions_factors.get("ef_n2o_direct_storage_tank_liquid")

    def get_ef_n2o_direct_storage_tank_solid(self):
        """
        Returns the direct N2O emissions factor for storage tank solid.

        Returns:
            float: The direct N2O emissions factor for storage tank solid.
        """
        return self.emissions_factors.get("ef_n2o_direct_storage_tank_solid")

    def get_ef_n2o_direct_storage_solid_deep_bedding(self):
        """
        Returns the direct N2O emissions factor for storage solid deep bedding.

        Returns:
            float: The direct N2O emissions factor for storage solid deep bedding.
        """
        return self.emissions_factors.get("ef_n2o_direct_storage_solid_deep_bedding")

    def get_ef_n2o_direct_storage_tank_anaerobic_digestion(self):
        """
        Returns the direct N2O emissions factor for storage tank anaerobic digestion.

        Returns:
            float: The direct N2O emissions factor for storage tank anaerobic digestion.
        """
        return self.emissions_factors.get(
            "ef_n2o_direct_storage_tank_anaerobic_digestion"
        )

    def get_ef_nh3_daily_spreading_none(self):
        """
        Returns the emissions factor for NH3 from daily spreading with no method.

        Returns:
            float: The emissions factor for NH3 from daily spreading with no method.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_none")

    def get_ef_nh3_daily_spreading_manure(self):
        """
        Returns the emissions factor for NH3 from daily spreading with manure.

        Returns:
            float: The emissions factor for NH3 from daily spreading with manure.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_manure")

    def get_ef_nh3_daily_spreading_broadcast(self):
        """
        Returns the emissions factor for NH3 from daily spreading with broadcast.

        Returns:
            float: The emissions factor for NH3 from daily spreading with broadcast.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_broadcast")

    def get_ef_nh3_daily_spreading_injection(self):
        """
        Returns the emissions factor for NH3 from daily spreading with injection.

        Returns:
            float: The emissions factor for NH3 from daily spreading with injection.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_injection")

    def get_ef_nh3_daily_spreading_traling_hose(self):
        """
        Returns the emissions factor for NH3 from daily spreading with trailing hose.

        Returns:
            float: The emissions factor for NH3 from daily spreading with trailing hose.
        """
        return self.emissions_factors.get("ef_nh3_daily_spreading_traling_hose")

    def get_ef_urea(self):
        """
        Returns the emissions factor for urea.

        Returns:
            float: The emissions factor for urea.
        """
        return self.emissions_factors.get("ef_urea")

    def get_ef_urea_and_nbpt(self):
        """
        Returns the emissions factor for urea and NBPT.

        Returns:
            float: The emissions factor for urea and NBPT.
        """
        return self.emissions_factors.get("ef_urea_and_nbpt")

    def get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(self):
        """
        Get the emissions factor for urea fertilisers to NH3 and NOx.

        Returns:
            float: The emissions factor for urea fertilisers to NH3 and NOx.
        """
        return self.emissions_factors.get("ef_fracGASF_urea_fertilisers_to_nh3_and_nox")

    def get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(self):
        """
        Get the emissions factor for urea and NBPT to NH3 and NOx.

        Returns:
            float: The emissions factor for urea and NBPT to NH3 and NOx.
        """
        return self.emissions_factors.get("ef_fracGASF_urea_and_nbpt_to_nh3_and_nox")

    def get_ef_frac_leach_runoff(self):
        """
        Get the fraction of leaching and runoff.

        Returns:
            float: The fraction of leaching and runoff.
        """
        return self.emissions_factors.get("ef_frac_leach_runoff")

    def get_ef_ammonium_nitrate(self):
        """
        Get the emissions factor for ammonium nitrate.

        Returns:
            float: The emissions factor for ammonium nitrate.
        """
        return self.emissions_factors.get("ef_ammonium_nitrate")

    def get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(self):
        """
        Get the emissions factor for ammonium fertilisers to NH3 and NOx.

        Returns:
            float: The emissions factor for ammonium fertilisers to NH3 and NOx.
        """
        return self.emissions_factors.get(
            "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
        )

    def get_ef_Frac_P_Leach(self):
        """
        Get the fraction of phosphorus leaching.

        Returns:
            float: The fraction of phosphorus leaching.
        """        
        return self.emissions_factors.get("ef_Frac_P_Leach")
    
    def get_ef_urea_co2(self):
        """
        Get the co2 emissions factor for urea.

        Returns:
            float: The co2 emissions factor for urea.
        """        
        return self.emissions_factors.get("ef_urea_co2")
    
    def get_ef_lime_co2(self):
        """
        Get the co2 emissions factor for lime.

        Returns:
            float: The co2 emissions factor for lime.
        """        
        return self.emissions_factors.get("ef_lime_co2")

    def is_loaded(self):
        """
        Check if the emissions factors data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """        
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################


class Grass(object):
    """
    Represents the data and functionality related to various types of grass.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing grass data.
        grasses (dict): A dictionary storing information for each grass genus, 
                        including its forage dry matter digestibility, crude protein, 
                        and gross energy values.

    Methods:
        average(property): Calculates the average value of a specified property 
                           (e.g., dry matter digestibility) across all grasses.
        get_forage_dry_matter_digestibility(forage): Returns the dry matter 
                                                      digestibility for a given forage.
        get_crude_protein(forage): Returns the crude protein value for a given forage.
        get_gross_energy_mje_dry_matter(forage): Returns the gross energy (in MJ per 
                                                 dry matter) for a given forage.
        is_loaded(): Checks whether the data frame is loaded successfully.
    """    
    def average(self, property):

        values = [
            row.get(property)
            for _, row in self.data_frame.iterrows()
            if pandas.notna(row.get(property))
        ]

        return sum(values) / len(values)

    def __init__(self, data):

        self.data_frame = data
        self.grasses = {}

        for _, row in self.data_frame.iterrows():

            genus = row.get("grass_genus".lower())
            dmd = row.get("forage_dry_matter_digestibility")
            cp = row.get("crude_protein")
            ge = row.get("gross_energy")

            self.grasses[genus] = {
                "forage_dry_matter_digestibility": dmd,
                "crude_protein": cp,
                "gross_energy": ge,
            }

        # Pre-compute averages
        self.grasses["average"] = {
            "forage_dry_matter_digestibility": self.average(
                "forage_dry_matter_digestibility"
            ),
            "crude_protein": self.average("crude_protein"),
            "gross_energy": self.average("gross_energy"),
        }

    def get_forage_dry_matter_digestibility(self, forage):
        """
        Get the dry matter digestibility for a given forage.

        Args:
            forage (str): The name of the forage.

        Returns:
            float: The dry matter digestibility for the specified forage.
        """        
        return self.grasses.get(forage).get("forage_dry_matter_digestibility")

    def get_crude_protein(self, forage):
        """
        Get the crude protein value for a given forage.

        Args:
            forage (str): The name of the forage.

        Returns:
            float: The crude protein value for the specified forage.
        """        
        return self.grasses.get(forage).get("crude_protein")

    def get_gross_energy_mje_dry_matter(self, forage):
        """
        Get the gross energy (in MJ per dry matter) for a given forage.

        Args:
            forage (str): The name of the forage.

        Returns:
            float: The gross energy for the specified forage.
        """        
        return self.grasses.get(forage).get("gross_energy")

    def is_loaded(self):
        """
        Check if the grass data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """        
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################
# concentrate file class
########################################################################################
class Concentrate(object):
    """
    Represents the data and functionality related to various types of animal feed concentrates.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing concentrate data.
        concentrates (dict): A dictionary storing information for each type of concentrate,
                             including its dry matter digestibility, digestible energy, crude protein,
                             gross energy, CO2 equivalents, and PO4 equivalents.

    Methods:
        average(property): Calculates the average value of a specified property (e.g., dry matter digestibility)
                           across all concentrates.
        get_con_dry_matter_digestibility(concentrate): Returns the dry matter digestibility for a given concentrate.
        get_con_digestible_energy(concentrate): Returns the digestible energy proportion for a given concentrate.
        get_con_crude_protein(concentrate): Returns the crude protein value for a given concentrate.
        get_gross_energy_mje_dry_matter(concentrate): Returns the gross energy (in MJ per dry matter) for a given concentrate.
        get_con_co2_e(concentrate): Returns the CO2 equivalents for a given concentrate.
        get_con_po4_e(concentrate): Returns the PO4 equivalents for a given concentrate.
        is_loaded(): Checks whether the data frame is loaded successfully.
    """    
    def average(self, property):

        values = [
            row.get(property)
            for _, row in self.data_frame.iterrows()
            if pandas.notna(row.get(property))
        ]

        try:
            return sum(values) / len(values)
        except ZeroDivisionError as err:
            pass

    def __init__(self, data):

        self.data_frame = data
        self.concentrates = {}

        for _, row in self.data_frame.iterrows():

            con_type = row.get("con_type".lower())
            con_dmd = row.get("con_dry_matter_digestibility")
            con_de = row.get("con_digestible_energy")
            con_cp = row.get("con_crude_protein")
            con_gross_energy = row.get("gross_energy_mje_dry_matter")
            con_co2_e = row.get("con_co2_e")
            con_po4_e = row.get("con_po4_e")

            self.concentrates[con_type] = {
                "con_dry_matter_digestibility": con_dmd,
                "con_digestible_energy": con_de,
                "con_crude_protein": con_cp,
                "gross_energy_mje_dry_matter": con_gross_energy,
                "con_co2_e": con_co2_e,
                "con_po4_e": con_po4_e,
            }

        # Pre-compute averages
        self.concentrates["average"] = {
            "con_dry_matter_digestibility": self.average(
                "con_dry_matter_digestibility"
            ),
            "con_digestible_energy": self.average("con_digestible_energy"),
            "con_crude_protein": self.average("con_crude_protein"),
        }

    def get_con_dry_matter_digestibility(self, concentrate):
        """
        Get the dry matter digestibility for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The dry matter digestibility for the specified concentrate.
        """        
        return self.concentrates.get(concentrate).get("con_dry_matter_digestibility")

    def get_con_digestible_energy(self, concentrate):
        """
        Get the digestible energy proportion for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The digestible energy proportion for the specified concentrate.
        """        
        return self.concentrates.get(concentrate).get("con_digestible_energy")

    def get_con_crude_protein(self, concentrate):
        """
        Get the crude protein value for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The crude protein value for the specified concentrate.
        """       
        return self.concentrates.get(concentrate).get("con_crude_protein")

    def get_gross_energy_mje_dry_matter(self, concentrate):
        """
        Get the gross energy (in MJ per dry matter) for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.
            
        Returns:
            float: The gross energy for the specified concentrate.
        """        
        return self.concentrates.get(concentrate).get("gross_energy_mje_dry_matter")

    def get_con_co2_e(self, concentrate):
        """
        Get the CO2 equivalents for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The CO2 equivalents for the specified concentrate.
        """        
        return self.concentrates.get(concentrate).get("con_co2_e")

    def get_con_po4_e(self, concentrate):
        """
        Get the PO4 equivalents for a given concentrate.

        Args:
            concentrate (str): The name of the concentrate.

        Returns:
            float: The PO4 equivalents for the specified concentrate.
        """        
        return self.concentrates.get(concentrate).get("con_po4_e")
    

    def is_loaded(self):
        """
        Check if the concentrate data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """        
        if self.data_frame is not None:
            return True
        else:
            return False


########################################################################################
# Upstream class
########################################################################################
class Upstream(object):
    """
    Represents upstream data for various inputs in an agricultural context.

    Attributes:
        data_frame (pandas.DataFrame): A DataFrame containing upstream data.
        upstream (dict): A dictionary storing upstream data for each type, 
                         including functional units, CO2 equivalents, PO4 equivalents, 
                         SO2 equivalents, net calorific value, and antimony equivalents.

    Methods:
        get_upstream_fu(upstream): Returns the functional unit for a given upstream type.
        get_upstream_kg_co2e(upstream): Returns the kg of CO2 equivalents for a given upstream type.
        get_upstream_kg_po4e(upstream): Returns the kg of PO4 equivalents for a given upstream type.
        get_upstream_kg_so2e(upstream): Returns the kg of SO2 equivalents for a given upstream type.
        get_upstream_mje(upstream): Returns net calorific value in MJ for a given upstream type.
        get_upstream_kg_sbe(upstream): Returns the kg of antimony equivalents for a given upstream type.
        is_loaded(): Checks whether the data frame is loaded successfully.
    """
    def __init__(self, data):

        # data_frame=pandas.read_sql("SELECT * FROM upstream_database", farm_lca_engine)
        self.data_frame = data
        self.upstream = {}

        for _, row in self.data_frame.iterrows():

            upstream_type = row.get("upstream_type".lower())
            upstream_fu = row.get("upstream_fu")
            upstream_kg_co2e = row.get("upstream_kg_co2e")
            upstream_kg_po4e = row.get("upstream_kg_po4e")
            upstream_kg_so2e = row.get("upstream_kg_so2e")
            upstream_mje = row.get("upstream_mje")
            upstream_kg_sbe = row.get("upstream_kg_sbe")

            self.upstream[upstream_type] = {
                "upstream_fu": upstream_fu,
                "upstream_kg_co2e": upstream_kg_co2e,
                "upstream_kg_po4e": upstream_kg_po4e,
                "upstream_kg_so2e": upstream_kg_so2e,
                "upstream_mje": upstream_mje,
                "upstream_kg_sbe": upstream_kg_sbe,
            }

    def get_upstream_fu(self, upstream):
        """
        Get the functional unit for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The functional unit for the specified upstream type.
        """        
        return self.upstream.get(upstream).get("upstream_fu")

    def get_upstream_kg_co2e(self, upstream):
        """
        Get the kg of CO2 equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of CO2 equivalents for the specified upstream type.
        """        
        return self.upstream.get(upstream).get("upstream_kg_co2e")

    def get_upstream_kg_po4e(self, upstream):
        """
        Get the kg of PO4 equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of PO4 equivalents for the specified upstream type.
        """        
        return self.upstream.get(upstream).get("upstream_kg_po4e")

    def get_upstream_kg_so2e(self, upstream):
        """
        Get the kg of SO2 equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of SO2 equivalents for the specified upstream type.
        """        
        return self.upstream.get(upstream).get("upstream_kg_so2e")

    def get_upstream_mje(self, upstream):
        """
        Get the net calorific value in MJ for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The net calorific value in MJ for the specified upstream type.
        """        
        return self.upstream.get(upstream).get("upstream_mje")

    def get_upstream_kg_sbe(self, upstream):
        """
        Get the kg of antimony equivalents for a given upstream type.

        Args:
            upstream (str): The name of the upstream type.

        Returns:
            float: The kg of antimony equivalents for the specified upstream type.
        """        
        return self.upstream.get(upstream).get("upstream_kg_sbe")

    def is_loaded(self):
        """
        Check if the upstream data has been successfully loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """        
        if self.data_frame is not None:
            return True
        else:
            return False


#############################################################################################


def load_grass_data():
    """
    Load the grass data.

    Returns:
        Grass: An instance of the Grass class containing the grass data.
    """    
    return Grass()


def load_concentrate_data():
    """
    Load the concentrate data.

    Returns:
        Concentrate: An instance of the Concentrate class containing the concentrate data.
    """    
    return Concentrate()


def load_upstream_data():
    """
    Load the upstream data.

    Returns:
        Upstream: An instance of the Upstream class containing the upstream data.
    """    
    return Upstream()


def load_emissions_factors_data():
    """
    Load the emissions factors data.

    Returns:
        EmissionsFactors: An instance of the EmissionsFactors class containing the emissions factors data.
    """    
    return Emissions_Factors()


def load_animal_features_data():
    """
    Load the animal features data.

    Returns:
        AnimalFeatures: An instance of the AnimalFeatures class containing the animal features data.
    """    
    return Animal_Features()


def load_farm_data(farm_data_frame):
    """
    Load the farm data.

    Args:
        farm_data_frame (pandas.DataFrame): The DataFrame containing the farm data.

    Returns:
        dict: A dictionary containing the farm data.
    """
    scenario_list = []

    for _, row in farm_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        scenario_list.append(Farm(data))

    return dict(enumerate(scenario_list))


def load_livestock_data(animal_data_frame):
    """
    Load the livestock data.

    Args:
        animal_data_frame (pandas.DataFrame): The DataFrame containing the livestock data.

    Returns:
        dict: A dictionary containing the livestock data.
    """    
    # 1. Load each animal category into an object

    categories = []

    for _, row in animal_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        categories.append(AnimalCategory(data))

    # 2. Aggregate the animal categories into collection based on the farm ID

    collections = {}

    for category in categories:
        farm_id = category.farm_id
        cohort = category.cohort

        if farm_id not in collections:
            collections[farm_id] = {cohort: category}
        else:
            collections[farm_id][cohort] = category

    # 3. Convert the raw collection data into animal collection objects

    collection_objects = {}

    for farm_id, raw_data in collections.items():
        collection_objects[farm_id] = {"animals": AnimalCollection(raw_data)}

    return collection_objects


def print_livestock_data(data):
    """
    Print the livestock data.

    Args:
        data (dict): A dictionary containing the livestock data.
    """    
    for _, key in enumerate(data):
        for animal in data[key].keys():
            for cohort in data[key][animal].__dict__.keys():
                for attribute in (
                    data[key][animal].__getattribute__(cohort).__dict__.keys()
                ):
                    print(
                        f"{cohort}: {attribute} = {data[key][animal].__getattribute__(cohort).__getattribute__(attribute)}"
                    )
