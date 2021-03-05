<div align="center">
  <h1>Visualizing Space Debris using Flask-embedded Bokeh Apps </h1>
</div>

<div align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-brightgreen.svg"></a>
  <a href="https://github.com/edesz/world-space-debris/pulls"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>
  <a href="https://github.com/edesz/world-space-debris/actions">
    <img src="https://github.com/edesz/world-space-debris/workflows/CodeQL/badge.svg"/>
  </a>
  <a href="https://en.wikipedia.org/wiki/Open-source_software"><img alt="Open Source?: Yes" src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github"></a>
  <a href="https://pyup.io/repos/github/edesz/world-space-debris/"><img src="https://pyup.io/repos/github/edesz/world-space-debris/shield.svg" alt="Updates" /></a>
</div>

<div align="center">
<a href="https://www.python.org/">
  <img alt="Made With: Python" src="https://forthebadge.com/images/badges/made-with-python.svg"/>
</a>
<a href="https://html.com/">
  <img alt="Uses: HTML" src="https://forthebadge.com/images/badges/uses-html.svg"/>
</a>
</div>

## [Table of Contents](#table-of-contents)
-   [About](#about)

-   [Usage](#usage)
    -   [Local Development](#local-development)
    -   [Deployment](#deployment)

-   [Notes](#notes)

-   [Attributions](#attributions)

-   [Future Improvements](#future-improvements)

## [About](#about)
This is a project to explore space debris by using the Python packages [Bokeh](https://docs.bokeh.org/en/latest/index.html) and [Flask](https://flask.palletsprojects.com/en/1.1.x/) (run via the [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) server [Gunicorn](https://gunicorn.org/)) to implement a simplified version of the visualizations used by [Our World in Data's obesity exploration](https://ourworldindata.org/obesity).

A secondary objective is to deploy the simplified visualization built here to the cloud using [Heroku](https://www.heroku.com/).

## [Notes](#notes)
1.  At the time of initial development of this project, [`numba` is not supported on Python 3.9](https://github.com/numba/numba/issues/5855) and so the [next supported version](https://devcenter.heroku.com/articles/python-support#supported-runtimes) of Python (3.8.8) was used.
2.  This is work in progress. Currently, only boilerplate code is put in place. Active analysis is being conduced in `./Untitled.ipynb`.

## [Attributions](#attributions)
1.  (Boilerplate content) [WHO GHO Dataset](https://apps.who.int/gho/data/node.main.A1022?lang=en) and (Space Debris) [Space-Track API](https://www.space-track.org/auth/login)
2.  [Three letter country codes](https://laendercode.net/en/3-letter-list.html) (not used here, used the Python package [`pcountry`](https://pypi.org/project/pycountry/) instead)
3.  As mentioned earlier, the primary motivation for this project was the analysis of world obesity, done by [Our World in Data](https://ourworldindata.org/obesity).

## [Future Improvements](#future-improvements)
1.  Choromap colorbar scale needs to be set based on ALL years' data
    -   to adjust this, change `cbar_low` and `cbar_high` using
        ```python
        cbar_low = df["Value"].min()
        cbar_high = df["Value"].max()
        ```

## [Usage](#usage)
### [Local Development](#local-development)
In order to download the data, run
```bash
make get-data
```

For locally testing standalone Bokeh apps, follow the three steps below

1.  In `./owd-flask-app/flask_app_config.yaml`, change `deploy: True` to `deploy: False`

2.  Comment out lines related to specifying a path to and using a Bokeh theme file
    -   in `./bokeh-server-apps/src/bokeh_choromap_helpers.py`, lines 126 and 198
    -   in `./bokeh-server-apps/src/bokeh_linechart_helpers.py`, lines 103 and 182
    -   in `.bokeh-server-apps/bokeh_server_map_s1_ss1.py` and `.bokeh-server-apps/bokeh_server_map_s1_ss2.py`
        -   line 57
        -   line 15 and uncomment line 17
    -   in `.bokeh-server-apps/bokeh_server_chart_s1_ss1.py`
        -   line 69
        -   line 14 and uncomment line 16

3.  Change into the `bkapps` directory by running
    ```bash
    cd bokeh-server-apps/bkapps
    ```

    and then run **one** of the following during local development
    ```bash
    bokeh serve bk_server_map_s1_ss1.py
    bokeh serve bk_server_map_s1_ss2.py
    bokeh serve bk_server_chart_s1_ss1.py
    ```

For locally testing Bokeh apps embedded in a Flask application (using a simple HTML document), follow the steps below from the project's root directory

1.  In `owd-flask-app/main.py`,

    -   comment out line 54 (which uses the full HTML template, with inheritance, etc.) and uncomment line 56 (to access the simplified HTML template)

### [Deployment](#deployment)
1.  From the project's root directory, run
    ```bash
    make heroku-create
    ```
