"""
Catchment Crop Production
=========================
This module contains the CatchmentCropData class which is used to generate a dataframe of catchment crops and a dataframe of scenario crops.

In addition, the class also handles the generation of farm data (fertiliser inputs) for the crop LCA model.
"""
from crop_lca.resource_manager.data_loader import Loader
from crop_lca.geo_crop_lca.catchment_crop_generator import CatchmentCropGenerator
import pandas as pd 

class CatchmentCropData:
    """
    The CatchmentCropData class is used to generate a dataframe of catchment crops and a dataframe of scenario crops, as well as to generate farm data (fertiliser inputs) for the crop LCA model.

    Methods
    -------
    gen_catchment_crop_production_dataframe(ef_country, catchment, year)
        Returns a dataframe of catchment crops.

    gen_scenario_crop_production_dataframe(ef_country, catchment, calibration_year, target_year, scenario= None, crop_dataframe=None)
        Returns a dataframe of scenario crops.

    gen_farm_data(crop_dataframe, urea_proportion, default_urea, default_urea_abated)
        Returns a dataframe of farm data (fertiliser inputs).
    """
    @classmethod
    def gen_catchment_crop_production_dataframe(cls, ef_country, catchment, year):
        """
        Returns a dataframe of catchment crops.

        Parameters
        ----------
        ef_country : str
            The name of the country for which the data is being generated.
        catchment : str
            The name of the catchment for which the data is being generated.
        year : int
            The year for which the data is being generated.

        Returns
        -------
        pandas.DataFrame
            A dataframe of catchment crops.
        """
        catchment_crop_generator = CatchmentCropGenerator(ef_country, catchment)
        catchment_crops = catchment_crop_generator.gen_catchment_crop_dataframe()
        
        data =[]

        for crop in catchment_crops.crop_type.unique():
            
            row = {
                "ef_country": ef_country,
                "farm_id": year,
                "year": year,
                "crop_type": catchment_crops.loc[catchment_crops["crop_type"]==crop, "param_name"].item(),
                "lucas_crop_type": crop,
                "kg_dm_per_ha": catchment_crops.loc[catchment_crops["crop_type"]==crop, "kg_dm_per_ha"].item(),
                "area": catchment_crops.loc[catchment_crops["crop_type"]==crop, "area_ha"].item()
            }
            data.append(row)

        return pd.DataFrame(data)
    

    @classmethod
    def gen_scenario_crop_production_dataframe(cls,ef_country,catchment, calibration_year, target_year, scenario= None, crop_dataframe=None):
        """
        Returns a dataframe of scenario crops.

        Parameters
        ----------
        ef_country : str
            The name of the country for which the data is being generated.
        catchment : str
            The name of the catchment for which the data is being generated.
        calibration_year : int
            The year for which the calibration data is being generated.
        target_year : int
            The year for which the scenario data is being generated.
        scenario : int, optional
            The scenario for which the data is being generated. The default is None.
        crop_dataframe : pandas.DataFrame, optional
            A dataframe of crop data. The default is None.

        Returns
        -------
        pandas.DataFrame
            A dataframe of scenario crops.
        """
        catchment_crop_generator = CatchmentCropGenerator(ef_country, catchment)
        catchment_crops = catchment_crop_generator.gen_catchment_crop_dataframe()

        if crop_dataframe is None:
            catchment_crop_df = CatchmentCropData.gen_catchment_crop_production_dataframe(ef_country,catchment, calibration_year)
        else:
            catchment_crop_df = crop_dataframe
        
        data = []
        for crop in catchment_crops.crop_type.unique():
            
            row = {
                "ef_country": ef_country,
                "farm_id": scenario,
                "year": target_year,
                "crop_type": catchment_crops.loc[catchment_crops["crop_type"]==crop, "param_name"].item(),
                "lucas_crop_type": crop,
                "kg_dm_per_ha": catchment_crops.loc[catchment_crops["crop_type"]==crop, "kg_dm_per_ha"].item(),
                "area": catchment_crops.loc[catchment_crops["crop_type"]==crop, "area_ha"].item()
            }
            
            data.append(row)
        
        scenario_crop_dataframe = pd.DataFrame(data)

        return pd.concat([catchment_crop_df, scenario_crop_dataframe], ignore_index=True) 

    @classmethod
    def gen_farm_data(cls, crop_dataframe, urea_proportion, default_urea, default_urea_abated):
        """
        Returns a dataframe of farm data (fertiliser inputs).

        Parameters
        ----------
        crop_dataframe : pandas.DataFrame
            A dataframe of crop data.

        urea_proportion : pandas.DataFrame
            A dataframe of urea proportions.

        default_urea : float
            The default urea proportion.

        default_urea_abated : float
            The default urea abated proportion.

        Returns
        -------
        pandas.DataFrame
            A dataframe of farm data (fertiliser inputs).
        """
        loader_class = Loader()

        application_rate = loader_class.get_fertiliser()


        cols = [
            "ef_country",
            "farm_id",
            "total_urea",
            "total_urea_abated",
            "total_n_fert",
            "total_p_fert",
            "total_k_fert",
        ]

        farm_data = pd.DataFrame(columns=cols)

        
        for sc in crop_dataframe.farm_id.unique():
            farm_data.at[sc, "ef_country"] = "ireland"
            farm_data.at[sc, "farm_id"] = sc

            farm_data.at[sc, "total_urea"] = 0
            farm_data.at[sc, "total_urea_abated"] = 0
            farm_data.at[sc, "total_n_fert"] = 0
            farm_data.at[sc, "total_p_fert"] = 0
            farm_data.at[sc, "total_k_fert"] = 0

            for crop in crop_dataframe.crop_type.unique():

                try:
                    urea_value = urea_proportion.at[sc, "Urea proportion"]

                    urea_abated_value = urea_proportion.at[sc, "Urea abated proportion"]
                
                except KeyError:
                    urea_value = default_urea
                    urea_abated_value = default_urea_abated


                mask = ((crop_dataframe["farm_id"]== sc) & (crop_dataframe["crop_type"]==crop))

                farm_data.at[sc, "total_urea"] += crop_dataframe.loc[mask, "area"].item() *(application_rate.get_fert_kg_n_per_ha(crop)
                        * urea_value)

                farm_data.at[sc, "total_urea_abated"] += crop_dataframe.loc[mask, "area"].item() * (crop_dataframe.loc[mask, "area"].item() * (application_rate.get_fert_kg_n_per_ha(crop)
                        * urea_value * urea_abated_value))

                farm_data.at[sc, "total_n_fert"] += crop_dataframe.loc[mask, "area"].item() *(application_rate.get_fert_kg_n_per_ha(crop)
                        * (1 -urea_value))
                
                farm_data.at[sc, "total_p_fert"] += crop_dataframe.loc[mask, "area"].item() * application_rate.get_fert_kg_p_per_ha(crop)
                farm_data.at[sc, "total_k_fert"] += crop_dataframe.loc[mask, "area"].item() * application_rate.get_fert_kg_k_per_ha(crop)

        return farm_data

