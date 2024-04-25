# 🐄🐏 Livstock generation tool for cattle herds and sheep flocks
[![license](https://img.shields.io/badge/License-MIT%203.0-red)](https://github.com/GOBLIN-Proj/livestock_generation/blob/0.1.0/LICENSE)
[![python](https://img.shields.io/badge/python-3.9-blue?logo=python&logoColor=white)](https://github.com/GOBLIN-Proj/livestock_generation)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


 Based on the [GOBLIN](https://gmd.copernicus.org/articles/15/2239/2022/) (**G**eneral **O**verview for a **B**ackcasting approach of **L**ivestock **IN**tensification) Cattle herd module. The package is designed to take as inputs the scenario parameters, while outputing dataframes of animal parameters for scenarios and the chosen baseline year. It also contains classes to export milk and beef outputs. 

 The package contains libraries for both catchment and national herd generation. For national herd generation, the package is shipped with key data for past herd numbers, concentrate feed inputs, and animal features. The catchment level herd numbers rely on data derived from CSO Ireland. 

 The package is structured as: 

  ```
    src/
    │
    ├── livestock_generation/
    │   └── ... (other modules and sub-packages)
        │
        ├── geo_livestock_generation/
        |   └── ... (other modules and sub-packages)

 ```
 
The ```geo_livestock_generation``` modules are used for catchment level analysis, while the ```livestock_generation``` modules are used for national 
level analysis. 

The package is currently parameterised for Ireland, the framework can be adapted for other contexts.

Outputs dataframes based on scenario inputs in relation to:

    -   Livestock by cohort
    -   Livestock population
    -   Daily milk
    -   Live weight
    -   Forage type
    -   Grazing type
    -   Concentrate input type and quantity
    -   Time outdoors, indoors and stabled
    -   Wool
    -   Manure management systems
    -   Daily spread systems
    -   Number bought and sold


## Installation

Install from git hub. 

```bash
pip install "livestock_generation@git+https://github.com/GOBLIN-Proj/livestock_generation.git@main" 

```

Install from PyPI

```bash
pip install livestock_generation
```

## Usage
```python
from livestock_generation.livestock import AnimalData
from livestock_generation.livestock_exports import Exports
import pandas as pd
import os


def main():

    # Create the DataFrame with the provided data, this represents scenario inputs
    path = "./data/"

    scenario_dataframe = pd.read_csv(os.path.join(path, "scenario_input_dataframe.csv"))

    # create additional parameters
    baseline_year = 2020
    target_year = 2050
    ef_country = "ireland"

    # create classes for the generation of animal data and livestock ouput data
    animal_class = AnimalData(ef_country, baseline_year, target_year, scenario_dataframe)
    export_class = Exports(ef_country, baseline_year, target_year, scenario_dataframe)

    # create dataframe for baseline year animals
    baseline_data = animal_class.create_baseline_animal_dataframe()

    # create dataframe for scenarios animals
    scenario_data = animal_class.create_animal_dataframe()

    scenario_data.to_csv("./data/example_scenario_animal_data_test.csv")

if __name__ == "__main__":
    main()
    
```
## License
This project is licensed under the terms of the MIT license.
