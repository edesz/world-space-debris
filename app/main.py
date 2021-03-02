#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
from threading import Thread

import pandas as pd
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.server.server import BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from flask import Flask, render_template
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import src.bokeh_apps as bk_apps
from src.data_loader import get_geo_data

PROJ_ROOT_DIR = os.getcwd()
# GeoData
geo_data_dir = os.path.join(PROJ_ROOT_DIR, "data", "raw")
geodata_shapefile_filepath = os.path.join(
    geo_data_dir,
    "ne_110m_admin_0_countries",
    "ne_110m_admin_0_countries.shp",
)
gdf = get_geo_data(geodata_shapefile_filepath)

PORT = os.environ.get("PORT", 8000)

app = Flask(__name__)

# can't use shortcuts here, since we are passing to low level BokehTornado
bkapp = Application(FunctionHandler(bk_apps.s1_ss1_choromap))
bkapp2 = Application(FunctionHandler(bk_apps.s1_ss1_choromap))

# This is so that if this app is run using something like "gunicorn -w 4" then
# each process will listen on its own port
sockets, port = bind_sockets("localhost", 0)


@app.route("/", methods=["GET"])
def bkapp_page():
    script = {
        "one": {
            "one": {
                "ex": "1",
                "text": "text.html",
                "table": "table.html",
                "map": server_document(f"http://localhost:{port}/bkapp"),
                "chart": server_document(f"http://localhost:{port}/bkapp2"),
            },
            # "two": {
            #     "three": server_document(f"http://localhost:{port}/bkapp3"),
            #     "four": server_document(f"http://localhost:{port}/bkapp4"),
            # },
        }
    }
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    asyncio.set_event_loop(asyncio.new_event_loop())

    bokeh_tornado = BokehTornado(
        {
            "/bkapp": bkapp,
            "/bkapp2": bkapp2,
            # "/bkapp3": bkapp3,
            # "/bkapp4": bkapp4,
        },
        extra_websocket_origins=[f"localhost:{PORT}"],
    )
    bokeh_http = HTTPServer(bokeh_tornado)
    bokeh_http.add_sockets(sockets)

    server = BaseServer(IOLoop.current(), bokeh_tornado, bokeh_http)
    server.start()
    server.io_loop.start()


t = Thread(target=bk_worker)
t.daemon = True
t.start()
