#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import os

import geopandas as gpd
import pandas as pd


def get_line_chart_data(
    processed_data_file_path,
    year_start=1961,
    year_end=2010,
    groupby_col="Country",
    countries=["Austria"],
    x="Year",
    z="Value",
):
    df = pd.read_parquet(
        processed_data_file_path,
        filters=[("Year", ">=", year_start), ("Year", "<=", year_end)],
        engine="pyarrow",
    )
    df = df.loc[df[groupby_col].isin(countries)]
    df = df.pivot(index=x, columns=[groupby_col], values=z)
    df = df.loc[:, :].div(df.iloc[0, :])
    return df


def get_geo_data(shapefile_filepath):
    shapefile_cols = ["ADMIN", "ADM0_A3", "geometry"]
    new_shapefile_cols = ["country", "country_code", "geometry"]
    gdf = gpd.read_file(shapefile_filepath)[shapefile_cols]
    gdf = gdf.loc[~(gdf["ADMIN"] == "Antarctica")]
    gdf.columns = new_shapefile_cols
    return gdf
