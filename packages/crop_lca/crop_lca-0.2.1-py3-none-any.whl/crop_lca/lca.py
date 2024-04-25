"""
Crop LCA
========
This module contains the classes and methods used to calculate the carbon footprint of crop production.
"""
import numpy as np
import pandas as pd

from crop_lca.resource_manager.data_loader import Loader
import copy

# CO2 from Crop Biomass

class Conversion:
    """
    Class for calculating CO2 emissions from transition from grassland to crop.

    Methods
    -------
    co2_form_grassland_to_crop(data)
        Calculate carbon emissions from transition from grassland to crop.
    """
    def __init__(self, ef_country) -> None:
        self.loader_class = Loader(ef_country)

    def co2_form_grassland_to_crop(self, data):
        """
        Calculate carbon emissions from transition from grassland to crop.

        Parameters:
        - data (object): Object containing necessary data for calculation.

        Returns:
        - float: Carbon emissions from transition.
        """
        grass = self.loader_class.emissions_factors.get_ef_grassland_dm_t()

        carbon_fraction = 0.5

        crop_dm = self.loader_class.emissions_factors.get_ef_dm_carbon_stock_crops()

        return data.temp_grass.area * ((0 - grass * carbon_fraction) + crop_dm)


######################################################################################################################

# Direct N2O Emissions from crop Residues
class Residues:
    """
    Class for calculating direct N2O emissions from crop residues.

    Methods
    -------
    n_from_crop_residue_direct(data)
        Calculate direct N2O emissions from crop residues.
    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)

    def n_from_crop_residue_direct(self, data):
        """
        Calculate direct N2O emissions from crop residues.

        Parameters:
        - data (object): Object containing necessary data for calculation.

        Returns:
        - float: Direct N2O emissions from crop residues.

        Notes:
        - This method is based on the IPCC 2019 guidelines for national greenhouse gas inventories.
        - The method is based on the following equation:

            EQUATION 11.6 (UPDATED) N FROM CROP RESIDUES AND FORAGE/PASTURE RENEWAL (TIER 1) (2019 IPCC)
        - Where:
            Fcr = annual amount of N in crop residues (above and below ground), including N-fixing crops,
            and from forage/pasture renewal, returned to soils annually, kg N yr-1

            AGR = annual total amount of above-ground crop residue for crop T, kg d.m. yr-1.

            NAG = N content of above-ground residues for crop T, kg N (kg d.m.) -1

            FracRemove= fraction of above-ground residues of crop T removed annually for purposes such as feed, bedding and construction, dimensionless. Survey of experts in country is required to obtain
            data. If data for FracRemove are not available, assume no removal

            BGR = annual total amount of belowground crop residue for crop T, kg d.m. yr-1

            Crop_t = harvested annual dry matter yield for crop T, kg d.m. ha-1

            AG_dm = Above-ground residue dry matter for crop T, kg d.m. ha-1

            Rag = ratio of above-ground residue dry matter to harvested yield for crop T (Crop(T)), kg d.m. ha-
            1 (kg d.m. ha-1)-1, (Table 11.1a)

            RS = ratio of below-ground root biomass to above-ground shoot biomass for crop T, kg d.m.ha-1
            (kg d.m. ha-1)-1, (Table 11.1a)

            FracRenew = fraction of total area under crop T that is renewed annually 15, dimensionless. For countries
            where pastures are renewed on average every X years, FracRenew = 1/X. For annual crops
            FracRenew = 1
        """

        dry_matter_fraction = {
            "grains": self.loader_class.crop_chars.get_crop_dry_matter("grains"),
            "crops": self.loader_class.crop_chars.get_crop_dry_matter("crops"),
            "maize": self.loader_class.crop_chars.get_crop_dry_matter("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_dry_matter("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_dry_matter("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_dry_matter("oats"),
            "barley": self.loader_class.crop_chars.get_crop_dry_matter("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_dry_matter("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_dry_matter("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_dry_matter("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_dry_matter("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_dry_matter("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_dry_matter("n_fixing_forage"),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_dry_matter("perennial_grasses"),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_dry_matter("grass_clover_mix"),
        }

        Rag = {
            "grains": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "grains"
            ),
            "crops": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "crops"
            ),
            "maize": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "maize"
            ),
            "winter_wheat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "winter_wheat"
            ),
            "spring_wheat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "spring_wheat"
            ),
            "oats": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "oats"
            ),
            "barley": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "barley"
            ),
            "beans_peas": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "beans_pulses"
            ),
            "potatoes": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "turnips": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "sugar_beat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "fodder_beat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "rye": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "rye"
            ),
            "sorghum": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "sorghum"
            ),
            "alfalfa": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "alfalfa"
            ),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "non_legume_hay"
            ),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "grass_clover_mix"
            ),
        }

        RS = {
            "grains": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "grains"
            ),
            "crops": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "crops"
            ),
            "maize": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "maize"
            ),
            "winter_wheat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "winter_wheat"
            ),
            "spring_wheat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "spring_wheat"
            ),
            "oats": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("oats"),
            "barley": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "barley"
            ),
            "beans_peas": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "beans_pulses"
            ),
            "potatoes": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "turnips": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "sugar_beat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "fodder_beat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "rye": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "sorghum"
            ),
            "alfalfa": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "alfalfa"
            ),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "non_legume_hay"
            ),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "grass_clover_mix"
            ),
        }

        crops_n_above = {
            "grains": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("grains"),
            "crops": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("crops"),
            "maize": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "winter_wheat"
            ),
            "spring_wheat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "spring_wheat"
            ),
            "oats": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("oats"),
            "barley": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "beans_pulses"
            ),
            "potatoes": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "turnips": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "sugar_beat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "fodder_beat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "rye": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "non_legume_hay"
            ),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "grass_clover_mix"
            ),
        }

        crops_n_below = {
            "grains": self.loader_class.crop_chars.get_crop_n_content_below_ground("grains"),
            "crops": self.loader_class.crop_chars.get_crop_n_content_below_ground("crops"),
            "maize": self.loader_class.crop_chars.get_crop_n_content_below_ground("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_n_content_below_ground("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_n_content_below_ground("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_n_content_below_ground("oats"),
            "barley": self.loader_class.crop_chars.get_crop_n_content_below_ground("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_n_content_below_ground("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_n_content_below_ground("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_n_content_below_ground("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_n_content_below_ground("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_n_content_below_ground("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_n_content_below_ground(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_n_content_below_ground(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_n_content_below_ground(
                "grass_clover_mix"
            ),
        }

        slope = {
            "grains": self.loader_class.crop_chars.get_crop_slope("grains"),
            "crops": self.loader_class.crop_chars.get_crop_slope("crops"),
            "maize": self.loader_class.crop_chars.get_crop_slope("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_slope("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_slope("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_slope("oats"),
            "barley": self.loader_class.crop_chars.get_crop_slope("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_slope("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_slope("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_slope("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_slope("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_slope("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_slope("n_fixing_forage"),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_slope("perennial_grasses"),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_slope("grass_clover_mix"),
        }

        intercept = {
            "grains": self.loader_class.crop_chars.get_crop_intercept("grains"),
            "crops": self.loader_class.crop_chars.get_crop_intercept("crops"),
            "maize": self.loader_class.crop_chars.get_crop_intercept("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_intercept("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_intercept("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_intercept("oats"),
            "barley": self.loader_class.crop_chars.get_crop_intercept("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_intercept("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_intercept("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_intercept("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_intercept("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_intercept("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_intercept("n_fixing_forage"),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_intercept("perennial_grasses"),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_intercept("grass_clover_mix"),
        }


        Crop_t = dry_matter_fraction.get(data.crop_type)
        if Crop_t is None:
            Crop_t = dry_matter_fraction.get("crops")

        Crop_t_output = self.loader_class.crop_chars.get_crop_dry_matter("crops")

        AG_dm = Rag.get(data.crop_type)
        if AG_dm is None:
            AG_dm = Rag.get("crops")

        AG_dm_output = Crop_t_output * AG_dm

        ratio_below_ground = RS.get(data.crop_type)
        if ratio_below_ground is None:
            ratio_below_ground = RS.get("crops")

        ratio_below_ground_output = ratio_below_ground

        NAG = crops_n_above.get(data.crop_type)

        if NAG is None:
            NAG = crops_n_above.get("crops")

        NAG_output = 0

        NAG_output = NAG

        NBG = crops_n_below.get(data.crop_type)

        if NBG is None:
            NBG = crops_n_below.get("crops")

        NBG_output = NBG

        FracRemove = 0.95

        FracRenew = 1

        AGR = Crop_t_output

        BGR = (
            (Crop_t_output + AG_dm_output)
            * ratio_below_ground_output
            * data.area
            * FracRenew
        ) * NBG_output

        AGR_total = AGR * NAG_output * (1 - FracRemove)

        Fcr = AGR_total + BGR

        return Fcr





###############################################################################
# Farm & Upstream Emissions
###############################################################################
# Fertiliser Use Calculations

class FertilserUse:
    """
    Class for calculating fertiliser use.

    Methods
    ------- 
    total_an_fert_use(data, urea_proportion)
        Total AN fert use in kg.

    total_urea_fert_use(data, urea_proportion)
        Total urea fert use in kg.

    total_p_fert_use(data)
        Total P fert use in kg.

    total_k_fert_use(data)
        Total K fert use in kg.

    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)


    def total_an_fert_use(self, data, urea_proportion):
        """
        Returns the total AN fert use in kg.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea.

        Returns:
        - float: Total AN fert use in kg.
        """
        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_an = 0

        for crop in crop_names:
            try:
                total_fert_an += self.loader_class.fertiliser.get_fert_kg_n_per_ha(crop) * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * (1 - urea_proportion)
                )

            except AttributeError:

                total_fert_an += self.loader_class.fertiliser.get_fert_kg_n_per_ha("average") * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * (1 - urea_proportion)
                )

        return total_fert_an


    def total_urea_fert_use(self, data, urea_proportion):
        """
        Returns the total urea fert use in kg.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea.

        Returns:
        - float: Total urea fert use in kg.
        """
        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_urea = 0

        for crop in crop_names:
            try:
                total_fert_urea += self.loader_class.fertiliser.get_fert_kg_n_per_ha(crop) * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * urea_proportion
                )

            except AttributeError:
                total_fert_urea += self.loader_class.fertiliser.get_fert_kg_n_per_ha("average") * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * urea_proportion
                )

        return total_fert_urea


    def total_p_fert_use(self, data):
        """
        Returns the total P fert use in kg.

        Parameters:
        - data (object): Object containing necessary data for calculation.

        Returns:
        - float: Total P fert use in kg.
        """
        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_p = 0

        for crop in crop_names:
            try:
                total_fert_p += (
                    self.loader_class.fertiliser.get_fert_kg_p_per_ha(crop) * data.__getitem__("crop_group").__getattribute__(crop).area
                )

            except AttributeError:
                total_fert_p += (
                    self.loader_class.fertiliser.get_fert_kg_p_per_ha("average")
                    * data.__getitem__("crop_group").__getattribute__(crop).area
                )

        return total_fert_p


    def total_k_fert_use(self, data):
        """
        Returns the total K fert use in kg.

        Parameters:
        - data (object): Object containing necessary data for calculation.

        Returns:
        - float: Total K fert use in kg.
        """
        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_k = 0

        for crop in crop_names:
            try:
                total_fert_k += (
                    self.loader_class.fertiliser.get_fert_kg_k_per_ha(crop) * data.__getitem__("crop_group").__getattribute__(crop).area
                )

            except AttributeError:
                total_fert_k += (
                    self.loader_class.fertiliser.get_fert_kg_k_per_ha("average")
                    * data.__getitem__("crop_group").__getattribute__(crop).area
                )

        return total_fert_k

