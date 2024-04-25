"""
Database Manager
================
This module contains the DataManager class, which is used to access the crop
data stored in the crop database.
"""
import sqlalchemy as sqa
import pandas as pd
from crop_lca.database import get_local_dir
import os


class DataManager:
    """
    The DataManager class is used to access the crop data stored in the crop database.

    Attributes
    ----------
    database_dir : str
        The path to the directory containing the crop database.
    engine : sqlalchemy.engine.base.Engine
        The engine used to connect to the crop database.
    ef_country : str
        The name of the country for which the data is being accessed.

    Methods
    -------
    data_engine_creater()
        Returns the engine used to connect to the crop database.
    crop_char_data(index=None)
        Returns the crop characteristics data.
    upstream_data(index=None)
        Returns the upstream data.
    emissions_factor_data(index=None)
        Returns the emissions factor data.
    fertiliser_data(index=None)
        Returns the fertiliser data.
    cso_crop_data(index=None)
        Returns the CSO crop production data.
    fao_production_data(ef_country, index=None)
        Returns the FAO production data for the specified country.
    """
    def __init__(self, ef_country=None):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()
        self.ef_country = ef_country if ef_country else None

    def data_engine_creater(self):
        """
        Returns the engine used to connect to the crop database.

        Returns
        -------
        sqlalchemy.engine.base.Engine
            The engine used to connect to the crop database.
        """
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "crop_database.db")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)

    def crop_char_data(self, index=None):
        """
        Returns the crop characteristics data.

        Parameters
        ----------
        index : str, optional
            The column to use as the index for the returned dataframe.

        Returns
        -------
        pandas.core.frame.DataFrame
            The crop characteristics data.
        """
        table = "crop_params"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def upstream_data(self, index=None):
        """
        Returns the upstream data.
        
        Parameters
        ----------
        index : str, optional
            The column to use as the index for the returned dataframe.

        Returns
        -------
        pandas.core.frame.DataFrame
            The upstream data.
        """
        table = "upstream_crop"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def emissions_factor_data(self, index=None):
        """
        Returns the emissions factor data.
        
        Parameters
        ----------
        index : str, optional
            The column to use as the index for the returned dataframe.

        Returns
        -------
        pandas.core.frame.DataFrame
            The emissions factor data.
        """
        table = "emission_factor_crop"

        if index == None:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
            )

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def fertiliser_data(self, index=None):
        """
        Returns the fertiliser data.

        Parameters
        ----------
        index : str, optional
            The column to use as the index for the returned dataframe.

        Returns
        -------
        pandas.core.frame.DataFrame
            The fertiliser data.
        """
        table = "fertiliser_crop"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe
    

    def cso_crop_data(self, index=None):
        """
        Returns the CSO crop production data.

        Parameters
        ----------
        index : str, optional
            The column to use as the index for the returned dataframe.

        Returns
        -------
        pandas.core.frame.DataFrame
            The CSO crop production data.
        """
        table = "cso_crop_production_data"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=["Year"],
            )

        dataframe["Hectares_000"] *= 1000

        return dataframe

    def fao_production_data(self, ef_country, index=None):
        """
        Returns the FAO production data for the specified country.

        Parameters
        ----------
        ef_country : str
            The name of the country for which the data is being accessed.

        index : str, optional
            The column to use as the index for the returned dataframe.

        Returns
        -------
        pandas.core.frame.DataFrame
            The FAO production data for the specified country.
        """
        table = "FAOSTAT_yield_data"

        ef_country = ef_country.capitalize()

        if index is None:
            query = "SELECT * FROM %s WHERE ef_country = '%s'" % (table, ef_country)
            dataframe = pd.read_sql(query, self.engine)
        else:
            query = "SELECT * FROM %s WHERE ef_country = '%s'" % (table, ef_country)
            dataframe = pd.read_sql(query, self.engine, index_col=[index])

        return dataframe