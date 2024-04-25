
"""
Sheep LCA Module
------------------

This module contains classes and methods for calculating the environmental impact of sheep farming, including energy requirements,
emissions, and waste management. It covers various stages of sheep lifecycle and farm operations such as grazing, housing, manure management, 
and fertilization practices. The module aims to provide a comprehensive assessment tool for understanding and reducing the environmental 
footprint associated with sheep production.

The module includes detailed assessments of greenhouse gas emissions, eutrophication potential, air quality impacts, and 
resource usage to support sustainable farming practices and decision-making. By integrating data from various sources and 
applying region-specific (Ireland) emission factors, the module helps in evaluating the overall environmental performance of sheep farms.

Key Features:
- Calculation of energy consumption and efficiency in sheep farming.
- Estimation of greenhouse gas emissions from enteric fermentation, manure management, and other farm activities.
- Assessment of nutrient runoff and its impact on eutrophication.
- Evaluation of ammonia emissions and their contribution to air quality issues.
- Analysis of upstream impacts related to feed production, fertilizer use, and other inputs.
"""
from sheep_lca.resource_manager.sheep_lca_data_manager import LCADataManager
import copy

class Energy:
    """
    A class for calculating various energy needs and outputs for sheep in different stages of their lifecycle and production phases.

    Attributes:
    - data_manager_class (LCADataManager): Manages and provides access to relevant LCA data based on the specific country's environmental factors and agricultural practices.
    
    Methods:
    - ratio_of_net_energy_maintenance(animal): Calculates the ratio of net energy needed for maintenance (REM) of sheep.
    - ratio_of_net_energy_growth(animal): Calculates the ratio of net energy for growth (REG) of sheep.
    - net_energy_for_maintenance(animal): Estimates the net energy required for the maintenance of sheep based on their body weight and energy coefficients.
    - net_energy_for_activity(animal): Determines the energy expended by sheep for their physical activities based on their grazing patterns.
    - net_energy_for_weight_gain(animal): Computes the net energy used for weight gain in sheep, essential for growing lambs and breeding ewes.
    - net_energy_for_lactation(animal): Calculates the energy required for lactation, critical for nursing ewes.
    - net_energy_for_wool(animal): Estimates the energy utilized for wool production, pertinent for wool breeds.
    - net_energy_for_pregnancy(animal): Assesses the energy needs for pregnant ewes.
    - gross_energy_from_concentrate(animal): Evaluates the total energy derived from concentrate feeds provided to the sheep.
    - gross_amount_from_con_in_percent(animal, share_in_percent): Estimates the proportion of energy intake from concentrates compared to the total diet.
    - gross_energy_from_grass(animal): Calculates the total energy intake from grass, the primary forage source for grazing sheep.

    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)

    def ratio_of_net_energy_maintenance(self, animal):
        """
        Calculates the Ratio of Net Energy for Maintenance (REM) for sheep, considering their specific diet.
        
        Parameters:
        - animal (Sheep): The sheep cohort under evaluation.
        
        Returns:
        - float: The ratio of energy available for maintenance after accounting for the digestible energy from the diet.
        
        """
        DE = self.data_manager_class.get_forage_digestibility(animal.forage)

        return (
            1.123
            - (4.092 * (10**-3) * DE)
            + (1.126 * (10**-5) * (DE**2))
            - (25.4 / DE)
        )


    def ratio_of_net_energy_growth(self, animal):
        """
        Calculates the Ratio of Net Energy for Growth (REG) for sheep, taking into account the total energy consumed.
        
        Parameters:
        - animal (Sheep): The sheep cohort under evaluation.
        
        Returns:
        - float: The ratio of energy available for growth, important for lambs and growing sheep.
        
        """
        DE = self.data_manager_class.get_forage_digestibility(animal.forage)

        return (
            1.164
            - (5.160 * (10**-3) * DE)
            + (1.308 * (10**-5) * (DE**2))
            - (37.4 / DE)
        )

    def net_energy_for_maintenance(self, animal):
        """
        Estimates the net energy required for maintaining the basic life functions of sheep based on their weight.
        
        Parameters:
        - animal (Sheep): The sheep under evaluation.
        
        Returns:
        - float: Total energy required for maintenance expressed in MJ/day.
        
        """
        cfi = self.data_manager_class.get_cohort_parameter(animal.cohort, "coefficient")()

        return cfi * (animal.weight**0.75)

    def net_energy_for_activity(self, animal):
        """
        Determines the energy expended by sheep for their physical activities based on typical grazing and movement patterns.
        
        Parameters:
        - animal (Sheep): The sheep under evaluation.
        
        Returns:
        - float: Additional energy expended for activities, in MJ/day.

        """
        return self.data_manager_class.get_grazing_type(animal.grazing)() * animal.weight


    def net_energy_for_weight_gain(self, animal):
        """
        Computes the net energy utilized for weight gain, considering the typical growth rates of sheep.
        
        Parameters:
        - animal (Sheep): The sheep under evaluation.
        
        Returns:
        - float: Energy used for growth in MJ/day.
        
        """
        year = 365

        a = self.data_manager_class.get_cohort_parameter(animal.cohort, "coefficient_a")()
        b = self.data_manager_class.get_cohort_parameter(animal.cohort, "coefficient_b")()

        bw_initial = self.data_manager_class.get_cohort_parameter(animal.cohort, "bwf")()
        bw_finish = self.data_manager_class.get_cohort_parameter(animal.cohort, "bwi")()

        weight_gain = bw_finish - bw_initial

        return (weight_gain * (a + (0.5 * b) * (bw_initial + bw_finish))) / year
    

    def net_energy_for_lactation(self, animal):
        """
        Calculates the energy required for lactation.
        
        Parameters:
        - animal (Sheep): The lactating ewe under evaluation.
        
        Returns:
        - float: Energy needed for producing milk, expressed in MJ/day.

        """
        milk_energy = 4.6
        
        if self.data_manager_class.get_cohort_parameter(animal.cohort, "lactation"):

            return ((5 * self.data_manager_class.get_lactation_weight()) / 365) * milk_energy
        else:
            return 0
        

    def net_energy_for_wool(self, animal):
        """
        Estimates the energy used for wool production.
        
        Parameters:
        - animal (Sheep): The wool-producing sheep under evaluation.
        
        Returns:
        - float: Energy allocated for wool growth, in MJ/day.

        """
        energy_val_wool = 24

        wool_production = animal.wool

        return (energy_val_wool * wool_production) / 365


    def net_energy_for_pregnancy(self, animal):
        """
        Assesses the additional energy requirements for pregnant ewes.
        
        Parameters:
        - animal (Sheep): The pregnant ewe under evaluation.
        
        Returns:
        - float: Additional energy required for supporting pregnancy, in MJ/day.

        """
        coef = self.data_manager_class.get_cohort_parameter(animal.cohort, "pregnancy")
        if coef is None:
            nep = 0
        else:
            nep = coef() * self.net_energy_for_maintenance(animal)

        return nep

    def gross_energy_from_concentrate(self, animal):
        """
        Evaluates the total energy derived from concentrate feeds.
        
        Parameters:
        - animal (Sheep): The sheep consuming the concentrate.
        
        Returns:
        - float: Total energy derived from concentrate feed, in MJ.
        
        Note:
        - Concentrates are often used to supplement grazing, especially in intensive farming systems.
        """
        dm = self.data_manager_class.get_concentrate_digestibility(
            animal.con_type
        )
        mj = self.data_manager_class.get_con_dry_matter_gross_energy(
            animal.con_type
        )

        return (animal.con_amount * dm / 100) * mj


    def gross_amount_from_con_in_percent(self, animal, share_in_percent):
        """
        Estimates the total energy intake for sheep based on a specified percentage of concentrate in their diet, 
        taking into account the energy from both grass and concentrate.

        Parameters:
        - animal (Sheep): The sheep under evaluation.
        - share_in_percent (float): The percentage of the diet that is made up of concentrate.

        Returns:
        - float: Total gross energy intake from the diet, factoring in the specified percentage of concentrate, expressed in Megajoules (MJ).

        Note:
        - This method integrates all energy components including maintenance, activity, lactation, pregnancy, and growth to calculate the overall energy intake.
        """
        REM = self.ratio_of_net_energy_maintenance(animal)
        REG = self.ratio_of_net_energy_growth(animal)
        NEM = self.net_energy_for_maintenance(animal)
        NEA = self.net_energy_for_activity(animal)
        NEL = self.net_energy_for_lactation(animal)
        NEP = self.net_energy_for_pregnancy(animal)
        NEG = self.net_energy_for_weight_gain(animal)
        dm = self.data_manager_class.get_concentrate_digestibility(
            animal.con_type
        )
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)
        mj_con = self.data_manager_class.get_con_dry_matter_gross_energy(
            animal.con_type
        )
        mj_grass = self.data_manager_class.get_grass_dry_matter_gross_energy(
            animal.forage
        )

        DMD_average = (
            share_in_percent / 100.0 * dm + (100.0 - share_in_percent) / 100 * DMD
        )
        mj_average = (
            share_in_percent / 100.0 * mj_con
            + (100.0 - share_in_percent) / 100.0 * mj_grass
        )

        return (
            ((((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD_average / 100.0))
            / mj_average
            * (share_in_percent / (100.0))
        )

    def gross_energy_from_grass(self, animal):
        """
        Calculates the total gross energy intake from grass for sheep after considering the energy provided by concentrates. 

        Parameters:
        - animal (Sheep): The sheep under evaluation.

        Returns:
        - float: Total gross energy intake from grass, after subtracting the energy supplied by concentrates, expressed in Megajoules (MJ).

        Note:
        - This calculation takes into account the energy for maintenance, activity, lactation, pregnancy, growth, and wool production, adjusted for the energy supplied by concentrates.
        """
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)

        REM = self.ratio_of_net_energy_maintenance(animal)
        REG = self.ratio_of_net_energy_growth(animal)
        NEM = self.net_energy_for_maintenance(animal)
        NEA = self.net_energy_for_activity(animal)
        NEL = self.net_energy_for_lactation(animal)
        NEP = self.net_energy_for_pregnancy(animal)
        NEG = self.net_energy_for_weight_gain(animal)
        NEW = self.net_energy_for_wool(animal)
        con = self.gross_energy_from_concentrate(animal)

        return (
            (((NEM + NEA + NEL + NEP) / REM) + ((NEG + NEW) / REG)) / (DMD / 100.0)
        ) - con


class GrassFeed:
    """
    This class is responsible for managing the nutritional energy calculations for grass-fed livestock, 
    integrating various energy needs such as maintenance, growth, and reproduction, and calculating the methane emissions 
    factor from the animals' feed intake.

    Attributes:
        energy_class (Energy): Instance of the Energy class to access energy-related calculations.
        data_manager_class (LCADataManager): Instance of the LCADataManager class for accessing livestock and environmental parameters.

    Methods:
        dry_matter_from_grass: Estimates the amount of dry matter consumed from grass after accounting for the energy provided by concentrates.
        ch4_emissions_factor: Calculates the methane emissions factor based on the animal's total energy intake from grass and concentrates.
    """
    def __init__(self, ef_country):
        self.energy_class = Energy(ef_country)
        self.data_manager_class = LCADataManager(ef_country)

    def dry_matter_from_grass(self, animal):
        """
        Estimates the amount of dry matter consumed from grass by the animal, factoring in the energy contributions from both grass and concentrates.

        Parameters:
        - animal (Animal): The animal for which the dry matter intake is being calculated.

        Returns:
        - float: Total dry matter consumed from grass, expressed in kg/day.
        
        Note:
        - This calculation integrates various energy needs of the animal, such as maintenance, activity, lactation, pregnancy, and growth, and adjusts for the energy supplied by concentrates.
        """

        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)

        REM = self.energy_class.ratio_of_net_energy_maintenance(animal)
        REG = self.energy_class.ratio_of_net_energy_growth(animal)
        NEM = self.energy_class.net_energy_for_maintenance(animal)
        NEA = self.energy_class.net_energy_for_activity(animal)
        NEL = self.energy_class.net_energy_for_lactation(animal)
        NEP = self.energy_class.net_energy_for_pregnancy(animal)
        NEG = self.energy_class.net_energy_for_weight_gain(animal)
        con = self.energy_class.gross_energy_from_concentrate(animal)
        GE = self.data_manager_class.get_grass_dry_matter_gross_energy(animal.forage)
        dm = self.data_manager_class.get_concentrate_digestibility(
            animal.con_type
        )

        share_con = con / (((NEM + NEA + NEL + NEP) / REM) + (NEG / REG))

        DMD_average = share_con * dm + (1 - share_con) * DMD

        return (
            (
                (((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD_average / 100.0)
                - con
            )
        ) / GE

    #########################################################################################################
    # CH4 CAlculations
    ########################################################################################################

    def ch4_emissions_factor(self, animal):
        """
        Calculates the methane emissions factor for the animal based on its total energy intake from both grass and concentrates. This factor is used to estimate the methane emissions from feed intake.

        Parameters:
        - animal (Animal): The animal for which the methane emissions factor is being calculated.

        Returns:
        - float: Methane emissions factor, expressed in kg CH4/year.
        
        Note:
        - This calculation follows the IPCC 2019 guidelines and considers the specific methane conversion factor for the animal category.
        - For lambs, a different conversion factor is used as per NIR 2020 adjustments.
        


        IPCC 2019 EQUATION 10.21

        As per NIR 2020, lambs have an assumed Ym of 4.5 instead of 6.7 as per IPCC.

            GEC = Gross Energy from Concentrates
            GEG = Gross Energy from GE_grass
            GET = Gross Energy total
            Ym  = Methane conversion factor, percent of gross energy content of methane
        """

        year = 365
        Ym = self.data_manager_class.get_cohort_parameter(animal.cohort, "methane_conversion_factor")()
        methane_energy = 55.65  # MJ/kg of CH4

        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)

        GET = GEC + GEG

        return (GET * Ym * year) / methane_energy


#############################################################################################
# Grazing Stage
#############################################################################################


class GrazingStage:
    """
    The GrazingStage class calculates various metrics related to the environmental impact of grazing animals. 
    This includes the volatile solids excretion rate to pasture, net nitrogen excretion, methane emissions from grazing, ammonia emissions, 
    nitrogen and phosphorus leaching, and direct and indirect N2O emissions from pasture.

    Attributes:
        energy_class : Energy
            An instance of the Energy class, used for calculations involving energy metrics of animals.
        grass_feed_class : GrassFeed
            An instance of the GrassFeed class, used to calculate energy intake from grasses.
        data_manager_class : LCADataManager
            An instance of the LCADataManager class, used to access data necessary for the calculations.

    Methods:
        percent_outdoors(animal)
            Calculates the percentage of time an animal spends outdoors based on its time outdoors attribute.
        volatile_solids_excretion_rate_GRAZING(animal)
            Calculates the rate at which volatile solids are excreted to pasture by the animal.
        net_excretion_GRAZING(animal)
            Calculates the net nitrogen excretion per kilogram to pasture by the animal.
        ch4_emissions_for_grazing(animal)
            Estimates the methane emissions from the animal excretion while grazing.
        nh3_emissions_per_year_GRAZING(animal)
            Calculates the total ammonia emissions per year from the animal while grazing.
        Nleach_GRAZING(animal)
            Estimates the amount of nitrogen leached from the pasture due to the grazing animal.
        PLeach_GRAZING(animal)
            Estimates the amount of phosphorus leached from the pasture due to the grazing animal.
        PRP_N2O_direct(animal)
            Calculates the direct nitrous oxide emissions from pasture, range, and paddock due to the grazing animal.
        PRP_N2O_indirect(animal)
            Calculates the indirect nitrous oxide emissions from atmospheric deposition and leaching related to pasture, 
            range, and paddock due to the grazing animal.
        """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.energy_class = Energy(ef_country)
        self.grass_feed_class = GrassFeed(ef_country)

    def percent_outdoors(self, animal):
        """
        Calculates the percentage of the day that the animal spends outdoors.

        Parameters:
        - animal (object): The animal object containing relevant data such as time spent outdoors.

        Returns:
        - float: The percentage of the day the animal spends outdoors.
        """
        hours = 24
        return animal.t_outdoors / hours

    def volatile_solids_excretion_rate_GRAZING(self, animal):
        """
        Calculates the rate at which volatile solids are excreted to pasture by the animal, an essential factor in assessing the environmental impact of grazing. 

        Parameters:
        - animal (object): The animal for which the volatile solids excretion rate is calculated.

        Returns:
        - float: The rate of volatile solids excretion to pasture (kg/day).

        Note:
        - This calculation considers the digestibility of both concentrate and grass, the urinary energy, and the ash content of the manure.
        - 'GEC' represents the gross energy from concentrates consumed by the animal.
        - 'GEG' denotes the gross energy from grass consumed.
        - 'DE' stands for the percentage of digestible energy from the consumed feed.
        - 'UE' refers to the energy lost through urination.
        - 'ASH' represents the incombustible inorganic matter present in the animal's waste.
        - The calculation adjusts for the time the animal spends outdoors ('OUT'), influencing the amount of waste directly deposited onto pasture.
        - The constant '18.45' is used as a conversion factor for dietary gross energy per kilogram of dry matter, expressed in MJ kg-1.
        """
        DEC = self.data_manager_class.get_concentrate_digestable_energy(
            animal.con_type
        )  # Digestibility
        UE = 0.04
        ASH = 0.08
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        OUT = self.percent_outdoors(animal)

        return (
            (((GEG * (1 - (DMD / 100))) + (UE * GEG)) * ((1 - ASH) / 18.45))
            + ((GEC * (1 - (DEC / 100)) + (UE * GEC)) * (((1 - ASH) / 18.45)))
        ) * OUT
    

    def net_excretion_GRAZING(self, animal):
        """
        Calculates the net nitrogen excretion per kilogram to pasture by grazing animals.
        
        Parameters:
        - animal (object): The animal for which the calculation is performed.
        
        Returns:
        - float: Net nitrogen excretion per kilogram to pasture by the animal.
        
        """
        CP = self.data_manager_class.get_concentrate_crude_protein(
            animal.con_type
        )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
        FCP = self.data_manager_class.get_grass_crude_protein(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        OUT = self.percent_outdoors(animal)
        N_retention_frac = 0.10

        return (
            (((GEC * 365) / 18.45) * ((CP / 100) / 6.25) * (1 - N_retention_frac))
            + ((((GEG * 365) / 18.45) * (FCP / 100.0) / 6.25) * (1 - N_retention_frac))
        ) * OUT

    def ch4_emissions_for_grazing(self, animal):
        """
        Estimates the methane emissions resulting from the animal's excretion while grazing.
        
        Parameters:
        - animal (object): The animal for which the methane emissions are estimated.
        
        Returns:
        - float: Estimated methane emissions from grazing, measured in kilograms per year.
        
        Note:
        The estimation follows the IPCC 2019 methodology and adjusts for animal size and time spent outdoors.
        """
        year = 365
        return (
            (self.volatile_solids_excretion_rate_GRAZING(animal) * year)
            * 0.1
            * 0.67
            * 0.19
        )

    def nh3_emissions_per_year_GRAZING(self, animal):
        """
        Calculates total annual ammonia emissions from grazing animals.
        
        Parameters:
        - animal (object): The animal for which the ammonia emissions are calculated.
        
        Returns:
        - float: Total ammonia emissions from grazing, measured over a year.
        
        Note:
        This calculation is based on net nitrogen excretion and the time the animal spends grazing.
        """
        TAN = self.data_manager_class.get_cohort_parameter(animal.cohort, "total_ammonia_nitrogen")()

        return self.net_excretion_GRAZING(animal) * 0.6 * TAN

    def Nleach_GRAZING(self, animal):
        """
        Estimates the amount of nitrogen leached from the pasture as a result of the grazing animal's activities.
        
        Parameters:
        - animal (object): The animal for which nitrogen leaching is being estimated.
        
        Returns:
        - float: Estimated nitrogen leached from the pasture, as a percentage of total nitrogen excretion.
        
        """
        ten_percent_nex = 0.1

        return self.net_excretion_GRAZING(animal) * ten_percent_nex

    def PLeach_GRAZING(self, animal):
        """
        Estimates the amount of phosphorus leached from the pasture due to the animal's grazing.
        
        Parameters:
        - animal (object): The animal for which phosphorus leaching is estimated.
        
        Returns:
        - float: Estimated phosphorus leached from the pasture.
        
        """
        return (self.net_excretion_GRAZING(animal) * (1.8 / 5)) * 0.03

    # direct and indirect (from leaching) N20 from PRP

    def PRP_N2O_direct(self, animal):
        """
        Calculates direct nitrous oxide (N2O) emissions from pasture, range, and paddock (PRP) attributable to the grazing animal.
        
        Parameters:
        - animal (object): The animal for which the direct N2O emissions are calculated.
        
        Returns:
        - float: Direct N2O emissions from PRP due to the grazing animal.
        
        Note:
        Applies IPCC guidelines for direct N2O emissions from animal excretion on pasture.
        """
        EF = self.data_manager_class.get_cohort_parameter(animal.cohort, "direct_n2o")()
        return self.net_excretion_GRAZING(animal) * EF

    def PRP_N2O_indirect(self, animal):
        """
        Calculates indirect N2O emissions from atmospheric deposition and leaching related to pasture, range, and paddock due to grazing animals.
        
        Parameters:
        - animal (object): The grazing animal for which the indirect N2O emissions are estimated.
        
        Returns:
        - float: Indirect N2O emissions from PRP attributable to the animal.
        
        Note:
        Indirect emissions are calculated based on ammonia emissions and nitrogen leaching, following IPCC guidelines.
        """
        indirect_atmosphere = self.data_manager_class.get_cohort_parameter(animal.cohort, "atmospheric_deposition")()
        indirect_leaching = self.data_manager_class.get_cohort_parameter(animal.cohort, "leaching")()

        NH3 = self.nh3_emissions_per_year_GRAZING(animal)
        NL = self.Nleach_GRAZING(animal)

        return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


class HousingStage:
    """
    The HousingStage class calculates various environmental impacts related to the housing of animals. This includes the calculation of volatile solids excretion, nitrogen excretion, ammonia emissions, and indirect nitrous oxide emissions during the period when animals are housed.

    Parameters:
    - ef_country: A country-specific factor that might affect the environmental calculations.

    Methods:
    - percent_indoors(animal): Calculates the percentage of time animals spend indoors.
    - VS_HOUSED(animal): Calculates the volatile solids excreted per day when animals are housed.
    - net_excretion_HOUSED(animal): Calculates the nitrogen excreted per year while animals are housed.
    - total_ammonia_nitrogen_nh4_HOUSED(animal): Calculates the total ammonia nitrogen excreted per year while housed.
    - nh3_emissions_per_year_HOUSED(animal): Calculates the total ammonia emissions per year from housing.
    - HOUSING_N2O_indirect(animal): Calculates indirect nitrous oxide emissions from housing.
    """    
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.energy_class = Energy(ef_country)

    def percent_indoors(self, animal):
        """
        Calculates the percentage of time that the animal spends indoors, combining time spent indoors and stabled.

        Parameters:
            - animal (object): The animal instance for which the indoor time percentage is calculated.

        Returns:
            - float: The percentage of the day that the animal spends indoors.
        """        
        hours = 24
        return (animal.t_indoors + animal.t_stabled) / hours

    def VS_HOUSED(self, animal):
        """
        Calculates the volatile solids excreted per day for animals during the period they are housed. This measurement is essential for understanding the potential environmental impact of manure produced indoors.

        Parameters:
            - animal (object): The animal instance for which the calculation is made.

        Returns:
            - float: The volatile solids excretion rate (kg/day) when animals are housed.

        Note:
            The calculation incorporates the energy from concentrates and grass, digestibility, urinary energy, ash content of manure, and time spent indoors. It provides insight into the potential for nutrient runoff and emissions from stored manure.
       
            Volitile Solids Excretion Rate (kg/day -1)
            GEcon = Gross Energy from Concentrates
            GEgrass = Gross Energy from grass
            DE= Percentage of Digestible Energy
            UE = Urinary Energy
            ASH = Ash content of manure
            18.45 = conversion factor for dietary GE per kg of dry matter, MJ kg-1.
        """
        DEC = self.data_manager_class.get_concentrate_digestable_energy(
            animal.con_type
        )  # Digestibility of concentrate
        UE = 0.04
        ASH = 0.08
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        IN = self.percent_indoors(animal)

        # The second instance of GEG in part 2 of equation may need to be changed to GEC

        return (
            (((GEC * (1 - (DEC / 100))) + (UE * GEC)) * ((1 - ASH) / 18.45))
            + ((GEG * (1 - (DMD / 100)) + (UE * GEG)) * ((1 - ASH) / 18.45))
        ) * IN


    def net_excretion_HOUSED(self, animal):
        """
        Calculates the amount of nitrogen excreted per year by housed animals. 

        Parameters:
            - animal (object): The animal instance for which the calculation is made.

        Returns:
            - float: The amount of nitrogen (kg) excreted per year while animals are housed.
        
        Note:
            The higher rate compared to other models may result from using IPCC equations that account for a broader range of energy ratios.
        """
        CP = self.data_manager_class.get_concentrate_crude_protein(
            animal.con_type
        )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
        FCP = self.data_manager_class.get_grass_crude_protein(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)

        N_retention_frac = 0.10

        IN = self.percent_indoors(animal)

        return (
            (((GEC * 365) / 18.45) * ((CP / 100) / 6.25) * (1 - N_retention_frac))
            + ((((GEG * 365) / 18.45) * (FCP / 100.0) / 6.25) * (1 - N_retention_frac))
        ) * IN


    def total_ammonia_nitrogen_nh4_HOUSED(self, animal):
        """
        Calculates the total ammonia nitrogen (TAN) produced per year from animals housed. 

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Total amount of ammonia nitrogen (TAN) produced per year, in kilograms.

        Note:
            The calculation assumes that TAN constitutes 60% of the total nitrogen excreted (Nex).
        """
        percentage_nex = 0.6

        return self.net_excretion_HOUSED(animal) * percentage_nex

    def nh3_emissions_per_year_HOUSED(self, animal):
        """
        Estimates the total ammonia (NH3) emissions per year from housing based on the total ammonia nitrogen (TAN) produced 
        and the specific management system in place.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Total ammonia emissions per year, in kilograms.

        Note:
            The method utilizes emission factors from IPCC 2019 guidelines and adjustments from the 
            National Inventory Report (NIR) 2020 to account for the management of sheep manure.
        """
        return (
            self.total_ammonia_nitrogen_nh4_HOUSED(animal)
            * self.data_manager_class.get_storage_TAN(animal.mm_storage)()
        )

    def HOUSING_N2O_indirect(self, animal):
        """
        Calculates indirect nitrous oxide (N2O) emissions from housing by considering ammonia (NH3) emissions and their atmospheric deposition.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Indirect N2O emissions per year, in kilograms.

        Note:
            This method uses the emission factor for indirect atmospheric deposition to calculate N2O emissions resulting from the volatilization of NH3 from housed animal manure.
        """
        ef = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        indirect_n2o = self.nh3_emissions_per_year_HOUSED(animal) * ef

        return indirect_n2o


class StorageStage:
    def __init__(self, ef_country):
        """
        The StorageStage class calculates emissions and nutrient loss from manure storage systems. It provides methods for calculating 
        net nitrogen excretion, ammonia nitrogen production, methane emissions, direct and indirect nitrous oxide emissions from manure storage.

        Attributes:
            data_manager_class (LCADataManager): Provides access to necessary data for calculations.
            housing_class (HousingStage): Allows access to calculations from the housing stage for use in storage calculations.

        Methods:
            net_excretion_STORAGE(animal): Calculates net nitrogen excretion from storage.
            total_ammonia_nitrogen_nh4_STORAGE(animal): Calculates total ammonia nitrogen production in storage.
            CH4_STORAGE(animal): Estimates methane emissions from manure storage.
            STORAGE_N2O_direct(animal): Calculates direct nitrous oxide emissions from storage.
            nh3_emissions_per_year_STORAGE(animal): Estimates annual ammonia emissions from storage.
            STORAGE_N2O_indirect(animal): Calculates indirect nitrous oxide emissions related to storage.

        """
        self.data_manager_class = LCADataManager(ef_country)
        self.housing_class = HousingStage(ef_country)

    def net_excretion_STORAGE(self, animal):
        """
        Calculates the net nitrogen excretion from storage by accounting for the reduction in nitrogen due to ammonia volatilization from housing.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Net nitrogen excretion from storage, in kilograms per year.
        """
        return self.housing_class.net_excretion_HOUSED(
            animal
        ) - self.housing_class.nh3_emissions_per_year_HOUSED(animal)

    def total_ammonia_nitrogen_nh4_STORAGE(self, animal):
        """
        Calculates the total ammonia nitrogen (TAN) produced per year in storage based on net nitrogen excretion.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Total ammonia nitrogen produced per year in storage, in kilograms.
        """
        percentage_nex = 0.6

        return self.net_excretion_STORAGE(animal) * percentage_nex

    def CH4_STORAGE(self, animal):
        """
        Estimates the total methane (CH4) emissions per year from manure storage.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Methane emissions from manure storage per year, in kilograms.
        """
        return (self.housing_class.VS_HOUSED(animal) * 365) * (
            0.1 * 0.67 * self.data_manager_class.get_storage_MCF(animal.mm_storage)()
        )

    def STORAGE_N2O_direct(self, animal):
        """
        Calculates the direct nitrous oxide (N2O) emissions from nitrogen in manure storage.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Direct nitrous oxide emissions from manure storage per year, in kilograms.
        """
        return self.net_excretion_STORAGE(animal) * self.data_manager_class.get_storage_N2O(animal.mm_storage)()


    def nh3_emissions_per_year_STORAGE(self, animal):
        """
        Estimates annual ammonia (NH3) emissions from manure storage based on total ammonia nitrogen production.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Ammonia emissions from manure storage per year, in kilograms.
        """
        return (
            self.total_ammonia_nitrogen_nh4_STORAGE(animal)
            * self.data_manager_class.get_storage_TAN(animal.mm_storage)()
        )

    def STORAGE_N2O_indirect(self, animal):
        """
        Calculates indirect nitrous oxide (N2O) emissions from atmospheric deposition related to ammonia volatilization in storage.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Indirect nitrous oxide emissions from storage per year, in kilograms.
        """
        indirect_atmosphere = self.data_manager_class.get_cohort_parameter(animal.cohort, "atmospheric_deposition")()

        NH3 = self.nh3_emissions_per_year_STORAGE(animal)

        return NH3 * indirect_atmosphere


class DailySpread:
    """
    The DailySpread class focuses on the environmental impact of spreading stored manure on fields, including calculations for net nitrogen 
    excretion, ammonia nitrogen, direct and indirect nitrous oxide emissions, and nitrogen and phosphorus leaching. It's important to note 
    that while this functionality is provided, solid manure from sheep is often not spread to pasture in Ireland.

    Attributes:
        data_manager_class (LCADataManager): Provides access to necessary data for calculations.
        storage_class (StorageStage): Allows access to calculations from the storage stage for use in spreading calculations.
    
    Methods:
        net_excretion_SPREAD(animal): Calculates the net nitrogen excretion from daily spreading.
        total_ammonia_nitrogen_nh4_SPREAD(animal): Calculates total ammonia nitrogen from daily spreading.
        SPREAD_N2O_direct(animal): Estimates direct nitrous oxide emissions from daily spreading.
        nh3_emissions_per_year_SPREAD(animal): Estimates annual ammonia emissions from daily spreading.
        leach_nitrogen_SPREAD(animal): Estimates the amount of nitrogen leached from daily spreading.
        leach_phosphorous_SPREAD(animal): Estimates the amount of phosphorus leached from daily spreading.
        SPREAD_N2O_indirect(animal): Calculates indirect nitrous oxide emissions from daily spreading.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.storage_class = StorageStage(ef_country)

    def net_excretion_SPREAD(self, animal):
        """
        Calculates the net nitrogen excretion from spreading, accounting for nitrogen loss in storage and emissions.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Net nitrogen excretion from daily spreading, in kilograms per year.
        """
        nex_storage = self.net_excretion_STORAGE(animal)
        direct_n2o = self.STORAGE_N2O_direct(animal)
        nh3_emissions = self.nh3_emissions_per_year_STORAGE(animal)
        indirect_n2o = self.STORAGE_N2O_indirect(animal)

        return nex_storage - direct_n2o - nh3_emissions - indirect_n2o

    def total_ammonia_nitrogen_nh4_SPREAD(self, animal):
        """
        Calculates the total ammonia nitrogen (TAN) produced from daily spreading.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Total ammonia nitrogen produced from daily spreading, in kilograms per year.
        """
        percentage_nex = 0.6

        return self.net_excretion_SPREAD(animal) * percentage_nex


    def SPREAD_N2O_direct(self, animal):
        """
        Estimates the direct nitrous oxide (N2O) emissions from daily spreading.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Direct nitrous oxide emissions from daily spreading, in kilograms per year.
        """
        return self.net_excretion_SPREAD(animal) * self.data_manager_class.get_cohort_parameter(animal.cohort, "direct_soil_n2o")()


    def nh3_emissions_per_year_SPREAD(self, animal):
        """
        Estimates annual ammonia (NH3) emissions from daily spreading.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Ammonia emissions from daily spreading, in kilograms per year.
        """
        nh4 = self.total_ammonia_nitrogen_nh4_SPREAD(animal)

        return nh4 * self.data_manager_class.get_daily_spreading(animal.daily_spreading)()

    def leach_nitrogen_SPREAD(self, animal):
        """
        Estimates the amount of nitrogen leached due to daily spreading.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Nitrogen leached from daily spreading, in kilograms per year.
        """
        ten_percent_nex = 0.1

        return self.net_excretion_SPREAD(animal) * ten_percent_nex

    def leach_phospherous_SPREAD(self, animal):
        """
        Estimates the amount of phosphorus leached due to daily spreading.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Phosphorus leached from daily spreading, in kilograms per year.
        """
        return (self.net_excretion_SPREAD(animal) * (1.8 / 5)) * 0.03

    def SPREAD_N2O_indirect(self, animal):
        """
        Calculates indirect nitrous oxide (N2O) emissions from atmospheric deposition and leaching related to daily spreading.

        Parameters:
            animal (object): The animal instance for which the calculation is made.

        Returns:
            float: Indirect nitrous oxide emissions from daily spreading, in kilograms per year.
        """
        indirect_atmosphere = self.data_manager_class.get_cohort_parameter(animal.cohort, "atmospheric_deposition")()
        indirect_leaching = self.data_manager_class.get_cohort_parameter(animal.cohort, "leaching")()

        NH3 = self.nh3_emissions_per_year_SPREAD(animal)
        NL = self.leach_nitrogen_SPREAD(animal)

        return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


