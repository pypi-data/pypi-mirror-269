# 🌾 Crop_lca, a lifecycle assessment tool for cropping systems in Ireland
[![license](https://img.shields.io/badge/License-MIT-red)](https://github.com/GOBLIN-Proj/crop_lca/blob/0.1.0/LICENSE)
[![python](https://img.shields.io/badge/python-3.9-blue?logo=python&logoColor=white)](https://github.com/GOBLIN-Proj/crop_lca)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

 Based on the [GOBLIN](https://gmd.copernicus.org/articles/15/2239/2022/) (**G**eneral **O**verview for a **B**ackcasting approach of **L**ivestock **IN**tensification) LifeCycle Analysis tool, the Crop_lca module decouples this module making it an independent distribution package.

 The package is shipped with key data for emissions factors, fertiliser inputs, crop characteristics and upstream emissions. 

 Currently parameterised for Ireland, but the database can be updated with additional emissions factor contexts, which are selected able with an emissions factor key. 

 Final results are output as a dictionary object capturing emissions for:

    -   crop_residue_direct
    -   N_direct_fertiliser
    -   N_indirect_fertiliser
    -   soils_CO2

## Structure
 The package is structured for use in national and catchment level analysis. 

 The geo_crop_lca sub module is intended for use at the catchment level and interfaces with the catchment_data_api to 
 retrieve catchment specific crop areas and types data that has been retrieved from [Ireland's National Land Cover map](https://www.epa.ie/our-services/monitoring--assessment/assessment/mapping/national-land-cover-map/) and merged with crop types using the [LUCAS land cover dataset](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=LUCAS_-_Land_use_and_land_cover_survey).

 ```
    src/
    │
    ├── crop_lca/
        └── ... (other modules and sub-packages)
        │
        ├── geo_crop_lca/
        |   └── ... (other modules and sub-packages)

 ```
## Installation

Install from git hub. 

```bash
pip install "crop_lca@git+https://github.com/GOBLIN-Proj/crop_lca.git@main" 

```
Install from PyPI

```bash
pip install crop_lca
```

## Usage
```python
import pandas as pd
from crop_lca.models import load_crop_farm_data
from crop_lca.lca import ClimateChangeTotals
from crop_lca.national_crop_production import NationalCropData


def main():
    # Instantiate ClimateChange Totals Class, passing Ireland as the emissions factor country
    climatechange = ClimateChangeTotals("ireland")

    # Create a dictionary to store results
    index = 2020
    crop_emissions_dict = climatechange.create_emissions_dictionary([index])

    # Create some data to generate results
    data = NationalCropData.gen_national_crop_production_dataframe(index)
    
    data_frame = pd.DataFrame(data)

    #proportion of fertiliser inputs that is urea
    urea_proportion =0.2
    urea_abated_proportion = 0
    # generate results and store them in the dictionary

    data = load_crop_farm_data(data_frame)

    crop_emissions_dict["crop_residue_direct"][index] += (
        climatechange.total_residue_per_crop_direct(
            data[index],
        )
    )
    crop_emissions_dict["N_direct_fertiliser"][index] += (
        climatechange.total_fertiliser_direct(
            data[index],
            urea_proportion,
            urea_abated_proportion,
        )
        
    )
    crop_emissions_dict["N_indirect_fertiliser"][index] += (
        climatechange.total_fertiliser_indirect(
            data[index],
            urea_proportion,
            urea_abated_proportion,
        )
    )
    crop_emissions_dict["soils_N2O"][index] += (
        crop_emissions_dict["crop_residue_direct"][index]
        + crop_emissions_dict["N_direct_fertiliser"][index]
        + crop_emissions_dict["N_indirect_fertiliser"][index]
    )
    crop_emissions_dict["soils_CO2"][index] += (
        climatechange.urea_co2(
            data[index],
            urea_proportion,
            urea_abated_proportion,
        )
        
    )

    print(crop_emissions_dict)


if __name__ == "__main__":
    main()

```
## License
This project is licensed under the terms of the MIT license.
