#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bokeh.models import HoverTool, Legend
from bokeh.palettes import Category20
from bokeh.plotting import figure


def bokeh_create_multiline_plot(
    data,
    x,
    x_start,
    x_end,
    y_names,
    lw=2,
    ptitle="Title",
    t_str="",
    t_loc="above",
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
            HoverTool(
                renderers=[p_dict[col_name]],
                tooltips=[(x, f"@{x}"), (col, f"@{col}")],
            )
        )

    legend = Legend(
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
    p.title.text = f"{ptitle}, {x_start}-{x_end}"
    p.legend.border_line_width = 0
    p.legend.padding = 0
    p.legend.margin = legend_axis_gap
    return p
