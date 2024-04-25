"""
Data Loader
===========
This module contains the Loader class, which is used to load data from the database and create instances of the models used in the crop LCA model.
"""
from crop_lca.resource_manager.database_manager import DataManager
from crop_lca.models import (
    Fertiliser,
    CropChars,
    Upstream,
    Emissions_Factors,
)


class Loader:
    """
    The Loader class is used to load data from the database and create instances of the models used in the crop LCA model.

    Attributes
    ----------
    ef_country : str
        The name of the country for which the data is being loaded.
    dataframes : DataManager
        An instance of the DataManager class used to load data from the database.
    crop_chars : CropChars
        An instance of the CropChars class used to manage the crop characteristics data.
    fertiliser : Fertiliser
        An instance of the Fertiliser class used to manage the fertiliser data.
    emissions_factors : Emissions_Factors
        An instance of the Emissions_Factors class used to manage the emissions factor data.
    upstream : Upstream
        An instance of the Upstream class used to manage the upstream data.

    Methods
    -------
    get_crop_chars()
        Returns an instance of the CropChars class.
    get_fertiliser()
        Returns an instance of the Fertiliser class.
    get_emissions_factors()
        Returns an instance of the Emissions_Factors class.
    get_upstream()
        Returns an instance of the Upstream class.
    get_national_crop_production()
        Returns the national crop production data.
    get_fao_yield_data(ef_country, index=None)
        Returns the FAO yield data for the specified country.

    """
    def __init__(self, ef_country = None):
        self.ef_country = ef_country if ef_country else None
        self.dataframes = DataManager(ef_country)
        self.crop_chars = self.get_crop_chars()
        self.fertiliser = self.get_fertiliser()
        self.emissions_factors = self.get_emissions_factors()
        self.upstream = self.get_upstream()

    def get_crop_chars(self):
        """
        Returns an instance of the CropChars class.

        Returns
        -------
        CropChars
            An instance of the CropChars class used to manage the crop characteristics data.
        """
        return CropChars(self.dataframes.crop_char_data())

    def get_fertiliser(self):
        """
        Returns an instance of the Fertiliser class.

        Returns
        -------
        Fertiliser
            An instance of the Fertiliser class used to manage the fertiliser data.
        """
        return Fertiliser(self.dataframes.fertiliser_data())

    def get_emissions_factors(self):
        """
        Returns an instance of the Emissions_Factors class.

        Returns
        -------
        Emissions_Factors
            An instance of the Emissions_Factors class used to manage the emissions factor data.
        """
        return Emissions_Factors(self.dataframes.emissions_factor_data())

    def get_upstream(self):
        """
        Returns an instance of the Upstream class.
        
        Returns
        -------
        Upstream
            An instance of the Upstream class used to manage the upstream data.
        """
        return Upstream(self.dataframes.upstream_data())
    
    def get_national_crop_production(self):
        """
        Returns the national crop production data.

        Returns
        -------
        pd.DataFrame
            The national crop production data.
        """
        return self.dataframes.cso_crop_data()
    
    def get_fao_yield_data(self, ef_country, index=None):
        """
        Returns the FAO yield data for the specified country.

        Parameters
        ----------
        ef_country : str
            The name of the country for which the data is being loaded.
        index : int, optional
            The index of the data to be returned.

        Returns
        -------
        pd.DataFrame
            The FAO yield data for the specified country.
            
        """
        return self.dataframes.fao_production_data(ef_country, index=index)
