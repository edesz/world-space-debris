#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os
from functools import lru_cache

import pandas as pd
from bokeh.layouts import row
from bokeh.models import Button, Column, GeoJSONDataSource, Slider
from bokeh.themes import Theme

from src.bokeh_choromap_helpers import bokeh_setup_create_choromap
from src.utils import my_flatten

PROJ_ROOT_DIR = os.getcwd()
who_gho_processed_data_file_path = os.path.join(
    PROJ_ROOT_DIR, "data", "raw", "data.parquet.gzip"
)

# WHO, GHO data
last_year_of_data = 2018

# Section1 Sub-Section1 Choromap
years_ranges = [
    [1960, 1979],
    [1980, 1999],
    [2000, 2009],
    [2010, 2020],
]
# year_range_dict = {
#     f"data2_{min(years)}_{max(years)}": list(range(min(years), max(years) + 1))
#     for years in years_ranges
# }
years = list(
    range(min(my_flatten(years_ranges)), max(my_flatten(years_ranges)) + 1)
)
start_year_slider_value = 2000
cbar_low = 0
cbar_high = 10


def s1_ss1_choromap(doc):
    @lru_cache
    def get_json_data(year):
        df = pd.read_parquet(
            who_gho_processed_data_file_path,
            filters=[("Year", "=", year)],
            engine="pyarrow",
        )
        df_merged = gdf.merge(
            df, right_on="Code", left_on="country_code", how="left"
        )
        df_merged = df_merged.fillna("No Data")
        df_merged_json = json.loads(df_merged.to_json())
        json_data = json.dumps(df_merged_json)
        return json_data

    slider = Slider(
        title="Year",
        start=min(years),
        end=last_year_of_data,
        step=1,
        value=start_year_slider_value,
        tooltips=True,
        width=725,
    )
    geodata = GeoJSONDataSource(geojson=get_json_data(slider.value))
    choro_tooltip = [
        ("Country", "@country"),
        ("Alcohol per capita Consumed", "@Value"),
        ("Year", "@Year"),
    ]
    p = bokeh_setup_create_choromap(
        choro_tooltip,
        geodata,
        start_year_slider_value,
        cbar_low,
        cbar_high,
        [950, 600],
    )

    def animate_update():
        year = slider.value + 1
        if year > last_year_of_data:
            year = years[0]
        slider.value = year

    def update_plot(attr, old, new):
        year = slider.value
        new_data = get_json_data(year)
        geodata.geojson = new_data
        p.title.text = f"Alcohol Consumption by Country - {year}"

    slider.on_change("value", update_plot)

    callback_id = None

    def animate():
        global callback_id
        if button.label == "► Play":
            button.label = "◼ Stop"
            callback_id = doc.add_periodic_callback(animate_update, 200)
        else:
            button.label = "► Play"
            doc.remove_periodic_callback(callback_id)

    button = Button(label="► Play", width=60, button_type="primary")
    button.on_click(animate)

    layout = Column(p, row(button, Column(slider)))
    doc.add_root(layout)
    doc.theme = Theme(filename="theme.yaml")
