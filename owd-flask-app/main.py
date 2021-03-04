#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Flask main script."""


import os

import yaml
from bokeh.embed import server_document
from flask import Flask, render_template

PROJ_ROOT_DIR = os.getcwd()
app_config_filepath = os.path.join(PROJ_ROOT_DIR, "flask_app_config.yaml")

with open(app_config_filepath) as f:
    params = yaml.safe_load(os.path.expandvars(f.read()))

deploy = params["deploy"]
deployed_bokeh_server_app_name = params["deployed_bokeh_server_app_name"]
standalone_bokeh_apps = params["standalone_bokeh_apps"]

if deploy:
    # Heroku
    BOKEH_URLS = {
        sname: f"https://{deployed_bokeh_server_app_name}.com/{bokeh_app}"
        for sname, bokeh_app in standalone_bokeh_apps.items()
    }
else:
    BOKEH_URLS = {
        sname: f"http://localhost:5006/{bokeh_app}"
        for sname, bokeh_app in standalone_bokeh_apps.items()
    }

app = Flask(__name__)


@app.route("/", methods=["GET"])
def bkapp_page():
    script = {
        "1": {
            "1": {
                "map": server_document(BOKEH_URLS["s1_ss1_map"]),
                "chart": server_document(BOKEH_URLS["s1_ss1_chart"]),
            },
            "2": {
                "map": server_document(BOKEH_URLS["s1_ss2_map"]),
                "chart": server_document(BOKEH_URLS["s1_ss2_chart"]),
            },
        }
    }
    # OWD Themed HTML document
    return render_template("embed.html", script=script)
    # # Blank HTML document for quick testing
    # return render_template("embed_basic.html", script=script)
