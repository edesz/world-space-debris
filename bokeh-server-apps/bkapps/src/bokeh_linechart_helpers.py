#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from functools import lru_cache

import bokeh.models as bkm
from bokeh.layouts import row
from bokeh.palettes import Category20
from bokeh.plotting import curdoc, figure
from bokeh.themes import Theme

from src.data_loader import get_line_chart_data


def bokeh_create_multiline_plot(
    data,
    x,
    y_names,
    lw=2,
    ptitle="Title",
    axis_tick_font_size="12pt",
    plot_titleFontSize="14pt",
    legend_axis_gap=5,
    fig_size=(700, 400),
):
    col_names = data.column_names[1:]
    color = Category20[len(data.column_names[1:])]
    p = figure(
        plot_width=fig_size[0],
        plot_height=fig_size[1],
        toolbar_location=None,
        tools="",
    )
    p_dict = dict()
    for col, c, col_name in zip(y_names, color, col_names):
        p_dict[col_name] = p.line(
            x,
            col,
            source=data,
            color=c,
            line_width=lw,
            line_alpha=1.0,
            line_color=c,
        )
        p.add_tools(
            bkm.HoverTool(
                renderers=[p_dict[col_name]],
                tooltips=[(x, f"@{x}"), (col, f"@{col}")],
            )
        )

    legend = bkm.Legend(
        items=[(x, [p_dict[x]]) for x in p_dict],
        location="top_right",
        orientation="vertical",
    )
    p.hover.point_policy = "follow_mouse"
    p.add_layout(legend, "right")
    p.legend.border_line_alpha = 0
    p.legend.background_fill_alpha = 0
    p.xaxis.major_label_text_font_size = axis_tick_font_size
    p.yaxis.major_label_text_font_size = axis_tick_font_size
    p.title.text_font_size = plot_titleFontSize
    p.legend.label_text_font_size = axis_tick_font_size
    p.title.text = ptitle
    p.legend.border_line_width = 0
    p.legend.padding = 0
    p.legend.margin = legend_axis_gap

    # Remove whitespace
    p.x_range.range_padding = 0
    p.y_range.range_padding = 0

    # Whitespace around plots in grid?
    p.min_border_top = 0
    p.min_border_bottom = 0

    # Add data source text label
    label_opts = dict(
        x=-35,
        y=0,
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


def bk_linechart_wrapper(
    who_gho_processed_data_file_path,
    first_year_of_data,
    last_year_of_data,
    start_year_slider_value,
    df_initial,
    countries,
    theme_filepath,  # comment out for local development
    fig_width=(850, 600),
):
    @lru_cache
    def get_json_data(year):
        df = get_line_chart_data(
            who_gho_processed_data_file_path,
            year_start=first_year_of_data,
            year_end=year,
            groupby_col="Code",
            countries=countries,
            x="Year",
            z="Value",
        )
        # print(first_year_of_data, year, df.shape)
        return df

    slider = bkm.Slider(
        title="Year",
        start=first_year_of_data,
        end=last_year_of_data,
        step=1,
        value=start_year_slider_value,
        tooltips=True,
        width=725,
    )
    data = dict(Year=df_initial.index.tolist())
    for c in countries:
        data[c] = df_initial[c].tolist()
    source = bkm.ColumnDataSource(data=data)
    p = bokeh_create_multiline_plot(
        source,
        "Year",
        countries,
        2,
        ptitle=(
            f"Alcohol Consumption relative to {first_year_of_data}, "
            f"{first_year_of_data}-{start_year_slider_value}"
        ),
        axis_tick_font_size="12pt",
        plot_titleFontSize="14pt",
        legend_axis_gap=5,
        fig_size=fig_width,
    )

    def animate_update():
        year = slider.value + 1
        if year > last_year_of_data:
            year = first_year_of_data
        slider.value = year

    def update_plot(attr, old, new):
        year = slider.value
        new_data = get_json_data(year)
        source.data = new_data
        p.title.text = (
            f"Alcohol Consumption relative to {first_year_of_data}, "
            f"{first_year_of_data}-{year}"
        )

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
    # Theme - comment out for local development
    curdoc().theme = Theme(filename=theme_filepath)
