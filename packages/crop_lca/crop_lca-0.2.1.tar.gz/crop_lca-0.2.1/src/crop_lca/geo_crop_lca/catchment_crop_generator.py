"""
Catchment Crop Generator
========================
This module contains the CatchmentCropGenerator class which is used to generate a dataframe of catchment crops.
"""
from crop_lca.resource_manager.data_loader import Loader
from catchment_data_api.crops import Crops
from crop_lca.resource_manager.crop_lca_data_manager import CropDataManager
import pandas as pd

class CatchmentCropGenerator:
    """
    The CatchmentCropGenerator class is used to generate a dataframe of catchment crops.
        
    Attributes
    ----------
    crop_data_manager : CropDataManager
        An instance of the CropDataManager class used to manage the crop data.
    catchment : str
        The name of the catchment for which the data is being generated.
    ef_country : str
        The name of the country for which the data is being generated.
    loader : Loader
        An instance of the Loader class used to load data from the database.
    crops_api : Crops
        An instance of the Crops class used to access the catchment data.

    Methods
    -------
    gen_catchment_crop_dataframe()
        Returns a dataframe of catchment crops.

    """
    def __init__(self, ef_country, catchment):
        self.crop_data_manager = CropDataManager()
        self.catchment = catchment
        self.ef_country = ef_country
        self.loader = Loader(ef_country)
        self.crops_api = Crops()


    def gen_catchment_crop_dataframe(self):
        """
        Returns a dataframe of catchment crops.

        Returns
        -------
        pandas.DataFrame
            A dataframe of catchment crops.
        """
        catchment_crops = self.crops_api._derive_crops(self.catchment)
        fao_yield_data = self.loader.get_fao_yield_data(self.ef_country)
        crop_tuples = self.crop_data_manager.get_catchment_to_param_crop_names()

        data = []

        for crop_dataframe_name, fao_name, param_name in crop_tuples:  
            if crop_dataframe_name in catchment_crops["crop"].values:
                if fao_name is not None and fao_name in fao_yield_data["Item"].values:
                    mask = fao_yield_data["Item"] == fao_name
                    catchment_crops_mask = catchment_crops["crop"] == crop_dataframe_name
                    dm_crop = fao_yield_data.loc[mask, "fm_value"].item() * self.loader.crop_chars.get_crop_dry_matter(param_name)

                    row = {
                        "crop_type": crop_dataframe_name,
                        "param_name": param_name,
                        "kg_dm_per_ha": dm_crop,
                        "area_ha": catchment_crops.loc[catchment_crops_mask, "area_ha"].item()
                    }
                    data.append(row)

        return pd.DataFrame(data)


    