########################################################################################################
# Urea Fertiliser Emissions
########################################################################################################
class FertiliserInputs:
    """
    Class for calculating emissions from fertilizer inputs.

    Methods
    -------
    urea_N2O_direct(data, urea_proportion, urea_abated_proportion)
        Calculate total direct emissions from urea and abated urea applied to soils.

    urea_NH3(data, urea_proportion, urea_abated_proportion)
        Calculate the amount of urea and abated urea volatized as NH3.

    urea_nleach(data, urea_proportion, urea_abated_proportion)
        Calculate the amount of N from urea and abated urea leached from soils.

    urea_N2O_indirect(data, urea_proportion, urea_abated_proportion)
        Calculate indirect emissions from urea.

    urea_p_leach(data, urea_proportion, urea_abated_proportion)
        Calculate the amount of P from urea and abated urea leached from soils.

    n_fertiliser_P_leach(data, urea_proportion)
        Calculate the amount of P from N fertiliser leached from soils.

    p_fertiliser_P_leach(data)
        Calculate the amount of P from P fertiliser leached from soils.

    n_fertiliser_direct(data, urea_proportion)
        Calculate direct emissions from N fertiliser.

    n_fertiliser_NH3(data, urea_proportion)
        Calculate the amount of N fertiliser volatized as NH3.

    n_fertiliser_nleach(data, urea_proportion)
        Calculate the amount of N from AN fertiliser leached from soils.

    n_fertiliser_N2O_indirect(data, urea_proportion)
        Calculate indirect emissions from N fertiliser.
    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.fertiliser_use_class = FertilserUse(ef_country)


    def urea_N2O_direct(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        """
        Calculate total direct emissions from urea and abated urea applied to soils.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.
        - urea_abated_proportion (float): Proportion of urea abated.

        Returns:
        - float: Total direct emissions from urea and abated urea.
        """

        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        ef_urea = self.loader_class.emissions_factors.get_ef_urea()
        ef_urea_abated = self.loader_class.emissions_factors.get_ef_urea_and_nbpt()

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


    def urea_NH3(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        """
        Calculate the amount of urea and abated urea volatized as NH3.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.
        - urea_abated_proportion (float): Proportion of urea abated.

        Returns:
        - float: Total amount of urea and abated urea volatized as NH3.
        """
        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        ef_urea = self.loader_class.emissions_factors.get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(
            
        )
        ef_urea_abated = self.loader_class.emissions_factors.get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(
            
        )

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


    def urea_nleach(
        self,
        data,
        urea_proportion,
        urea_abated_proportion
    ):

        """
        Calculate the amount of N from urea and abated urea leached from soils.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.
        - urea_abated_proportion (float): Proportion of urea abated.

        Returns:
        - float: Total amount of urea and abated urea leached from soils.
        """
        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        leach = self.loader_class.emissions_factors.get_ef_frac_leach_runoff()

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea + total_urea_abated) * leach


    def urea_N2O_indirect(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculate indirect emissions from urea.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.
        - urea_abated_proportion (float): Proportion of urea abated.

        Returns:
        - float: Total indirect emissions from urea.
        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
                
            )
        )
        indirect_leaching = self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(
            
        )
        """
        this functino returns the upstream CO2 emissions from electricity consumption
        """

        return (
            self.urea_NH3(
                data,
                urea_proportion,
                urea_abated_proportion,
            )
            * indirect_atmosphere
        ) + (
            self.urea_nleach(
                data,
                urea_proportion,
                urea_abated_proportion,
            )
            * indirect_leaching
        )


    def urea_P_leach(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
         Calculate the amount of P from urea and abated urea leached from soils.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.
        - urea_abated_proportion (float): Proportion of urea abated.

        Returns:
        - float: Total indirect emissions from urea.
        """

        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea + total_urea_abated) * frac_leach


    #########################################################################################################
    # Nitrogen Fertiliser Emissions
    #########################################################################################################
    def n_fertiliser_P_leach(
        self, data, urea_proportion
    ):
        """
         Calculate the amount of P from AN fertiliser leached from soils.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Total indirect emissions from urea.
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * frac_leach


    def p_fertiliser_P_leach(self, data):
        """
         Calculate the amount of P from P fertiliser leached from soils.

        Parameters:
        - data (object): Object containing necessary data for calculation.

        Returns:
        - float: Total indirect emissions from urea
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        total_p_fert = self.fertiliser_use_class.total_p_fert_use(data)

        return total_p_fert * frac_leach


    def n_fertiliser_direct(
        self, data, urea_proportion
    ):
        """
        This function returns total direct emissions from ammonium nitrate application at field level

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Total direct emissions from ammonium nitrate application at field level
        """
        ef = self.loader_class.emissions_factors.get_ef_ammonium_nitrate()

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * ef


    def n_fertiliser_NH3(self, data, urea_proportion):
        """
        This function returns total NH3 emissions from ammonium nitrate application at field level

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Total NH3 emissions from ammonium nitrate application at field level
        """
        ef = self.loader_class.emissions_factors.get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(
            
        )

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * ef


    def n_fertiliser_nleach(
        self, data, urea_proportion
    ):  
        """
        This function returns the amount of N from AN fertiliser leached from soils.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Total amount of N from AN fertiliser leached from soils
        """

        leach = self.loader_class.emissions_factors.get_ef_frac_leach_runoff()

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * leach


    def n_fertiliser_indirect(
        self, data, urea_proportion
    ):
        """
        This function returns the indirect emissions from AN fertiliser.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Total indirect emissions from AN fertiliser
        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
                
            )
        )
        indirect_leaching = self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(
            
        )

        return (
            self.n_fertiliser_NH3(
                 data, urea_proportion
            )
            * indirect_atmosphere
        ) + (
            self.n_fertiliser_nleach(
                data, urea_proportion
            )
            * indirect_leaching
        )



class Upstream:
    """
    Class for calculating upstream emissions.

    Methods
    -------
    fert_upstream_po4(data, urea_proportion)
        Calculate the upstream emissions from urea and ammonium fertiliser manufacture.
    
    fert_upstream_co2(data, urea_proportion)
        Calculate the upstream CO2 emissions from urea and ammonium fertiliser manufacture.

    diesel_CO2(diesel_kg)
        Calculate the direct and indirect upstream CO2 emissions from diesel.

    diesel_PO4(diesel_kg)
        Calculate the direct and indirect upstream PO4 emissions from diesel.

    elec_CO2(elec_kwh)
        Calculate the upstream CO2 emissions from electricity consumption.

    elec_PO4(elec_kwh)
        Calculate the upstream PO4 emissions from electricity consumption.

    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.fertiliser_use_class = FertilserUse(ef_country)


    def fert_upstream_po4(self, data, urea_proportion):
        """
        this function returns the upstream emissions from urea and ammonium fertiliser manufacture.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Upstream emissions from urea and ammonium fertiliser manufacture.
        """
        AN_fert_PO4 = self.loader_class.upstream.get_upstream_kg_po4e(
            "ammonium_nitrate_fertiliser"
        )  
        Urea_fert_PO4 = self.loader_class.upstream.get_upstream_kg_po4e("urea_fert")
        Triple_superphosphate = self.loader_class.upstream.get_upstream_kg_po4e("triple_superphosphate")
        Potassium_chloride = self.loader_class.upstream.get_upstream_kg_po4e("potassium_chloride")

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)
        total_p_fert = self.fertiliser_use_class.total_p_fert_use(data)
        total_k_fert = self.fertiliser_use_class.total_k_fert_use(data)
        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion)

        return (
            (total_n_fert * AN_fert_PO4)
            + (total_urea * Urea_fert_PO4)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
        )

    def fert_upstream_co2(self, data, urea_proportion):
        """
        this function returns the upstream CO2 emissions from urea and ammonium fertiliser manufacture.

        Parameters:
        - data (object): Object containing necessary data for calculation.
        - urea_proportion (float): Proportion of urea used as fertilizer.

        Returns:
        - float: Upstream CO2 emissions from urea and ammonium fertiliser manufacture.
        """
        AN_fert_CO2 = self.loader_class.upstream.get_upstream_kg_co2e(
            "ammonium_nitrate_fertiliser"
        )  
        Urea_fert_CO2 = self.loader_class.upstream.get_upstream_kg_co2e("urea_fert")
        Triple_superphosphate = self.loader_class.upstream.get_upstream_kg_co2e("triple_superphosphate")
        Potassium_chloride = self.loader_class.upstream.get_upstream_kg_co2e("potassium_chloride")

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)
        total_p_fert = self.fertiliser_use_class.total_p_fert_use(data)
        total_k_fert = self.fertiliser_use_class.total_k_fert_use(data)
        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion)


        return (
            (total_n_fert * AN_fert_CO2)
            + (total_urea * Urea_fert_CO2)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
        )
    
    def diesel_CO2(self, diesel_kg):
        """
        this function returns the direct and indirect upstream CO2 emmisions from diesel 

        Parameters:
        - diesel_kg (float): Amount of diesel used.

        Returns:
        - float: Direct and indirect upstream CO2 emmisions from diesel.
        """
        Diesel_indir = self.loader_class.upstream.get_upstream_kg_co2e("diesel_indirect")
        Diest_dir = self.loader_class.upstream.get_upstream_kg_co2e("diesel_direct")

        return diesel_kg * (Diest_dir + Diesel_indir)
    

    def diesel_PO4(self, diesel_kg):
        """
        this function returns the direct and indirect upstream PO4 emmisions from diesel

        Parameters:
        - diesel_kg (float): Amount of diesel used.

        Returns:
        - float: Direct and indirect upstream PO4 emmisions from diesel.
        """
        Diesel_indir = self.loader_class.upstream.get_upstream_kg_po4e(
            "diesel_indirect"
        )
        Diest_dir = self.loader_class.upstream.get_upstream_kg_po4e("diesel_direct")

        return diesel_kg * (Diest_dir + Diesel_indir)
    

    def elec_CO2(self, elec_kwh):
        """
        this function returns the upstream CO2 emissions from electricity consumption

        Parameters:
        - elec_kwh (float): Amount of electricity consumed.

        Returns:
        - float: Upstream CO2 emissions from electricity consumption.
        """
        elec_consumption = self.loader_class.upstream.get_upstream_kg_co2e(
            "electricity_consumed"
        )  # based on Norway hydropower
        return elec_kwh * elec_consumption


    def elec_PO4(self, elec_kwh):
        """
        this function returns the upstream PO4 emissions from electricity consumption
        
        Parameters:
        - elec_kwh (float): Amount of electricity consumed.

        Returns:
        - float: Upstream PO4 emissions from electricity consumption.
        """
        elec_consumption = self.loader_class.upstream.get_upstream_kg_po4e(
            "electricity_consumed"
        )  # based on Norway hydropower
        return elec_kwh * elec_consumption
    

