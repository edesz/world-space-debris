#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bokeh.models import ColorBar, HoverTool, Label, LinearColorMapper
from bokeh.palettes import YlOrRd9
from bokeh.plotting import figure


def bokeh_choromap_setup(tooltip, cbar_low=0, cbar_high=10):
    # Instantiate LinearColorMapper that maps numbers to a sequence of colors.
    geojson_colormap = YlOrRd9[::-1]
    color_mapper = LinearColorMapper(
        palette=geojson_colormap, low=cbar_low, high=cbar_high
    )

    # Add the hovering tooltips.
    hover = HoverTool(tooltips=tooltip)

    # Create the color bar.
    color_bar = ColorBar(
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
    p.title.text_font_size = "12pt"
    p.title.text_font_style = "normal"
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
    caption1 = Label(
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
