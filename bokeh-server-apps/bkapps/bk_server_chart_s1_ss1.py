#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Standalone Bokeh server with line chart."""


import os

from src.bokeh_linechart_helpers import bk_linechart_wrapper
from src.data_loader import get_line_chart_data

PROJ_ROOT_DIR = os.getcwd()
# PROJ_ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# print(PROJ_ROOT_DIR)
bk_theme_filepath = os.path.join(PROJ_ROOT_DIR, "theme.yaml")
who_gho_processed_data_file_path = os.path.join(
    PROJ_ROOT_DIR, "data", "raw", "data.parquet.gzip"
)

# WHO, GHO data
first_year_of_data = 1961
last_year_of_data = 2018
start_year_slider_value = 2000

groupby_col = "Code"
nlargest = 15
x = "Year"
z = "Value"
# Top 15 countries by avg. alcohol consumption over all years in dataset
# - df.groupby(["Code"])["Value"].mean().nlargest(15).index.tolist()
countries = [
    "FRA",
    "LUX",
    "PRT",
    "DEU",
    "ESP",
    "HUN",
    "SVN",
    "CZE",
    "ITA",
    "AUT",
    "EST",
    "CHE",
    "BHS",
    "ARG",
    "SVK",
]

df_initial = get_line_chart_data(
    who_gho_processed_data_file_path,
    year_start=first_year_of_data,
    year_end=start_year_slider_value,
    groupby_col="Code",
    countries=countries,
    x="Year",
    z="Value",
)

bk_linechart_wrapper(
    who_gho_processed_data_file_path,
    first_year_of_data,
    last_year_of_data,
    start_year_slider_value,
    df_initial,
    countries,
    bk_theme_filepath,
    (850, 505),
)
