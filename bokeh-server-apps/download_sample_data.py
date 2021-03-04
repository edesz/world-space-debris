#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Data retrieval script."""


import logging
import os
import urllib.request
from glob import glob
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import pycountry

import pandas as pd


def requests_download_data(filepath, url, down_msg, stop_msg):
    logger = logging.getLogger(__name__)
    if not os.path.exists(filepath):
        logger.info(down_msg)
        folder_path, ext = os.path.splitext(filepath)
        if ext == ".zip":
            with urlopen(url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(folder_path)
        else:
            urllib.request.urlretrieve(url, filepath)
        logger.info("Done")
    else:
        logger.info(stop_msg)


def download_geo_data(raw_data_dir):
    url = (
        "https://www.naturalearthdata.com/http//www.naturalearthdata.com/"
        "download/110m/cultural/ne_110m_admin_0_countries.zip"
    )
    zip_filename = os.path.basename(url)

    filepath = os.path.join(raw_data_dir, zip_filename)
    requests_download_data(
        filepath,
        url,
        f"Downloading geodata...",
        "Found geodata locally. Doing nothing.",
    )


def download_data(years_ranges, raw_data_dir):
    for s_e in years_ranges:
        years = list(range(min(s_e), max(s_e) + 1))[::-1]
        year_str = [f";YEAR:{year}" for year in years]
        url = (
            "https://apps.who.int/gho/athena/data/xmart.csv?target=GHO/"
            "SA_0000001400&profile=crosstable&filter=COUNTRY:*"
            f"{''.join(year_str)}&x-sideaxis=COUNTRY;DATASOURCE;ALCOHOLTYPE&x"
            "-topaxis=GHO;YEAR"
        )

        filepath = os.path.join(
            raw_data_dir, f"data2_{min(years)}_{max(years)}.csv"
        )
        requests_download_data(
            filepath,
            url,
            f"Downloading years in range {min(years)}-{max(years)}...",
            (
                f"Found data for years in range {min(years)}-{max(years)}. "
                "Doing nothing."
            ),
        )


def get_country_codes(df, d):
    codes = []
    for _, row in df.iterrows():
        country = row["Country"].split(r" (")[0]
        try:
            code = pycountry.countries.get(name=country).alpha_3
        except:
            if row["Country"] in list(d.keys()):
                code = d[row["Country"]]
            else:
                code = row["Country"]
        codes.append(code)
    df["Code"] = codes
    return df


def combine_process_data(files, new_col_names, d, processed_data_file_path):
    logger = logging.getLogger(__name__)

    if os.path.exists(processed_data_file_path):
        logger.info("Found processed data. Doing nothing.")
    else:
        logger.info("Processing data...")
        dfs = [pd.read_csv(file, header=1) for file in files]

        # Get file with maximum number of countries
        dfs = []
        max_countries_idx = 0
        max_countries = 0
        for f_idx, file in enumerate(files):
            df = pd.read_csv(file, header=1)
            df = df[df["Beverage Types"] == " All types"].drop(
                columns=["Beverage Types", "Data Source"], axis=1
            )
            if df["Country"].nunique() > max_countries:
                max_countries_idx = f_idx
                max_countries = df["Country"].nunique()
            dfs.append(df)
        # LEFT JOIN file with maximum number of countries with other files
        df_non_max_countries = [
            dfs[i] for i, v in enumerate(dfs) if i != max_countries_idx
        ]
        df = dfs[max_countries_idx]
        for df_i in df_non_max_countries:
            df = df.merge(df_i, how="left", on=["Country"])

        # Reshape tidy data to support parquet-filters when loading file
        df = df.drop_duplicates(keep="first")
        df = df.set_index(["Country"]).unstack().reset_index()
        df.columns = new_col_names
        df = df.dropna()

        # Formatting
        df["Year"] = df["Year"].astype(int)

        # Get country codes
        df = get_country_codes(df, d)

        # Sort
        df = df.sort_values(["Year", "Value"], ascending=[True, False])

        df.to_parquet(
            processed_data_file_path,
            compression="gzip",
            index=False,
            engine="pyarrow",
        )
        logger.info("Done...")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    PROJ_ROOT_DIR = os.getcwd()
    raw_data_dir = os.path.join(PROJ_ROOT_DIR, "data", "raw")
    processed_data_file_path = os.path.join(
        PROJ_ROOT_DIR, "data", "raw", "data.parquet.gzip"
    )

    years_ranges = [
        [1960, 1979],
        [1980, 1999],
        [2000, 2009],
        [2010, 2020],
    ]

    download_data(years_ranges, raw_data_dir)
    download_geo_data(raw_data_dir)

    new_col_names = ["Year", "Country", "Value"]
    d = {
        "Bolivia (Plurinational State of)": "BOL",
        "Democratic People's Republic of Korea": "PRK",
        "Democratic Republic of the Congo": "COD",
        "Iran (Islamic Republic of)": "IRN",
        "Micronesia (Federated States of)": "FSM",
        "Republic of Korea": "KOR",
        "Republic of Moldova": "MDA",
        "United Kingdom of Great Britain and Northern Ireland": "GBR",
        "United Republic of Tanzania": "TZA",
        "United States of America": "USA",
        "Venezuela (Bolivarian Republic of)": "VEN",
    }
    combine_process_data(
        glob(os.path.join(raw_data_dir, "data2_*.csv")),
        new_col_names,
        d,
        processed_data_file_path,
    )
