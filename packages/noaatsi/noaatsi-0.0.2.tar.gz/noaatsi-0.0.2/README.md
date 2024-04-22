# noaatsi
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/5710884/tree )

takefuji (2022) noaatsi: a PyPI for displaying TSI graph based on NOAA [Source Code]. https://doi.org/10.24433/CO.6916537.v1

This is under review.

noaatsi is a PyPI package application to scrape the updated data from NOAA on TSI and to display the TSI graph.
Data is stored in the following site which will be automatically scraped by noaatsi:

https://www.ncei.noaa.gov/data/total-solar-irradiance/access/yearly/tsi_v02r01_yearly_s1610_e2021_c20220202.nc

NOAA file is based on netCDF4.
In order to read .nc file, netCDF4 library is needed. To install it, run the following command.

$ pip install netCDF4

In order to install noaatsi, run the following command.

$ pip install noaatsi

To generate TSI file (tsi.csv) and the graph on the screen (tsi.png), run the following command.

$ noaatsi


noaatsi.png is finally generated.

<img src='https://github.com/y-takefuji/noaatsi/raw/main/noaatsi.png' height=300 width=900>
