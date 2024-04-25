
"""
Models
======
This module contains classes and functions for modeling crop data, 
including crop characteristics, emissions factors, upstream impacts, 
and fertilizer data. Key functionality includes:

* **DynamicData Classes:**  Flexible data structures to store crop, farm, and collections data.
* **CropChars:**  Management of crop characteristics (e.g., dry matter, nutrient content).
* **Emissions_Factors:** Storage and retrieval of emissions factors.
* **Upstream:**  Modeling of upstream environmental impacts.
* **Fertiliser:**  Handling fertilizer data and calculations.
* **Data Loading Functions:**  Loading data from various sources.
"""

class DynamicData(object):
    """
    Provides a flexible data structure for storing attributes loaded from external sources.

    Key Features:
        * **Dynamic Attributes:** Attributes are not predefined; they are created based on the data provided during initialization.
        * **Default Values:**  Assigns default values to attributes if not present in the input data.

    Usage:
        1. Instantiate with a data dictionary and an optional dictionary of defaults.
        2. Access attributes directly using dot notation (e.g., `my_data.attribute_name`).  
    """
    def __init__(self, data, defaults={}):

        # Set the defaults first
        for variable, value in defaults.items():
            setattr(self, variable, value)

        # Overwrite the defaults with the real values
        for variable, value in data.items():
            setattr(self, variable, value)


class CropCategory(DynamicData):
    """
    Represents a single crop category with its associated attributes.

    Attributes:
            kg_dm_per_ha (float):  Kilograms of dry matter per hectare for the crop.
            area (float): Area (in hectares) occupied by the crop.

   """
    def __init__(self, data):

        defaults = {"kg_dm_per_ha": 0.0, "area": 0.0}

        super(CropCategory, self).__init__(data, defaults)


class CropCollection(DynamicData):
    """
    Represents a collection of CropCategory objects.

    Inherits the flexibility of the DynamicData class to accommodate varying crop data.
    """
    def __init__(self, data):

        super(CropCollection, self).__init__(data)


class Farm(DynamicData):
    """
    Represents an agricultural farm with its associated attributes.

    Attributes:
        * **Dynamic Attributes:** The specific attributes will depend on the data loaded.
        * **crop_collections (optional):** A dictionary or other structure to store CropCollection objects related to the farm.
    """
    def __init__(self, data):#, crop_collections):

        #self.crops = crop_collections.get(data.get("farm_id"))

        super(Farm, self).__init__(data)


