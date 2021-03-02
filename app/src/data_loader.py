#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import os

import geopandas as gpd

# import pandas as pd
# import pycountry


# def get_data_by_year(
#     year,
#     year_range_dict,
#     raw_data_dir,
#     usecols=["Country", "Beverage Types"],
#     new_col_names=["Year", "Country", "Value"],
# ):
#     filename = ""
#     for k, v in year_range_dict.items():
#         if any(e == year for e in v):
#             filename = f"{k}.csv"
#     filepath = os.path.join(raw_data_dir, filename)
#     df = pd.read_csv(filepath, header=1, usecols=usecols + [" " + str(year)])
#     df = df[df["Beverage Types"] == " All types"].drop(
#         columns=["Beverage Types"], axis=1
#     )
#     df = df.set_index(["Country"]).unstack().reset_index()
#     df.columns = new_col_names
#     df = df.dropna()
#     return df.copy()


# def get_data(year, year_range_dict, raw_data_dir, usecols, new_col_names):
#     df = get_data_by_year(
#         year,
#         year_range_dict,
#         raw_data_dir,
#         usecols=usecols,
#         new_col_names=new_col_names,
#     )
#     d = {
#         "Bolivia (Plurinational State of)": "BOL",
#         "Democratic People's Republic of Korea": "PRK",
#         "Democratic Republic of the Congo": "COD",
#         "Iran (Islamic Republic of)": "IRN",
#         "Micronesia (Federated States of)": "FSM",
#         "Republic of Korea": "KOR",
#         "Republic of Moldova": "MDA",
#         "United Kingdom of Great Britain and Northern Ireland": "GBR",
#         "United Republic of Tanzania": "TZA",
#         "United States of America": "USA",
#         "Venezuela (Bolivarian Republic of)": "VEN",
#     }
#     codes = []
#     for _, row in df.iterrows():
#         country = row["Country"].split(r" (")[0]
#         try:
#             code = pycountry.countries.get(name=country).alpha_3
#         except:
#             if row["Country"] in list(d.keys()):
#                 code = d[row["Country"]]
#             else:
#                 code = row["Country"]
#         codes.append(code)
#     df["Code"] = codes
#     return df


def get_geo_data(shapefile_filepath):
    shapefile_cols = ["ADMIN", "ADM0_A3", "geometry"]
    new_shapefile_cols = ["country", "country_code", "geometry"]
    gdf = gpd.read_file(shapefile_filepath)[shapefile_cols]
    gdf = gdf.loc[~(gdf["ADMIN"] == "Antarctica")]
    gdf.columns = new_shapefile_cols
    return gdf
