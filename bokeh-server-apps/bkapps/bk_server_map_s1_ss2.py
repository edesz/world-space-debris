#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Standalone Bokeh server with bar chart."""


import os

from src.bokeh_choromap_helpers import bk_choromap_wrapper
from src.data_loader import get_geo_data
from src.utils import my_flatten

# Deployment
PROJ_ROOT_DIR = os.getcwd()
# # Local Development
# PROJ_ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

bk_theme_filepath = os.path.join(PROJ_ROOT_DIR, "theme.yaml")
who_gho_processed_data_file_path = os.path.join(
    PROJ_ROOT_DIR, "data", "raw", "data.parquet.gzip"
)
# GeoData
geo_data_dir = os.path.join(PROJ_ROOT_DIR, "data", "raw")
geodata_shapefile_filepath = os.path.join(
    geo_data_dir,
    "ne_110m_admin_0_countries",
    "ne_110m_admin_0_countries.shp",
)
gdf = get_geo_data(geodata_shapefile_filepath)

# WHO, GHO data
last_year_of_data = 2018

# Section1 Sub-Section1 Choromap
years_ranges = [
    [1960, 1979],
    [1980, 1999],
    [2000, 2009],
    [2010, 2020],
]
years = list(
    range(min(my_flatten(years_ranges)), max(my_flatten(years_ranges)) + 1)
)
start_year_slider_value = 2000
cbar_low = 0
cbar_high = 10

bk_choromap_wrapper(
    who_gho_processed_data_file_path,
    gdf,
    years,
    last_year_of_data,
    start_year_slider_value,
    cbar_low,
    cbar_high,
    bk_theme_filepath,  # comment out for local development
    (850, 505),
)
