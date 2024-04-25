# catchment_data_api
[![license](https://img.shields.io/badge/License-MIT-red)](https://github.com/GOBLIN-Proj/catchment_data_api/blob/0.1.0/LICENSE)
[![python](https://img.shields.io/badge/python-3.9-blue?logo=python&logoColor=white)](https://github.com/GOBLIN-Proj/catchment_data_api)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

API for retrieval of catchment data for land cover and livestock. The package uses data derived from the [National Landcover Map](https://www.tailte.ie/en/surveying/products/professional-mapping/national-land-cover-map/), 
[the Teagasc Soils Map](https://www.teagasc.ie/environment/soil/soil-maps/) and [LUCAS crop map](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=LUCAS_-_Land_use_and_land_cover_survey).

## Installation

Install from github 

```bash
pip install "cathment_data_api@git+https://github.com/GOBLIN-Proj/catchment_data_api.git@main" 
```

Install from PyPI

```bash
pip install catchment_data_api
```


## Usage

```python 
from catchment_data_api import catchment_data_api

def main():
    api = catchment_data_api.CatchmentDataAPI()
    df = api.get_catchment_livestock_data()

    print(df.head())

    df1 = api.get_catchment_livestock_data_by_catchment_name("blackwater")

    print(df1.head())

    print(api.get_catchment_names())

    df2 = api.get_catchment_livestock_total_pop_by_catchment_name("blackwater")

    print(df2.head())



if __name__ == "__main__":
    main()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`catchment_data_api` was created by Colm Duffy. It is licensed under the terms of the MIT license.

## Credits

`catchment_data_api` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
