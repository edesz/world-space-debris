#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from functools import lru_cache

import bokeh.models as bkm
import pandas as pd
from bokeh.layouts import row
from bokeh.palettes import YlOrRd9
from bokeh.plotting import curdoc, figure
from bokeh.themes import Theme


def bokeh_choromap_setup(tooltip, cbar_low=0, cbar_high=10):
    # Instantiate LinearColorMapper that maps numbers to a sequence of colors.
    geojson_colormap = YlOrRd9[::-1]
    color_mapper = bkm.LinearColorMapper(
        palette=geojson_colormap, low=cbar_low, high=cbar_high
    )

    # Add the hovering tooltips.
    hover = bkm.HoverTool(tooltips=tooltip)

    # Create the color bar.
    color_bar = bkm.ColorBar(
        color_mapper=color_mapper,
        label_standoff=4,
        width=650,
        height=10,
        border_line_color=None,
        bar_line_alpha=1,
        bar_line_color="#A9A9A9",
        major_tick_in=0,
        bar_line_width=0.75,
        major_label_text_font_size="9pt",
        location=(50, 0),  # (0,0) or 'center'
        orientation="horizontal",
    )
    return [hover, color_bar, color_mapper]


def create_choromap_figure(
    hover, geosource, color_bar, color_mapper, year, fig_size=[950, 600]
):
    p = figure(
        title=f"Alcohol Consumption by Country - {year}",
        plot_height=fig_size[1],
        plot_width=fig_size[0],
        toolbar_location=None,
        tools=[hover],
    )
    p.hover.point_policy = "follow_mouse"
    # Remove the grid lines.
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    # Remove figure frame
    p.outline_line_color = None
    # Remove axes
    p.axis.visible = False
    p.grid.visible = False
    # Remove whitespace
    p.x_range.range_padding = 0
    p.y_range.range_padding = 0
    # Configure Plot title
    p.title.text_font_size = "14pt"
    p.title.text_font_style = "bold"
    # Show color bar below plot
    p.add_layout(color_bar, "below")
    # GeoDataSource patch
    p.patches(
        "xs",
        "ys",
        source=geosource,
        fill_color={"field": "Value", "transform": color_mapper},
        line_color="black",
        line_width=0.5,
        fill_alpha=1,
    )
    # Whitespace around plots in grid?
    p.min_border_top = 0
    p.min_border_bottom = 0
    # Add data source text label
    label_opts = dict(
        x=0,
        y=5,
        text_align="left",
        text_font_size="12px",
        text_color="#888888",
        x_units="screen",
        y_units="screen",
    )
    caption1 = bkm.Label(
        text="Source: WHO, Global Health Observatory", **label_opts
    )
    p.add_layout(caption1, "below")
    return p


def bokeh_setup_create_choromap(
    tooltip,
    geodata,
    year,
    cbar_low=0,
    cbar_high=10,
    fig_size=[950, 600],
):
    hover, color_bar, color_mapper = bokeh_choromap_setup(
        tooltip, cbar_low, cbar_high
    )
    p = create_choromap_figure(
        hover, geodata, color_bar, color_mapper, year, fig_size
    )
    return p


def bk_choromap_wrapper(
    who_gho_processed_data_file_path,
    gdf,
    years,
    last_year_of_data,
    start_year_slider_value,
    cbar_low,
    cbar_high,
    bk_theme_filepath,  # comment out for local development
    fig_width=(850, 600),
):
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

    slider = bkm.Slider(
        title="Year",
        start=min(years),
        end=last_year_of_data,
        step=1,
        value=start_year_slider_value,
        tooltips=True,
        width=725,
    )
    geodata = bkm.GeoJSONDataSource(geojson=get_json_data(slider.value))
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
        fig_width,
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
            callback_id = curdoc().add_periodic_callback(animate_update, 200)
        else:
            button.label = "► Play"
            curdoc().remove_periodic_callback(callback_id)

    button = bkm.Button(label="► Play", width=60, button_type="primary")
    button.on_click(animate)

    layout = bkm.Column(p, row(button, bkm.Column(slider)))
    curdoc().add_root(layout)
    # Set theme - comment out below for local development
    curdoc().theme = Theme(filename=bk_theme_filepath)