################################################################################
# Total Global Warming Potential of whole farms
################################################################################
class ClimateChangeTotals:
    """
    A class to calculate various climate change totals based on factors like emissions, residues, fertilizers, etc.

    Attributes:
        loader_class (Loader): An instance of the Loader class to load data.
        residues_class (Residues): An instance of the Residues class to handle residue data.
        fertiliser_emissions_class (FertiliserInputs): An instance of the FertiliserInputs class to manage fertilizer emissions.
        fertiliser_use_class (FertilserUse): An instance of the FertilserUse class to handle fertilizer use data.
        upstream_class (Upstream): An instance of the Upstream class to deal with upstream data.

    Methods:
        create_emissions_dictionary(keys): Creates a dictionary to store emissions data.
        create_extended_emissions_dictionary(keys): Creates an extended dictionary to store emissions data including upstream.
        total_residue_per_crop_direct(data): Calculates total nitrogen from all crops based on direct residue data.
        total_fertiliser_direct(data, urea_proportion, urea_abated_proportion): Calculates total direct emissions from urea and ammonium fertilizers.
        total_fertiliser_indirect(data, urea_proportion, urea_abated_proportion): Calculates total indirect emissions from urea and ammonium fertilizers.
        urea_co2(data, urea_proportion, urea_abated_proportion): Calculates total CO2 emissions from urea application.
        upstream_and_inputs_and_fuel_co2(data, urea_proportion, diesel_kg, elec_kwh): Calculates total CO2 emissions from upstream activities, inputs, and fuel usage.
    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.residues_class = Residues(ef_country)
        self.fertiliser_emissions_class = FertiliserInputs(ef_country)
        self.fertiliser_use_class = FertilserUse(ef_country)
        self.upstream_class = Upstream(ef_country)


    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary to store emissions data.

        Args:
            keys (list): List of keys to be used in the emissions dictionary.

        Returns:
            dict: A dictionary with emissions data initialized to zero.
        """
        crop_key_list = [
            "crop_residue_direct",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soils_N2O",
        ]

        crop_keys_dict = dict.fromkeys(keys)

        crop_emissions_dict = dict.fromkeys(crop_key_list)

        for key in crop_emissions_dict.keys():
            crop_emissions_dict[key] = copy.deepcopy(crop_keys_dict)
            for inner_k in crop_keys_dict.keys():
                crop_emissions_dict[key][inner_k] = 0

        return crop_emissions_dict


    def create_extended_emissions_dictionary(self, keys):
        """
        Creates an extended dictionary to store emissions data including upstream.

        Args:
            keys (list): List of keys to be used in the emissions dictionary.

        Returns:
            dict: An extended dictionary with emissions data initialized to zero, including upstream data.
        """
        crop_key_list = [
            "crop_residue_direct",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soils_N2O",
            "upstream"
        ]

        crop_keys_dict = dict.fromkeys(keys)

        crop_emissions_dict = dict.fromkeys(crop_key_list)

        for key in crop_emissions_dict.keys():
            crop_emissions_dict[key] = copy.deepcopy(crop_keys_dict)
            for inner_k in crop_keys_dict.keys():
                crop_emissions_dict[key][inner_k] = 0

        return crop_emissions_dict
    
    
    #######################################################################################################
    # Total  N from All crops
    #######################################################################################################
    def total_residue_per_crop_direct(self, data):
        """
        Calculates the total nitrogen from all crops based on direct residue data.

        Args:
            data: Data containing information about crops and their residues.

        Returns:
            float: Total nitrogen from all crops based on direct residue data.
        """
        mole_weight = 44.0 / 28.0

        EF_1 = self.loader_class.emissions_factors.get_ef_emissions_factor_1_ipcc_2019()

        result = 0
        for crop in data.__getitem__("crop_group").__dict__.keys():
            
            result += (
                self.residues_class.n_from_crop_residue_direct(data.__getitem__("crop_group").__getattribute__(crop)) * EF_1
            ) * data.__getitem__("crop_group").__getattribute__(crop).area

        return result * mole_weight

    # Fertiliser Application Totals for N20 and CO2


    def total_fertiliser_direct(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculates total direct emissions from urea and ammonium fertilizers.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total direct emissions from urea and ammonium fertilizers.
        """
        result = self.fertiliser_emissions_class.urea_N2O_direct(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_direct(
           data,  urea_proportion
        )

        return result


    def total_fertiliser_indirect(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculates total indirect emissions from urea and ammonium fertilizers.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total indirect emissions from urea and ammonium fertilizers.
        """
        result = self.fertiliser_emissions_class.urea_N2O_indirect(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_indirect(data, urea_proportion
        )

        return result
    


    def urea_co2(self, data, urea_proportion, urea_abated_proportion):
        """
        Calculates total CO2 emissions from urea application.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total CO2 emissions from urea application.
        """
        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return ((total_urea + total_urea_abated) * 0.2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation
    

    def upstream_and_inputs_and_fuel_co2(
        self,
        data,
        urea_proportion,
        diesel_kg,
        elec_kwh,
    ):
        """
        Calculates total CO2 emissions from upstream activities, inputs, and fuel usage.

        Args:
            data: Data containing information about upstream activities, inputs, and fuel usage.
            urea_proportion (float): Proportion of urea used.
            diesel_kg (float): Amount of diesel used in kilograms.
            elec_kwh (float): Amount of electricity used in kilowatt-hours.

        Returns:
            float: Total CO2 emissions from upstream activities, inputs, and fuel usage.
        """
        return (
            self.upstream_class.diesel_CO2(diesel_kg)
            + self.upstream_class.elec_CO2(elec_kwh)
            + self.upstream_class.fert_upstream_co2(data, urea_proportion
            ))
    

###############################################################################
# Water Quality EP PO4e
###############################################################################

class EutrophicationTotals:
    """
    A class to calculate various eutrophication totals based on factors like emissions, residues, fertilizers, etc.

    Attributes:
        loader_class (Loader): An instance of the Loader class to load data.
        residues_class (Residues): An instance of the Residues class to handle residue data.
        fertiliser_emissions_class (FertiliserInputs): An instance of the FertiliserInputs class to manage fertilizer emissions.
        upstream_class (Upstream): An instance of the Upstream class to deal with upstream data.

    Methods:
        create_emissions_dictionary(keys): Creates a dictionary to store emissions data.
        create_extended_emissions_dictionary(keys): Creates an extended dictionary to store emissions data including upstream.
        total_soils_NH3_and_LEACH_EP(data, urea_proportion, urea_abated_proportion): Calculates total emissions of NH3 and LEACH to soils.
        total_soils_P_LEACH_EP(data, urea_proportion, urea_abated_proportion): Calculates total emissions of P LEACH to soils.
        total_soils_EP(data, urea_proportion, urea_abated_proportion): Calculates total emissions of EP to soils.
        upstream_and_inputs_and_fuel_po4(data, urea_proportion, diesel_kg, elec_kwh): Calculates total PO4 emissions from upstream activities, inputs, and fuel usage.
    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.residues_class = Residues(ef_country)
        self.fertiliser_emissions_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)

    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary to store emissions data.

        Args:
            keys (list): List of keys to be used in the emissions dictionary.

        Returns:
            dict: A dictionary with emissions data initialized to zero.
        """
        crop_key_list = [
            "soils",
        ]

        crop_keys_dict = dict.fromkeys(keys)

        crop_emissions_dict = dict.fromkeys(crop_key_list)

        for key in crop_emissions_dict.keys():
            crop_emissions_dict[key] = copy.deepcopy(crop_keys_dict)
            for inner_k in crop_keys_dict.keys():
                crop_emissions_dict[key][inner_k] = 0
        
        return crop_emissions_dict


    def create_extended_emissions_dictionary(self, keys):
        """
        Creates an extended dictionary to store emissions data including upstream.

        Args:
            keys (list): List of keys to be used in the emissions dictionary.

        Returns:
            dict: An extended dictionary with emissions data initialized to zero, including upstream data.
        """
        crop_key_list = [
            "soils",
            "upstream"
        ]

        crop_keys_dict = dict.fromkeys(keys)

        crop_emissions_dict = dict.fromkeys(crop_key_list)

        for key in crop_emissions_dict.keys():
            crop_emissions_dict[key] = copy.deepcopy(crop_keys_dict)
            for inner_k in crop_keys_dict.keys():
                crop_emissions_dict[key][inner_k] = 0

        return crop_emissions_dict

    # SOILS
    def total_soils_NH3_and_LEACH_EP(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculates total emissions of NH3 and LEACH to soils.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total emissions of NH3 and LEACH to soils.
       
        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
            )
        )

        NH3N = self.fertiliser_emissions_class.urea_NH3(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_NH3(
           data, urea_proportion
        )

        LEACH = self.fertiliser_emissions_class.urea_nleach(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_nleach(
            data,urea_proportion
        )

        return (NH3N * indirect_atmosphere) + LEACH * 0.42 #N to PO4 0.42
    

    def total_soils_P_LEACH_EP(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculates total emissions of P LEACH to soils.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total emissions of P LEACH to soils.
        """
        PLEACH = (
            self.fertiliser_emissions_class.urea_P_leach(
                data,
                urea_proportion,
                urea_abated_proportion,
            )
            + self.fertiliser_emissions_class.n_fertiliser_P_leach(data, urea_proportion
            )
            + self.fertiliser_emissions_class.p_fertiliser_P_leach(data)
        )

        return PLEACH * 3.06


    def total_soils_EP(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculates total emissions of EP to soils.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total emissions of EP to soils.
        """
        return self.total_soils_NH3_and_LEACH_EP(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.total_soils_P_LEACH_EP(
            data,
            urea_proportion,
            urea_abated_proportion,
        )


    def upstream_and_inputs_and_fuel_po4(
        self,
        data,
        urea_proportion,
        diesel_kg,
        elec_kwh,
    ):
        """
        Calculates total PO4 emissions from upstream activities, inputs, and fuel usage.

        Args:
            data: Data containing information about upstream activities, inputs, and fuel usage.
            urea_proportion (float): Proportion of urea used.
            diesel_kg (float): Amount of diesel used in kilograms.
            elec_kwh (float): Amount of electricity used in kilowatt-hours.

        Returns:
            float: Total PO4 emissions from upstream activities, inputs, and fuel usage.
        """
        return (
            self.upstream_class.diesel_PO4(diesel_kg)
            + self.upstream_class.elec_PO4(elec_kwh)
            + self.upstream_class.fert_upstream_po4(data, urea_proportion
            ))
###############################################################################
# Air Quality
###############################################################################
class AirQualityTotals:
    """
    A class to calculate various air quality totals based on factors like emissions from soils.

    Attributes:
        loader_class (Loader): An instance of the Loader class to load data.
        fertiliser_emissions_class (FertiliserInputs): An instance of the FertiliserInputs class to manage fertilizer emissions.

    Methods:
        create_emissions_dictionary(keys): Creates a dictionary to store emissions data.
        total_soils_NH3_AQ(data, urea_proportion, urea_abated_proportion): Calculates total NH3 emissions from soils.
    """
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.fertiliser_emissions_class = FertiliserInputs(ef_country)


    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary to store emissions data.

        Args:
            keys (list): List of keys to be used in the emissions dictionary.

        Returns:
            dict: A dictionary with emissions data initialized to zero.
        """
        crop_key_list = [
            "soils",
        ]

        crop_keys_dict = dict.fromkeys(keys)

        crop_emissions_dict = dict.fromkeys(crop_key_list)

        for key in crop_emissions_dict.keys():
            crop_emissions_dict[key] = copy.deepcopy(crop_keys_dict)
            for inner_k in crop_keys_dict.keys():
                crop_emissions_dict[key][inner_k] = 0

        return crop_emissions_dict
    
    
# SOILS
    def total_soils_NH3_AQ(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Calculates total NH3 emissions from soils.

        Args:
            data: Data containing information about fertilizer application.
            urea_proportion (float): Proportion of urea used.
            urea_abated_proportion (float): Proportion of urea that is abated.

        Returns:
            float: Total NH3 emissions from soils.
        """

        NH3N = self.fertiliser_emissions_class.urea_NH3(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_NH3(data, urea_proportion
        )

        return NH3N
