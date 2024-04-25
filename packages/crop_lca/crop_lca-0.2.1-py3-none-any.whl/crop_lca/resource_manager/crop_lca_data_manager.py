"""
Crop data manager
=================

This module contains the CropDataManager class which is used to manage the crop data used in the crop LCA model. 
The class contains a method to get the crop names used in the crop LCA model.

"""

class CropDataManager:
    """
    The CropDataManager class is used to manage the crop data used in the crop LCA model.

    Attributes
    ----------
    catchment_to_param_crop_names : list
        A list of tuples containing the crop names used in the catchment data and the parameter names used in the crop LCA model.

    Methods
    -------
    get_catchment_to_param_crop_names()
        Returns the list of tuples containing the crop names used in the catchment data and the parameter names used in the crop LCA model.
    """
    def __init__(self):
        self.catchment_to_param_crop_names = [
            ("Common wheat", "Wheat", "grains"),
            ("Sunflower", "Peas, dry", "beans_pulses"),
            ("Rapeseed and turnip rapeseed", "Rape or colza seed", "crops"),
            ("Barley", "Barley", "barley"),
            ("Maize", "Oats", "maize"),
            ("Sugar beet", "Leeks and other alliaceous vegetables", "crops"),
            ("Dry pulses", "Peas, dry", "beans_pulses"),
            ("Bare arable land", None, None)
        ]

    def get_catchment_to_param_crop_names(self):
        return self.catchment_to_param_crop_names