########################################################################################
# Crop Chars class
########################################################################################
class CropChars(object):
    """
    Stores and provides access to crop characteristics data.

    Attributes:
        data_frame (pandas.DataFrame): The DataFrame containing the loaded crop characteristics.
        crop_char (dict): A dictionary mapping crop types to their characteristics.

    """
    def __init__(self, data):

        self.data_frame = data

        self.crop_char = {}

        for _, row in self.data_frame.iterrows():

            crop_type = row.get("crop_type".lower())
            crop_dry_matter = row.get("crop_dry_matter")
            crop_below_ground_ratio_to_above_ground_biomass = row.get(
                "crop_below_ground_ratio_to_above_ground_biomass"
            )
            crop_above_ground_residue_dry_matter_to_harvested_yield = row.get(
                "crop_above_ground_residue_dry_matter_to_harvested_yield"
            )
            crop_n_content_below_ground = row.get("crop_n_content_below_ground")
            crop_n_content_of_above_ground_residues = row.get(
                "crop_n_content_of_above_ground_residues"
            )
            crop_slope = row.get("crop_slope")
            crop_intercept = row.get("crop_intercept")

            self.crop_char[crop_type] = {
                "crop_dry_matter": crop_dry_matter,
                "crop_below_ground_ratio_to_above_ground_biomass": crop_below_ground_ratio_to_above_ground_biomass,
                "crop_above_ground_residue_dry_matter_to_harvested_yield": crop_above_ground_residue_dry_matter_to_harvested_yield,
                "crop_n_content_below_ground": crop_n_content_below_ground,
                "crop_n_content_of_above_ground_residues": crop_n_content_of_above_ground_residues,
                "crop_slope": crop_slope,
                "crop_intercept": crop_intercept,
            }

    def get_crop_dry_matter(self, crop_char):
        """
        Returns the dry matter content of the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The dry matter content of the crop or None if not found.
        """
        return self.crop_char.get(crop_char).get("crop_dry_matter")

    def get_crop_below_ground_ratio_to_above_ground_biomass(self, crop_char):
        """
        Returns the ratio of below ground biomass to above ground biomass for the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The ratio of below ground biomass to above ground biomass or None if not found.
        """
        return self.crop_char.get(crop_char).get(
            "crop_below_ground_ratio_to_above_ground_biomass"
        )

    def get_crop_above_ground_residue_dry_matter_to_harvested_yield(self, crop_char):
        """
        Returns the ratio of above ground residue dry matter to harvested yield for the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The ratio of above ground residue dry matter to harvested yield or None if not found.
        """
        return self.crop_char.get(crop_char).get(
            "crop_above_ground_residue_dry_matter_to_harvested_yield"
        )

    def get_crop_n_content_below_ground(self, crop_char):
        """
        Returns the nitrogen content below ground for the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The nitrogen content below ground or None if not found.
        """
        return self.crop_char.get(crop_char).get("crop_n_content_below_ground")

    def get_crop_n_content_of_above_ground_residues(self, crop_char):
        """
        Returns the nitrogen content of above ground residues for the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The nitrogen content of above ground residues or None if not found.
        """
        return self.crop_char.get(crop_char).get(
            "crop_n_content_of_above_ground_residues"
        )

    def get_crop_slope(self, crop_char):
        """
        Returns the slope of the crop for the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The slope of the crop or None if not found.
        """
        return self.crop_char.get(crop_char).get("crop_slope")

    def get_crop_intercept(self, crop_char):
        """
        Returns the intercept of the crop for the specified crop.

        Parameters:
            crop_char (str): The crop type.

        Returns:
            float: The intercept of the crop or None if not found.
        """
        return self.crop_char.get(crop_char).get("crop_intercept")

    def is_loaded(self):
        """
        Returns whether the crop characteristics data has been loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False

######################################################################################
# Emissions Factors Data
######################################################################################
class Emissions_Factors(object):
    """
   Stores and provides access to emissions factors data.

   Attributes:
       data_frame (pandas.DataFrame): The DataFrame containing the loaded emissions factors.
       emissions_factors (dict): A dictionary mapping emissions factor names to their values.
   """
    def __init__(self, data):

        self.data_frame = data

        self.emissions_factors = {}

        for _, row in self.data_frame.iterrows():

            ef_emissions_factor_1_ipcc_2019 = row.get("ef_emissions_factor_1_ipcc_2019")
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
            ef_indirect_n2o_atmospheric_deposition_to_soils_and_water = row.get(
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
            )
            ef_indirect_n2o_from_leaching_and_runoff = row.get(
                "ef_indirect_n2o_from_leaching_and_runoff"
            )
            ef_grassland_dm_t = row.get("ef_grassland_dm_t")
            ef_dm_carbon_stock_crops = row.get("ef_dm_carbon_stock_crops")
            ef_Frac_P_Leach = row.get("ef_Frac_P_Leach")

            self.emissions_factors= {
                "ef_emissions_factor_1_ipcc_2019": ef_emissions_factor_1_ipcc_2019,
                "ef_urea": ef_urea,
                "ef_urea_and_nbpt": ef_urea_and_nbpt,
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox": ef_fracGASF_urea_fertilisers_to_nh3_and_nox,
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox": ef_fracGASF_urea_and_nbpt_to_nh3_and_nox,
                "ef_frac_leach_runoff": ef_frac_leach_runoff,
                "ef_ammonium_nitrate": ef_ammonium_nitrate,
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox": ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox,
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water": ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "ef_indirect_n2o_from_leaching_and_runoff": ef_indirect_n2o_from_leaching_and_runoff,
                "ef_grassland_dm_t": ef_grassland_dm_t,
                "ef_dm_carbon_stock_crops": ef_dm_carbon_stock_crops,
                "ef_Frac_P_Leach": ef_Frac_P_Leach,
            }

    def get_ef_emissions_factor_1_ipcc_2019(self):
        """
       Returns the value of the 'ef_emissions_factor_1_ipcc_2019' emissions factor.

       Returns:
           float: The value of the emissions factor or None if not found.
       """
        return self.emissions_factors.get(
            "ef_emissions_factor_1_ipcc_2019"
        )

    def get_ef_urea(self):
        """
         Returns the value of the 'ef_urea' emissions factor.

        Returns:    
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get("ef_urea")

    def get_ef_urea_and_nbpt(self):
        """
        Returns the value of the 'ef_urea_and_nbpt' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get("ef_urea_and_nbpt")

    def get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(self):
        """
        Returns the value of the 'ef_fracGASF_urea_fertilisers_to_nh3_and_nox' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.

        """
        return self.emissions_factors.get(
            "ef_fracGASF_urea_fertilisers_to_nh3_and_nox"
        )

    def get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(self):
        """
        Returns the value of the 'ef_fracGASF_urea_and_nbpt_to_nh3_and_nox' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get(
            "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"
        )

    def get_ef_frac_leach_runoff(self):
        """
        Returns the value of the 'ef_frac_leach_runoff' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get("ef_frac_leach_runoff")

    def get_ef_ammonium_nitrate(self):
        """
        Returns the value of the 'ef_ammonium_nitrate' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.

        """
        return self.emissions_factors.get("ef_ammonium_nitrate")

    def get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(self):
        """
        Returns the value of the 'ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get(
            "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
        )

    def get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
        self
    ):
        """
        Returns the value of the 'ef_indirect_n2o_atmospheric_deposition_to_soils_and_water' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get(
            "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
        )

    def get_ef_indirect_n2o_from_leaching_and_runoff(self):
        """
        Returns the value of the 'ef_indirect_n2o_from_leaching_and_runoff' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get(
            "ef_indirect_n2o_from_leaching_and_runoff"
        )

    def get_ef_grassland_dm_t(self):
        """
        Returns the value of the 'ef_grassland_dm_t' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get("ef_grassland_dm_t")

    def get_ef_dm_carbon_stock_crops(self):
        """
        Returns the value of the 'ef_dm_carbon_stock_crops' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get(
            "ef_dm_carbon_stock_crops"
        )

    def get_ef_Frac_P_Leach(self):
        """
        Returns the value of the 'ef_Frac_P_Leach' emissions factor.

        Returns:
            float: The value of the emissions factor or None if not found.
        """
        return self.emissions_factors.get("ef_Frac_P_Leach")


    def is_loaded(self):
        """
        Returns whether the emissions factors data has been loaded.

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
    Stores and provides access to upstream data.

    Attributes:
        data_frame (pandas.DataFrame): The DataFrame containing the loaded upstream data.
        upstream (dict): A dictionary mapping upstream types to their values.
    """
    def __init__(self, data):

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

    def get_upstream_fu(self, upstream_type):
        """
        Returns the functional unit of the specified upstream type.

        Parameters:
            upstream_type (str): The upstream type.

        Returns:
            float: The functional unit of the upstream type or None if not found.
        """
        return self.upstream.get(upstream_type).get("upstream_fu")

    def get_upstream_kg_co2e(self, upstream_type):
        """
        Returns the kg CO2e of the specified upstream type.

        Parameters:
            upstream_type (str): The upstream type.

        Returns:
            float: The kg CO2e of the upstream type or None if not found.
        """
        return self.upstream.get(upstream_type).get("upstream_kg_co2e")

    def get_upstream_kg_po4e(self, upstream_type):
        """
        Returns the kg PO4e of the specified upstream type.

        Parameters:
            upstream_type (str): The upstream type.

        Returns:
            float: The kg PO4e of the upstream type or None if not found.
        """
        return self.upstream.get(upstream_type).get("upstream_kg_po4e")

    def get_upstream_kg_so2e(self, upstream_type):
        """
        Returns the kg SO2e of the specified upstream type.

        Parameters:
            upstream_type (str): The upstream type.

        Returns:
            float: The kg SO2e of the upstream type or None if not found.
        """
        return self.upstream.get(upstream_type).get("upstream_kg_so2e")

    def get_upstream_mje(self, upstream_type):
        """
        Returns the MJE of the specified upstream type.

        Parameters:
            upstream_type (str): The upstream type.

        Returns:
            float: The MJE of the upstream type or None if not found.
        """
        return self.upstream.get(upstream_type).get("upstream_mje")

    def get_upstream_kg_sbe(self, upstream_type):
        """
        Returns the kg SBE of the specified upstream type.

        Parameters:
            upstream_type (str): The upstream type.

        Returns:
            float: The kg SBE of the upstream type or None if not found.
        """
        return self.upstream.get(upstream_type).get("upstream_kg_sbe")

    def is_loaded(self):
        """
        Returns whether the upstream data has been loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False
        
#############################################################################################
# Fertiliser class
########################################################################################
class Fertiliser(object):
    """
    Stores and provides access to fertiliser data.

    Attributes:
        data_frame (pandas.DataFrame): The DataFrame containing the loaded fertiliser data.
        fertiliser (dict): A dictionary mapping crop types to their fertiliser values.
    """
    def __init__(self, data):

        self.data_frame = data

        self.fertiliser = {}

        for _, row in self.data_frame.iterrows():

            fert_crop_type = row.get("fert_crop_type".lower())
            fert_kg_n_per_ha = row.get("fert_kg_n_per_ha")
            fert_kg_p_per_ha = row.get("fert_kg_p_per_ha")
            fert_kg_k_per_ha = row.get("fert_kg_k_per_ha")

            self.fertiliser[fert_crop_type] = {
                "fert_kg_n_per_ha": fert_kg_n_per_ha,
                "fert_kg_p_per_ha": fert_kg_p_per_ha,
                "fert_kg_k_per_ha": fert_kg_k_per_ha,
            }

    def get_fert_kg_n_per_ha(self, fert_crop_type):
        """
        Returns the kg N per hectare for a specified crop type.

        Parameters:
            fert_crop_type (str): The crop type.

        Returns:
            float: The kg N per hectare for the specified crop or None if not found.
        """
        crop = self.fertiliser.get(fert_crop_type)
        if crop is None:
            return self.fertiliser.get("average").get("fert_kg_n_per_ha")
        return crop.get("fert_kg_n_per_ha")
    

    def get_fert_kg_p_per_ha(self, fert_crop_type):
        """
        Returns the kg P per hectare for a specified crop type.

        Parameters:
            fert_crop_type (str): The crop type.

        Returns:
            float: The kg P per hectare for the specified crop or None if not found.
        """
        crop = self.fertiliser.get(fert_crop_type)
        if crop is None:
            return self.fertiliser.get("average").get("fert_kg_p_per_ha")
        return crop.get("fert_kg_p_per_ha")
    

    def get_fert_kg_k_per_ha(self, fert_crop_type):
        """
        Returns the kg K per hectare for a specified crop type.

        Parameters:
            fert_crop_type (str): The crop type.

        Returns:
            float: The kg K per hectare for the specified crop or None if not found.
        """
        crop = self.fertiliser.get(fert_crop_type)
        if crop is None:
            return self.fertiliser.get("average").get("fert_kg_k_per_ha")
        return crop.get("fert_kg_k_per_ha")
    

    def is_loaded(self):
        """
        Returns whether the fertiliser data has been loaded.

        Returns:
            bool: True if the data has been loaded, False otherwise.
        """
        if self.data_frame is not None:
            return True
        else:
            return False
        
################################################################################################
# Data Loading
################################################################################################


def load_crop_farm_data(crop_type_dataframe):
    """
    Load crop type data into a collection of CropCategory and CropCollection objects.

    Parameters
    ----------
    crop_type_dataframe : pandas.DataFrame
        The DataFrame containing the crop type data.

    Returns
    -------
    dict
        A dictionary containing the loaded crop type data.
    """
    # 1. Load each animal category into an object

    categories = []

    for _, row in crop_type_dataframe.iterrows():

        data = dict([(x, row.get(x)) for x in row.keys()])
        categories.append(CropCategory(data))

    # 2. Aggregate the animal categories into collection based on the farm ID

    collections = {}

    for category in categories:

        farm_id = category.farm_id

        crop_type = category.crop_type

        if farm_id not in collections:
            collections[farm_id] = {crop_type: category}
        else:
            collections[farm_id][crop_type] = category

    # 3. Convert the raw collection data into animal collection objects

    collection_objects = {}

    for farm_id, raw_data in collections.items():
        collection_objects[farm_id] = {"crop_group":CropCollection(raw_data)}

    return collection_objects


def load_farm_data(farm_data_frame):
    """
    Load farm data into a collection of Farm objects.
    
    Parameters
    ----------
    farm_data_frame : pandas.DataFrame
        The DataFrame containing the farm data.

    Returns
    -------
    dict
        A dictionary containing the loaded farm data.
    """
    subset = [
        "diesel_kg",
        "elec_kwh",
    ]
    farm_data_frame.drop_duplicates(subset=subset, keep="first", inplace=True)

    scenario_list = []
    keys = []
    for _, row in farm_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        scenario_list.append(Farm(data))
        #keys.append(row.get("farm_id"))

    #collections ={}

    #for _, sc in scenario_list:
        #collections[sc] = scenario_list[sc]

    #return dict(enumerate(scenario_list))
    return dict([(x.farm_id, x) for x in scenario_list])
####################################################################################################
# Load Additional Databases
####################################################################################################


def load_crop_chars_data():
    """
    Load crop characteristics data.

    Returns
    -------
    CropChars
        An instance of the CropChars class containing the loaded crop characteristics data.
    """
    return CropChars()


def load_emissions_factors_data(ef_country):
    """
    Load emissions factors data.

    Parameters
    ----------
    ef_country : str
        The name of the country for which the data is being loaded.

    Returns
    -------
    Emissions_Factors
        An instance of the Emissions_Factors class containing the loaded emissions factors data.
    """
    return Emissions_Factors(ef_country)


def load_upstream_data():
    """
    Load upstream data.

    Returns
    -------
    Upstream
        An instance of the Upstream class containing the loaded upstream data.
    """
    return Upstream()


def load_fertiliser_data():
    """
    Load fertiliser data.

    Returns
    -------
    Fertiliser
        An instance of the Fertiliser class containing the loaded fertiliser data.
    """
    return Fertiliser()



def print_crop_data(data):
    """
    Print the crop data.

    Parameters
    ----------
    data : dict
        The crop data to print.

    """
    for _, key in enumerate(data):
        for crops in data[key].keys():
            for crop in data[key].__getitem__(crops).__dict__.keys():
                for attribute in data[key].__getitem__(crops).__getattribute__(crop).__dict__.keys():
                    print(
                        f"{crop}: {attribute} = {data[key].__getitem__(crops).__getattribute__(crop).__getattribute__(attribute)}"
                    )