###############################################################################
# Farm & Upstream Emissions
###############################################################################
class FertiliserInputs:
    """
    Handles the calculations related to the environmental impact of fertiliser inputs, including urea and ammonium nitrate fertilisers. 
    It calculates direct and indirect nitrous oxide emissions, ammonia volatilisation, leaching, and carbon dioxide emissions from the 
    application of fertilisers and lime.

    Attributes:
        data_manager_class (LCADataManager): Provides access to necessary data for calculations.
    
    Methods:
        urea_N2O_direct: Calculates direct N2O emissions from urea application.
        urea_NH3: Estimates ammonia volatilised from urea application.
        urea_nleach: Calculates nitrogen leached from urea application.
        urea_N2O_indirect: Calculates indirect N2O emissions from urea application.
        urea_co2: Estimates CO2 emissions from urea application.
        lime_co2: Estimates CO2 emissions from lime application.
        urea_P_leach: Calculates phosphorus leached from urea application.
        n_fertiliser_P_leach: Calculates phosphorus leached from nitrogen fertiliser application.
        n_fertiliser_direct: Calculates direct N2O emissions from ammonium nitrate fertiliser application.
        n_fertiliser_NH3: Estimates ammonia volatilised from ammonium nitrate fertiliser application.
        n_fertiliser_nleach: Calculates nitrogen leached from ammonium nitrate fertiliser application.
        n_fertiliser_indirect: Calculates indirect N2O emissions from ammonium nitrate fertiliser application.
        p_fertiliser_P_leach: Calculates phosphorus leached from phosphorus fertiliser application.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)

    # Urea Fertiliser
    def urea_N2O_direct(self, total_urea, total_urea_abated):
        """
        Calculates the direct N2O emissions from the application of urea and urea treated with nitrification inhibitors (abated urea) to soils.

        Parameters:
            total_urea (float): The total amount of urea applied, in kilograms.
            total_urea_abated (float): The total amount of abated urea applied, in kilograms.

        Returns:
            float: Total direct N2O emissions from urea and abated urea application, in kilograms.
        """
        ef_urea = self.data_manager_class.get_ef_urea()
        ef_urea_abated = self.data_manager_class.get_ef_urea_abated()

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)

    def urea_NH3(self, total_urea, total_urea_abated):
        """
        Estimates the amount of NH3 volatilized from both standard and abated urea applications.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total NH3 emissions (kg).
        """
        ef_urea = (
            self.data_manager_class.get_ef_urea_to_nh3_and_nox()
        )
        ef_urea_abated = (
            self.data_manager_class.get_ef_urea_abated_to_nh3_and_nox()
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)

    def urea_nleach(self, total_urea, total_urea_abated):
        """
        Calculates the amount of urea and abated urea leached from soils after application.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total leached urea (kg).
        """
        leach = self.data_manager_class.get_ef_fration_leach_runoff()

        return (total_urea + total_urea_abated) * leach

    def urea_N2O_indirect(self, total_urea, total_urea_abated):
        """
        Calculates indirect emissions from urea and abated urea application, considering atmospheric deposition and leaching.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total indirect N2O emissions (kg).
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )
        indirect_leaching = (
            self.data_manager_class.get_indirect_leaching()
        )

        return (self.urea_NH3(total_urea, total_urea_abated) * indirect_atmosphere) + (
            self.urea_nleach(total_urea, total_urea_abated) * indirect_leaching
        )

    def urea_co2(self, total_urea):
        """
        Calculates the total CO2 emissions resulting from the application of urea.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).

        Returns:
            float: Total CO2 emissions (kg).
        """
        ef_urea_co2 = float(self.data_manager_class.get_ef_urea_co2())

        return (total_urea  * ef_urea_co2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation


    def lime_co2(self, total_lime):
        """
        Calculates total CO2 emissions from the application of lime.

        Parameters:
            total_lime (float): Total amount of lime applied (kg).

        Returns:
            float: Total CO2 emissions from lime application (kg).
        """
        ef_lime_co2 = float(self.data_manager_class.get_ef_lime_co2())

        return (total_lime * ef_lime_co2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation


    def urea_P_leach(self, total_urea, total_urea_abated):
        """
        Calculates the amount of phosphorus leached from urea and abated urea application.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total phosphorus leached (kg).
        """
        frac_leach = float(self.data_manager_class.get_frac_p_leach())

        return (total_urea + total_urea_abated) * frac_leach

    # Nitrogen Fertiliser Emissions

    def n_fertiliser_P_leach(self, total_n_fert):
        """
        Calculates the amount of phosphorus leached due to the application of nitrogen fertilisers.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total phosphorus leached due to nitrogen fertiliser application (kg).
        """
        frac_leach = float(self.data_manager_class.get_frac_p_leach())

        return total_n_fert * frac_leach

    def n_fertiliser_direct(self, total_n_fert):
        """
        Calculates direct N2O emissions resulting from the application of nitrogen fertilisers at field level.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total direct N2O emissions from nitrogen fertiliser application (kg).
        """
        ef = self.data_manager_class.get_ef_AN_fertiliser()
        return total_n_fert * ef

    def n_fertiliser_NH3(self, total_n_fert):
        """
        Calculates total NH3 emissions resulting from the application of nitrogen fertilisers at field level.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total NH3 emissions from nitrogen fertiliser application (kg).
        """
        ef = (
            self.data_manager_class.get_ef_AN_fertiliser_to_nh3_and_nox()
        )
        return total_n_fert * ef

    def n_fertiliser_nleach(self, total_n_fert):
        """
        Calculates the total nitrogen leached from the application of nitrogen fertilisers at field level.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total nitrogen leached from nitrogen fertiliser application (kg).
        """
        ef = self.data_manager_class.get_ef_fration_leach_runoff()

        return total_n_fert * ef

    def n_fertiliser_indirect(self, total_n_fert):
        """
        Calculates the indirect N2O emissions from the use of nitrogen fertilisers, accounting for atmospheric deposition and leaching.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total indirect N2O emissions from nitrogen fertiliser application (kg).
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )
        indirect_leaching = (
            self.data_manager_class.get_indirect_leaching()
        )

        return (self.n_fertiliser_NH3(total_n_fert) * indirect_atmosphere) + (
            self.n_fertiliser_nleach(total_n_fert) * indirect_leaching
        )
    

    def total_fertiliser_N20(self, total_urea, total_urea_abated, total_n_fert):
        """
        Returns the total N2O emissions, both direct and indirect, from the application of both urea and ammonium nitrate fertilisers.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total N2O emissions from all fertiliser applications (kg).
        """
        result = (
            self.urea_N2O_direct(total_urea, total_urea_abated)
            + self.urea_N2O_indirect(total_urea, total_urea_abated)
        ) + (
            self.n_fertiliser_direct(total_n_fert)
            + self.n_fertiliser_indirect(total_n_fert)
        )

        return result
    

    def p_fertiliser_P_leach(self, total_p_fert):
        """
        Calculates the amount of phosphorus leached due to the application of phosphorus fertilisers.

        Parameters:
            total_p_fert (float): Total amount of phosphorus fertiliser applied (kg).

        Returns:
            float: Total phosphorus leached from phosphorus fertiliser application (kg).
        """
        frac_leach = float(self.data_manager_class.get_frac_p_leach())

        return total_p_fert * frac_leach


################################################################################
# Total Global Warming Potential of whole farms (Upstream Processes & Fossil Fuel Energy)
################################################################################

# Emissions from on Farm Fossil Fuels


class Upstream:
    """
    Handles the calculation of upstream emissions related to concentrate production, diesel usage, and electricity consumption 
    for the environmental impact assessment of sheep farming operations. It focuses on CO2 and PO4 emissions from various 
    sources including fertiliser production, diesel fuel, and electricity used in farm operations.

    Attributes:
        data_manager_class (LCADataManager): Provides access to necessary data for calculations.

    Methods:
        co2_from_concentrate_production: Calculates CO2 emissions from concentrate production for sheep.
        po4_from_concentrate_production: Calculates PO4 emissions from concentrate production for sheep.
        diesel_CO2: Estimates CO2 emissions from diesel fuel usage.
        diesel_PO4: Estimates PO4 emissions from diesel fuel usage.
        elec_CO2: Calculates CO2 emissions from electricity consumption.
        elec_PO4: Calculates PO4 emissions from electricity consumption.
        fert_upstream_CO2: Estimates CO2 emissions from the production of various fertilisers.
        fert_upstream_EP: Estimates PO4 emissions from the production of various fertilisers.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)

    def co2_from_concentrate_production(self, animal):
        """
        Calculates CO2e emissions from the production of concentrates consumed by the animal cohorts.

        Parameters:
            animal (object): An object containing data about different animal cohorts and their concentrate consumption.

        Returns:
            float: The total CO2e emissions from concentrate production for all animal cohorts (kg/year).
        """
        concentrate_co2 = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                concentrate_co2 += (
                    animal.__getattribute__(key).con_amount
                    * self.data_manager_class.get_upstream_concentrate_co2e(
                        animal.__getattribute__(key).con_type
                    )
                ) * animal.__getattribute__(key).pop

        return concentrate_co2 * 365


        # Imported Feeds
    def po4_from_concentrate_production(self, animal):
        """
        Calculates phosphorus (PO4e) emissions from the production of concentrates consumed by the animal cohorts.

        Parameters:
            animal (object): An object containing data about different animal cohorts and their concentrate consumption.

        Returns:
            float: The total PO4e emissions from concentrate production for all animal cohorts (kg/year).
        """
        concentrate_p = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                concentrate_p += (
                    animal.__getattribute__(key).con_amount
                    * self.data_manager_class.get_upstream_concentrate_po4e(
                        animal.__getattribute__(key).con_type
                    )
                ) * animal.__getattribute__(key).pop

        return concentrate_p * 365


    def diesel_CO2(self, diesel_kg):
        """
        Calculates CO2e emissions from diesel consumption, including both direct and indirect upstream emissions.

        Parameters:
            diesel_kg (float): The amount of diesel consumed (kg).

        Returns:
            float: The total CO2e emissions from diesel consumption (kg).
        """
        Diesel_indir = self.data_manager_class.get_upstream_diesel_co2e_indirect()
        Diest_dir = self.data_manager_class.get_upstream_diesel_co2e_direct()

        return diesel_kg * (Diest_dir + Diesel_indir)
    

    def diesel_PO4(self, diesel_kg):
        """
        Calculates phosphorus (PO4e) emissions from diesel consumption, including both direct and indirect upstream emissions.

        Parameters:
            diesel_kg (float): The amount of diesel consumed (kg).

        Returns:
            float: The total PO4e emissions from diesel consumption (kg).
        """
        Diesel_indir = self.data_manager_class.get_upstream_diesel_po4e_indirect()
        Diest_dir = self.data_manager_class.get_upstream_diesel_po4e_direct()

        return diesel_kg * (Diest_dir + Diesel_indir)

    def elec_CO2(self, elec_kwh):
        """
        Calculates CO2e emissions from electricity consumption.

        Parameters:
            elec_kwh (float): The amount of electricity consumed (kWh).

        Returns:
            float: The total CO2e emissions from electricity consumption (kg).
        """
        elec_consumption = self.data_manager_class.get_upstream_electricity_co2e() # based on Norway hydropower
        return elec_kwh * elec_consumption


    def elec_PO4(self, elec_kwh):
        """
        Calculates phosphorus emissions (PO4e) from electricity consumption.

        Parameters:
            elec_kwh (float): The amount of electricity consumed (kWh).

        Returns:
            float: The total PO4e emissions from electricity consumption (kg).
        """
        elec_consumption = self.data_manager_class.get_upstream_electricity_po4e() # based on Norway hydropower
        return elec_kwh * elec_consumption
    

    # Emissions from upstream fertiliser production
    def fert_upstream_CO2(
        self, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert
    ):
        """
        Calculates the total upstream CO2e emissions from the production of various fertilizers.

        Parameters:
            total_n_fert (float): Total nitrogen fertilizer applied (kg).
            total_urea (float): Total urea applied (kg).
            total_urea_abated (float): Total abated urea applied (kg).
            total_p_fert (float): Total phosphorus fertilizer applied (kg).
            total_k_fert (float): Total potassium fertilizer applied (kg).
            total_lime_fert (float): Total lime fertilizer applied (kg).

        Returns:
            float: The total upstream CO2e emissions from fertilizer production (kg).
        """
        AN_fert_CO2 = self.data_manager_class.get_upstream_AN_fertiliser_co2e() # Ammonium Nitrate Fertiliser
        Urea_fert_CO2 = self.data_manager_class.get_upstream_urea_fertiliser_co2e()
        Triple_superphosphate = self.data_manager_class.get_upstream_triple_phosphate_co2e()
        Potassium_chloride = self.data_manager_class.get_upstream_potassium_chloride_co2e()
        Lime = self.data_manager_class.get_upstream_lime_co2e()

        return (
            (total_n_fert * AN_fert_CO2)
            + (total_urea * Urea_fert_CO2)
            + (total_urea_abated * Urea_fert_CO2)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
            + (total_lime_fert * Lime)
        )

    def fert_upstream_EP(
        self, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert
    ):
        """
        Calculates the total upstream emissions (PO4e) from the production of various fertilizers.

        Parameters:
            total_n_fert (float): Total nitrogen fertilizer applied (kg).
            total_urea (float): Total urea applied (kg).
            total_urea_abated (float): Total abated urea applied (kg).
            total_p_fert (float): Total phosphorus fertilizer applied (kg).
            total_k_fert (float): Total potassium fertilizer applied (kg).
            total_lime_fert (float): Total lime fertilizer applied (kg).

        Returns:
            float: The total upstream emissions (PO4e) from fertilizer production (kg).
        """
        AN_fert_PO4 = self.data_manager_class.get_upstream_AN_fertiliser_po4e()# Ammonium Nitrate Fertiliser
        Urea_fert_PO4 = self.data_manager_class.get_upstream_urea_fertiliser_po4e()
        Triple_superphosphate = self.data_manager_class.get_upstream_triple_phosphate_po4e()
        Potassium_chloride = self.data_manager_class.get_upstream_potassium_chloride_po4e()
        Lime = self.data_manager_class.get_upstream_lime_po4e()

        return (
            (total_n_fert * AN_fert_PO4)
            + (total_urea * Urea_fert_PO4)
            + (total_urea_abated * Urea_fert_PO4)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
            + (total_lime_fert * Lime)
        )


################################################################################
# Allocation
################################################################################
class Allocation:
    """
    The Allocation class is designed to compute the economic value of outputs from sheep farming activities, including the value
    derived from lambs, sheep, and wool. It calculates the economic allocation factors for these outputs.

    Attributes:
        None explicitly defined within the class but requires animal objects with specific attributes for calculations.

    Methods:
        lamb_live_weight_output_value: Calculates the total economic value from the sale of lambs based on their live weight and sale price.
        sheep_live_weight_output_value: Calculates the total economic value from the sale of adult sheep based on their live weight and sale price.
        wool_output_value: Computes the total economic value from wool production.
        live_weight_bought: Calculates the total live weight of sheep and lambs bought.
        total_lamb_live_weight_kg: Sums up the total live weight of all lambs.
        total_sheep_live_weight_kg: Sums up the total live weight of all adult sheep.
        total_wool_weight_kg: Calculates the total weight of wool produced.
        lamb_allocation_factor: Determines the proportion of economic value attributed to lambs relative to total output value.
        sheep_allocation_factor: Determines the proportion of economic value attributed to adult sheep relative to total output value.
        wool_allocation_factor: Determines the proportion of economic value attributed to wool relative to total output value.
    """
    def lamb_live_weight_output_value(self, animal):
        """
        Calculates the economic value of lambs based on their live weight and the market price per kilogram.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total economic value from the sale of lambs.
        """
        return (
            (
                (animal.lamb_less_1_yr.weight * animal.lamb_less_1_yr.n_sold)
                * animal.lamb_less_1_yr.meat_price_kg
            )
            + (
                (animal.lamb_more_1_yr.weight * animal.lamb_more_1_yr.n_sold)
                * animal.lamb_more_1_yr.meat_price_kg
            )
            + (
                (animal.male_less_1_yr.weight * animal.male_less_1_yr.n_sold)
                * animal.male_less_1_yr.meat_price_kg
            )
        )

    def sheep_live_weight_output_value(self, animal):
        """
        Calculates the economic value generated of adult sheep (ewes and rams) based on their live weight and the market price per kilogram.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total economic value from the sale of adult sheep.
        """
        return (
            (animal.ewes.weight * animal.ewes.n_sold) * animal.ewes.meat_price_kg
        ) + ((animal.ram.weight * animal.ram.n_sold) * animal.ram.meat_price_kg)

    def wool_output_value(self, animal):
        """
        Computes the total economic value derived from wool based on the quantity of wool produced and the market price per kilogram.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total economic value from wool production.
        """
        return (
            (
                (animal.lamb_less_1_yr.wool * animal.lamb_less_1_yr.wool_price_kg)
                * (animal.lamb_less_1_yr.pop - animal.lamb_less_1_yr.n_sold)
            )
            + (
                (animal.lamb_more_1_yr.wool * animal.lamb_more_1_yr.wool_price_kg)
                * (animal.lamb_more_1_yr.pop - animal.lamb_more_1_yr.n_sold)
            )
            + (
                (animal.male_less_1_yr.wool * animal.male_less_1_yr.wool_price_kg)
                * (animal.male_less_1_yr.pop - animal.male_less_1_yr.n_sold)
            )
            + (
                (animal.ewes.wool * animal.ewes.wool_price_kg)
                * (animal.ewes.pop - animal.ewes.n_sold)
            )
            + (
                (animal.ram.wool * animal.ram.wool_price_kg)
                * (animal.ram.pop - animal.ram.n_sold)
            )
        )

    def live_weight_bought(self, animal):
        """
        Calculates the total live weight of sheep and lambs bought.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total live weight of sheep and lambs bought, in kilograms.
        """
        return (
            (animal.ewes.weight * animal.ewes.n_bought)
            + (animal.lamb_less_1_yr.weight * animal.lamb_less_1_yr.n_bought)
            + (animal.lamb_more_1_yr.weight * animal.lamb_more_1_yr.n_bought)
            + (animal.male_less_1_yr.weight * animal.male_less_1_yr.n_bought)
            + (animal.ram.weight * animal.ram.n_bought)
        )

    def total_lamb_live_weight_kg(self, animal):
        """
        Summarizes the total live weight of all lambs.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total live weight of lambs, in kilograms.
        """
        return (
            (animal.lamb_less_1_yr.weight * animal.lamb_less_1_yr.n_sold)
            + (animal.lamb_more_1_yr.weight * animal.lamb_more_1_yr.n_sold)
            + (animal.male_less_1_yr.weight * animal.male_less_1_yr.n_sold)
        )

    def total_sheep_live_weight_kg(self, animal):
        """
        Computes the total live weight of adult sheep.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total live weight of adult sheep, in kilograms.
        """
        return (animal.ewes.weight * animal.ewes.n_sold) + (
            animal.ram.weight * animal.ram.n_sold
        )

    def total_wool_weight_kg(self, animal):
        """
        Calculates the total weight of wool produced.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Total weight of wool produced, in kilograms.
        """
        return (
            (
                animal.lamb_less_1_yr.wool
                * (animal.lamb_less_1_yr.pop - animal.lamb_less_1_yr.n_sold)
            )
            + (
                animal.lamb_more_1_yr.wool
                * (animal.lamb_more_1_yr.pop - animal.lamb_more_1_yr.n_sold)
            )
            + (
                animal.male_less_1_yr.wool
                * (animal.male_less_1_yr.pop - animal.male_less_1_yr.n_sold)
            )
            + (animal.ewes.wool * (animal.ewes.pop - animal.ewes.n_sold))
            + (animal.ram.wool * (animal.ram.pop - animal.ram.n_sold))
        )

    def lamb_allocation_factor(self, animal):
        """
        Determines the economic allocation factor for lambs.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Economic allocation factor for lambs, as a proportion of the total output value.
        """        
        total = (
            self.lamb_live_weight_output_value(animal)
            + self.sheep_live_weight_output_value(animal)
            + self.wool_output_value(animal)
        )
        return self.lamb_live_weight_output_value(animal) / total


    def sheep_allocation_factor(self, animal):
        """
        Identifies the economic allocation factor for adult sheep.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Economic allocation factor for adult sheep, as a proportion of the total output value.
        """        
        total = (
            self.lamb_live_weight_output_value(animal)
            + self.sheep_live_weight_output_value(animal)
            + self.wool_output_value(animal)
        )
        return self.sheep_live_weight_output_value(animal) / total

    def wool_allocation_factor(self, animal):
        """
        Calculates the economic allocation factor for wool.

        Parameters:
            animal (Animal): The animal instance for which the calculation is made.

        Returns:
            float: Economic allocation factor for wool, as a proportion of the total output value.
        """        
        total = (
            self.lamb_live_weight_output_value(animal)
            + self.sheep_live_weight_output_value(animal)
            + self.wool_output_value(animal)
        )
        return self.wool_output_value(animal) / total


################################################################################
# Total Global Warming Potential of whole farms
################################################################################


class ClimateChangeTotals:
    """
    This class calculates total greenhouse gas emissions associated with various farm activities 
    including enteric fermentation, manure management, soil management, and the upstream 
    impacts of fuel and feed production. It utilizes data from various other classes to 
    accumulate total emissions related to climate change.

    Attributes:
        data_manager_class (LCADataManager): Manages lifecycle assessment data.
        grass_feed_class (GrassFeed): Manages grass feed-related calculations.
        grazing_class (GrazingStage): Manages grazing-related calculations.
        spread_class (DailySpread): Manages nutrient spreading-related calculations.
        housing_class (HousingStage): Manages housing-related calculations.
        storage_class (StorageStage): Manages manure storage-related calculations.
        fertiliser_class (FertiliserInputs): Manages fertiliser input-related calculations.
        upstream_class (Upstream): Manages upstream emissions calculations.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.grass_feed_class = GrassFeed(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)

    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary template for emissions calculations with zero-initialized values.

        Parameters:
            keys (list): List of animal cohorts or other categories for emissions calculation.

        Returns:
            dict: A dictionary of dictionaries for organizing emissions data.
        """
        key_list = [
            "enteric_ch4",
            "manure_management_N2O",
            "manure_management_CH4",
            "manure_applied_N",
            "N_direct_PRP",
            "N_direct_PRP",
            "N_indirect_PRP",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soil_organic_N_direct",
            "soil_organic_N_indirect",
            "soil_inorganic_N_direct",
            "soil_inorganic_N_indirect",
            "soil_histosol_N_direct",
            "crop_residue_direct",
            "soil_N_direct",
            "soil_N_indirect",
            "soils_N2O",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    

    def create_expanded_emissions_dictionary(self, keys):
        """
        Extends the basic emissions dictionary template with additional categories for more 
        detailed emissions calculations.

        Parameters:
            keys (list): List of animal cohorts or other categories for detailed emissions calculation.

        Returns:
            dict: An expanded dictionary of dictionaries for organizing detailed emissions data.
        """
        key_list = [
            "enteric_ch4",
            "manure_management_N2O",
            "manure_management_CH4",
            "manure_applied_N",
            "N_direct_PRP",
            "N_direct_PRP",
            "N_indirect_PRP",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soil_organic_N_direct",
            "soil_organic_N_indirect",
            "soil_inorganic_N_direct",
            "soil_inorganic_N_indirect",
            "soil_N_direct",
            "soil_N_indirect",
            "soil_histosol_N_direct",
            "crop_residue_direct",
            "soils_N2O",
            "upstream_fuel_fert",
            "upstream_feed",
            "upstream",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    

    def Enteric_CH4(self, animal):
        """
        Calculates methane emissions from enteric fermentation for a given animal.

        Parameters:
            animal (AnimalCategory): The animal cohort for which emissions are being calculated.

        Returns:
            float: Total methane emissions from enteric fermentation for the specified animal (kg CH4).
        """
        return self.grass_feed_class.ch4_emissions_factor(animal)

    def CH4_enteric_ch4(self, animal):
        """
        Accumulates total methane emissions from enteric fermentation across all animal cohorts.

        Parameters:
            animal (AnimalCollection): Collection of animal cohorts within the farm system.

        Returns:
            float: Total methane emissions from enteric fermentation across all cohorts (kg CH4).
        """
        Enteric = 0

        for key in animal.__dict__.keys():

            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                Enteric += (
                    self.Enteric_CH4(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return Enteric

    def CH4_manure_management(self, animal):
        """
        Calculates methane emissions from manure management for animal cohorts.

        Parameters:
            animal (AnimalCollection): Collection of animal cohorts within the farm system.

        Returns:
            float: Total methane emissions from manure management across all cohorts (kg CH4).
        """
        result = 0

        for key in animal.__dict__.keys():

            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                result += (
                    self.Total_manure_ch4(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return result

    def PRP_Total(self, animal):
        """
        Calculates the total N2O emissions related to Pasture, Range, and Paddock (PRP) for a given animal.

        Parameters:
            animal (AnimalCategory): The animal cohort for which emissions are being calculated.

        Returns:
            float: Total N2O emissions from PRP for the specified animal.
        """
        return self.grazing_class.PRP_N2O_direct(
            animal
        ) + self.grazing_class.PRP_N2O_indirect(animal)

    def Total_storage_N2O(self, animal):
        """
        Calculates the total N2O emissions related to the storage of manure for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal collection for which emissions are being calculated.

        Returns:
            float: Total N2O emissions from manure storage for the specified animal collection.
        """
        mole_weight = 44.0 / 28.0

        n2o_direct = 0
        n2o_indirect_storage = 0
        n2o_indirect_housing = 0

        for key in animal.__dict__.keys():

            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                n2o_direct += (
                    self.storage_class.STORAGE_N2O_direct(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )
                n2o_indirect_storage += (
                    self.storage_class.STORAGE_N2O_indirect(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )
                n2o_indirect_housing += (
                    self.housing_class.HOUSING_N2O_indirect(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )

        return (n2o_direct + n2o_indirect_storage + n2o_indirect_housing) * mole_weight
    

    def N2O_total_PRP_N2O_direct(self, animal):
        """
        Calculates the direct N2O emissions from pasture, range, and paddock for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal cohort collection for which emissions are being calculated.

        Returns:
            float: Direct N2O emissions from PRP for the specified animal collection.
        """
        mole_weight = 44.0 / 28.0

        PRP_direct = 0

        for key in animal.__dict__.keys():

            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                PRP_direct += (
                    self.grazing_class.PRP_N2O_direct(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PRP_direct * mole_weight

    def N2O_total_PRP_N2O_indirect(self, animal):
        """
        Calculates the indirect N2O emissions from pasture, range, and paddock for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal cohort collection for which emissions are being calculated.

        Returns:
            float: Indirect N2O emissions from PRP for the specified animal collection.
        """
        mole_weight = 44.0 / 28.0

        PRP_indirect = 0

        for key in animal.__dict__.keys():

            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                PRP_indirect += (
                    self.grazing_class.PRP_N2O_indirect(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PRP_indirect * mole_weight

    def Total_manure_ch4(self, animal):
        """
        Calculates the total methane emissions related to manure management for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal collection for which emissions are being calculated.

        Returns:
            float: Total methane emissions from manure management for the specified animal collection.
        """
        return self.grazing_class.ch4_emissions_for_grazing(
            animal
        ) + self.storage_class.CH4_STORAGE(animal)

    def CO2_soils_GWP(self, total_urea, total_lime):
        """
        Calculates the global warming potential from CO2 emissions related to soil management through urea and lime application.

        Parameters:
            total_urea (float): Total amount of urea used (kg).
            total_lime (float): Total amount of lime used (kg).

        Returns:
            float: CO2 emissions from soil management.
        """
        return self.fertiliser_class.urea_co2(total_urea) + self.fertiliser_class.lime_co2(total_lime)

    def N2O_direct_fertiliser(self, total_urea, total_urea_abated, total_n_fert):
        """
        Calculates the total direct N2O emissions from urea and ammonium fertilizers.

        Parameters:
            total_urea (float): Total amount of urea used (kg).
            total_urea_abated (float): Total amount of urea with emissions-reducing treatments applied (kg).
            total_n_fert (float): Total amount of nitrogen fertilizer used (kg).

        Returns:
            float: Total direct N2O emissions from fertilizer application.
        """
        result = (
            (
                self.fertiliser_class.urea_N2O_direct(total_urea, total_urea_abated)
                + self.fertiliser_class.n_fertiliser_direct(total_n_fert)
            )
            * 44.0
            / 28.0
        )

        return result

    def N2O_fertiliser_indirect(self, total_urea, total_urea_abated, total_n_fert):
        """
        Calculates the total indirect N2O emissions from urea and ammonium fertilizers.

        Parameters:
            total_urea (float): Total amount of urea used (kg).
            total_urea_abated (float): Total amount of urea with emissions-reducing treatments applied (kg).
            total_n_fert (float): Total amount of nitrogen fertilizer used (kg).

        Returns:
            float: Total indirect N2O emissions from fertilizer application.
        """
        result = (
            (
                self.fertiliser_class.urea_N2O_indirect(total_urea, total_urea_abated)
                + self.fertiliser_class.n_fertiliser_indirect(total_n_fert)
            )
            * 44.0
            / 28.0
        )

        return result

    def upstream_and_inputs_and_fuel_co2(
        self,
        diesel_kg,
        elec_kwh,
        total_n_fert,
        total_urea,
        total_urea_abated,
        total_p_fert,
        total_k_fert,
        total_lime_fert,
    ):
        """
        Calculates the total CO2 emissions from various upstream activities and inputs. 
        This includes emissions from the use of diesel, electricity, and different types of fertilizers. 

        Parameters:
        - diesel_kg: The amount of diesel used, in kilograms.
        - elec_kwh: The amount of electricity consumed, in kilowatt-hours.
        - total_n_fert: The total amount of nitrogen fertilizer used, in kilograms.
        - total_urea: The total amount of urea used, in kilograms.
        - total_urea_abated: The total amount of abated urea (urea treated to reduce emissions) used, in kilograms.
        - total_p_fert: The total amount of phosphorus fertilizer used, in kilograms.
        - total_k_fert: The total amount of potassium fertilizer used, in kilograms.
        - total_lime_fert: The total amount of lime fertilizer used, in kilograms.

        Returns:
        Total CO2 emissions from all specified sources, measured in equivalent kilograms of CO2.
        """
        return (
            self.upstream_class.diesel_CO2(diesel_kg)
            + self.upstream_class.elec_CO2(elec_kwh)
            + self.upstream_class.fert_upstream_CO2(
                total_n_fert,
                total_urea,
                total_urea_abated,
                total_p_fert,
                total_k_fert,
                total_lime_fert,
            )
        )
    
    def co2_from_concentrate_production(self, animal):
        """
        Calculates the CO2e emissions from the production of concentrates fed to the animal.
        This function looks at the type and amount of concentrate feed and uses predefined emission factors to estimate the CO2e impact.

        Parameters:
        - animal: The animal collection for which the CO2e emissions are being calculated.
        This object should contain the type and amount of concentrate feed consumed.

        Returns:
        The total CO2e emissions from the production of concentrate feed, measured in equivalent kilograms of CO2.

        """
        return self.upstream_class.co2_from_concentrate_production(animal)


###############################################################################
# Water Quality EP PO4e
###############################################################################


class EutrophicationTotals:
    """
    A class responsible for calculating the total eutrophication potential associated with a given farming operation. 
    This includes contributions from manure management, soil management, fertiliser application, and upstream processes 
    related to feed and fuel production.

    Attributes:
        data_manager_class (LCADataManager): An instance of the LCADataManager class to access necessary emission factors and conversion values.
        grazing_class (GrazingStage): An instance of the GrazingStage class to access grazing-related eutrophication contributions.
        housing_class (HousingStage): An instance of the HousingStage class to access housing-related eutrophication contributions.
        storage_class (StorageStage): An instance of the StorageStage class to access storage-related eutrophication contributions.
        spread_class (DailySpread): An instance of the DailySpread class to access spreading-related eutrophication contributions.
        fertiliser_class (FertiliserInputs): An instance of the FertiliserInputs class to access fertiliser-related eutrophication contributions.
        upstream_class (Upstream): An instance of the Upstream class to access upstream-related eutrophication contributions.

    Methods:
        create_emissions_dictionary(keys): Creates a structured dictionary for tracking eutrophication emissions.
        create_expanded_emissions_dictionary(keys): Creates a more detailed structured dictionary for tracking eutrophication emissions, including upstream processes.
        total_manure_NH3_EP(animal): Calculates the total ammonia emissions from manure management, converted to phosphate equivalents.
        total_fertiliser_soils_NH3_and_LEACH_EP(total_urea, total_urea_abated, total_n_fert): Calculates total ammonia and leaching from fertiliser application to soils, converted to phosphate equivalents.
        total_grazing_soils_NH3_and_LEACH_EP(animal): Calculates total ammonia and leaching from grazing management to soils, converted to phosphate equivalents.
        fertiliser_soils_P_LEACH_EP(total_urea, total_urea_abated, total_n_fert, total_p_fert): Calculates total phosphorus leaching from fertiliser application, contributing to eutrophication.
        grazing_soils_P_LEACH_EP(animal): Calculates total phosphorus leaching from grazing, contributing to eutrophication.
        total_fertilser_soils_EP(total_urea, total_urea_abated, total_n_fert, total_p_fert): Aggregates total eutrophication potential from fertiliser applications to soils.
        total_grazing_soils_EP(animal): Aggregates total eutrophication potential from grazing management.
        upstream_and_inputs_and_fuel_po4(diesel_kg, elec_kwh, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert): Calculates total eutrophication potential from upstream activities and inputs, including fuel and electricity usage.
        po4_from_concentrate_production(animal): Calculates total phosphorus emissions from concentrate production used in animal diets.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)
    
    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary to store eutrophication emissions data for different categories.
        
        Parameters:
            keys: A list of keys representing different farm activities or emission sources.
        
        Returns:
            A dictionary with initialized values for each key and sub-key.
        """
        key_list = [
            "manure_management",
            "soils",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    

    def create_expanded_emissions_dictionary(self, keys):
        """
        Creates an expanded dictionary to store detailed eutrophication emissions data.
        
        Parameters:
            keys: A list of keys representing different farm activities or emission sources.
        
        Returns:
            An expanded dictionary with initialized values for each category and sub-category.
        """
        key_list = [
            "manure_management",
            "soils",
            "upstream_fuel_fert",
            "upstream_feed",
            "upstream",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict

    # Manure Management
    def total_manure_NH3_EP(self, animal):
        """
        Calculates total ammonia emissions from manure, converted to equivalent phosphorus, contributing to eutrophication potential.
        
        Parameters:
            animal: Animal data object containing manure emission details.
        
        Returns:
            Total ammonia emissions from manure management converted to phosphorus equivalent.
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                NH3N += (
                    self.storage_class.nh3_emissions_per_year_STORAGE(
                        animal.__getattribute__(key)
                    )
                    + self.housing_class.nh3_emissions_per_year_HOUSED(
                        animal.__getattribute__(key)
                    )
                ) * animal.__getattribute__(key).pop

        return (NH3N * indirect_atmosphere) * 0.42

    # SOILS
    def total_fertiliser_soils_NH3_and_LEACH_EP(
        self, total_urea, total_urea_abated, total_n_fert
    ):
        """
        Calculates total ammonia and leaching emissions from fertilizer application, converted to phosphorus equivalent.
        
        Parameters:
            total_urea: Total amount of urea applied.
            total_urea_abated: Total amount of urea with abatement measures applied.
            total_n_fert: Total amount of nitrogen fertilizers applied.
        
        Returns:
            Total ammonia and leaching emissions from fertilizers, converted to phosphorus equivalent.
        """
        LEACH = 0
        NH3N = 0

        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        if total_urea != None or total_urea_abated != None or total_n_fert != None:
            LEACH = self.fertiliser_class.urea_nleach(
                total_urea, total_urea_abated
            ) + self.fertiliser_class.n_fertiliser_nleach(total_n_fert)
            NH3N = self.fertiliser_class.urea_NH3(
                total_urea, total_urea_abated
            ) + self.fertiliser_class.n_fertiliser_NH3(total_n_fert)

        return (NH3N * indirect_atmosphere) + LEACH * 0.42

    def total_grazing_soils_NH3_and_LEACH_EP(self, animal):
        """
        Calculates total ammonia and leaching emissions from grazing soils, converted to phosphorus equivalent.
        
        Parameters:
            animal: Animal data object containing grazing information.
        
        Returns:
            Total ammonia and leaching emissions from grazing, converted to phosphorus equivalent.

        Note:
            Spreading not included for sheep.
        """
        LEACH = 0
        NH3N = 0

        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                NH3N += (
                    self.grazing_class.nh3_emissions_per_year_GRAZING(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )

                # Leach from grazing, none from spread for sheep

                LEACH += (
                    self.grazing_class.Nleach_GRAZING(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return (NH3N * indirect_atmosphere) + LEACH * 0.42

    def fertiliser_soils_P_LEACH_EP(
        self, total_urea, total_urea_abated, total_n_fert, total_p_fert
    ):
        """
        Calculates phosphorus leaching from fertilizer application on soils.
        
        Parameters:
            total_urea: Total amount of urea applied.
            total_urea_abated: Total amount of urea with abatement measures applied.
            total_n_fert: Total amount of nitrogen fertilizers applied.
            total_p_fert: Total amount of phosphorus fertilizers applied.
        
        Returns:
            Total phosphorus leaching from fertilizers application.
        """
        PLEACH = 0

        PLEACH = (
            self.fertiliser_class.urea_P_leach(total_urea, total_urea_abated)
            + self.fertiliser_class.n_fertiliser_P_leach(total_n_fert)
            + self.fertiliser_class.p_fertiliser_P_leach(total_p_fert)
        )

        return PLEACH * 3.06

    def grazing_soils_P_LEACH_EP(self, animal):
        """
        Calculates phosphorus leaching from grazing soils.
        
        Parameters:
            animal: Animal data object containing grazing information.
        
        Returns:
            Total phosphorus leaching from grazing activities.
        """
        PLEACH = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                # Just leach from grazing, not from manure application
                PLEACH += (
                    self.grazing_class.PLeach_GRAZING(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PLEACH * 3.06

    def total_fertilser_soils_EP(
        self,
        total_urea,
        total_urea_abated,
        total_n_fert,
        total_p_fert,
    ):
        """
        Calculates total eutrophication potential from fertilizer application on soils.
        
        Parameters:
            total_urea, total_urea_abated, total_n_fert, total_p_fert: Amounts of different fertilizers applied.
        
        Returns:
            Total eutrophication potential from fertilizer application.
        """
        return self.total_fertiliser_soils_NH3_and_LEACH_EP(
            total_urea, total_urea_abated, total_n_fert
        ) + self.fertiliser_soils_P_LEACH_EP(
            total_urea, total_urea_abated, total_n_fert, total_p_fert
        )

    def total_grazing_soils_EP(self, animal):
        """
        Calculates total eutrophication potential from grazing soils.
        
        Parameters:
            animal: Animal data object containing grazing information.
        
        Returns:
            Total eutrophication potential from grazing activities.
        """
        return self.total_grazing_soils_NH3_and_LEACH_EP(
            animal
        ) + self.grazing_soils_P_LEACH_EP(animal)


    def upstream_and_inputs_and_fuel_po4(
        self,
        diesel_kg,
        elec_kwh,
        total_n_fert,
        total_urea,
        total_urea_abated,
        total_p_fert,
        total_k_fert,
        total_lime_fert,
    ):
        """
        Calculates total phosphorus emissions from upstream activities, inputs, and fuel related to livestock production.
        
        Parameters:
            diesel_kg, elec_kwh, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert: Quantities of inputs used.
        
        Returns:
            Total phosphorus emissions from upstream activities.
        """
        return (
            self.upstream_class.diesel_PO4(diesel_kg)
            + self.upstream_class.elec_CO2(elec_kwh)
            + self.upstream_class.fert_upstream_CO2(
                total_n_fert,
                total_urea,
                total_urea_abated,
                total_p_fert,
                total_k_fert,
                total_lime_fert,
            ))
    
    def po4_from_concentrate_production(self, animal):
        """
        Calculates the total phosphorus emissions (PO4 equivalent) resulting from the production of concentrate feeds used in animal diet.
        This method considers the entire lifecycle of concentrate production including the acquisition of raw materials, processing, and transportation.

        Parameters:
            animal: An object representing the animal cohort, containing data related to the type and amount of concentrate consumed.

        Returns:
            The total phosphorus emissions (PO4 equivalent) from concentrate production for the given animal cohort over a specified period, contributing to the eutrophication potential of the system.
        """
        return self.upstream_class.po4_from_concentrate_production(animal)

###############################################################################
# Air Quality Ammonia
###############################################################################


class AirQualityTotals:
    """
    This class calculates the total ammonia (NH3) emissions contributing to air quality impacts from various 
    farm management practices including manure management, soil management, and fertilization strategies. 
    The calculations are based on the lifecycle of animal cohorts and their feed, manure handling practices, as well as fertiliser application rates.

    Attributes:
        data_manager_class (LCADataManager): A class instance that provides access to necessary emission factors and data specific to a given country or region.
        grazing_class (GrazingStage): A class instance to calculate emissions from grazing practices.
        housing_class (HousingStage): A class instance to calculate emissions from animal housing practices.
        storage_class (StorageStage): A class instance to calculate emissions from manure storage practices.
        spread_class (DailySpread): A class instance to calculate emissions from manure spreading practices.
        fertiliser_class (FertiliserInputs): A class instance to calculate emissions from fertiliser application.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)


    def create_emissions_dictionary(self, keys):
        """
        Creates a nested dictionary structure to store NH3 emission values from various sources categorized by specific keys (e.g., animal types).

        Parameters:
            keys (list): A list of string keys representing different emission categories or animal types.

        Returns:
            dict: A nested dictionary structured to hold emission values.
        """
        key_list = [
            "manure_management",
            "soils",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    

    # Manure Management
    def total_manure_NH3_AQ(self, animal):
        """
        Calculates total NH3 emissions from manure management practices for the specified animal collection.

        Parameters:
            animal (Animal): An instance representing a specific animal collection.

        Returns:
            float: Total NH3 emissions (kg) from manure management for the specified animal collection.
        """
        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):

                NH3N += (
                    self.storage_class.nh3_emissions_per_year_STORAGE(
                        animal.__getattribute__(key),
                    )
                    + self.housing_class.nh3_emissions_per_year_HOUSED(
                        animal.__getattribute__(key),
                    )
                ) * animal.__getattribute__(key).pop

        return NH3N

    # SOILS
    def total_fertiliser_soils_NH3_AQ(
        self, total_urea, total_urea_abated, total_n_fert
    ):
        """
        Calculates total NH3 emissions from fertiliser application to soils.

        Parameters:
            total_urea (float): Total urea fertiliser applied (kg).
            total_urea_abated (float): Total abated urea fertiliser applied (kg).
            total_n_fert (float): Total nitrogen fertiliser applied (kg).

        Returns:
            float: Total NH3 emissions (kg) from fertiliser application to soils.
        """
        NH3N = self.fertiliser_class.urea_NH3(
            total_urea, total_urea_abated
        ) + self.fertiliser_class.n_fertiliser_NH3(total_n_fert)

        return NH3N

    def total_grazing_soils_NH3_AQ(self, animal):
        """
        Calculates total NH3 emissions from soils during grazing for the specified animal collection.

        Parameters:
            animal (Animal): An instance representing a specific animal collection.

        Returns:
            float: Total NH3 emissions (kg) from soils during grazing for the specified animal collection.
        """
        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                NH3N += (
                    self.grazing_class.nh3_emissions_per_year_GRAZING(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )

        return NH3N
