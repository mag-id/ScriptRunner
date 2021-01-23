"""Plotly Dash app."""

from typing import Dict, List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, callback_context
from dash.dependencies import Input, Output
from exceptions import StopScriptRunnerExc
from filehandler import config_handler, script_handler
from pipeline import submit_tasks

__all__ = ["app"]

app = Dash(__name__, prevent_initial_callbacks=False)


app.layout = html.Div(
    children=[
        html.H1("ScriptRunner"),
        html.Div(
            id="config",
            children=[
                html.H2("Configs"),
                dcc.Dropdown(id="config-dropdown"),
                dcc.Textarea(id="config-textarea"),
                dbc.Button("update", id="config-update"),
                html.Div(id="config-input"),
                html.Div(id="config-output"),
            ],
        ),
        html.Div(
            id="script",
            children=[
                html.H2("Scripts"),
                dcc.Dropdown(id="script-dropdown"),
                dcc.Textarea(id="script-textarea"),
                html.Div(id="script-input"),
            ],
        ),
        html.Div(
            id="submit",
            children=[
                html.Button("Submit scripts queue", id="submit-button", n_clicks=0),
                html.Div(id="submit-output"),
            ],
        ),
    ]
)


@app.callback(
    Output(component_id="config-dropdown", component_property="options"),
    Input(component_id="config-input", component_property="children"),
    prevent_initial_call=False,
)
def update_configs_dropdown(_) -> List[Dict]:
    """
    Checks `config_handler.directory` and writes all names into `config-dropdown` menu.
    """
    return [{"label": name, "value": name} for name in config_handler.file_names]


@app.callback(
    Output(component_id="script-dropdown", component_property="options"),
    Input(component_id="script-input", component_property="children"),
    prevent_initial_call=False,
)
def update_scripts_dropdown(_) -> List[Dict]:
    """
    Checks `script_handler.directory` and writes all names into `script-dropdown` menu.
    """
    return [{"label": name, "value": name} for name in script_handler.file_names]


@app.callback(
    Output(component_id="config-textarea", component_property="value"),
    Input(component_id="config-dropdown", component_property="value"),
    prevent_initial_call=False,
)
def get_config(value: str) -> str or None:
    """
    Returns content of the selected in `config-dropdown`
    menu file and places it into `config-textarea`.
    """
    return config_handler.read_file(name=value) if value else None


@app.callback(
    Output(component_id="script-textarea", component_property="value"),
    Input(component_id="script-dropdown", component_property="value"),
    prevent_initial_call=False,
)
def get_script(value: str) -> str or None:
    """
    Returns content of the selected in `script-dropdown`
    menu file and places it into `script-textarea`.
    """
    return script_handler.read_file(name=value) if value else None


# https://stackoverflow.com/questions/62671226/
def triggered_by(id_: str) -> bool:
    """
    Returns `True` if `id_` in the input triggers.
    """
    return id_ in [item["prop_id"] for item in callback_context.triggered][0]


@app.callback(
    Output(component_id="config-output", component_property="children"),
    [
        Input(component_id="config-update", component_property="n_clicks"),
        Input(component_id="config-dropdown", component_property="value"),
        Input(component_id="config-textarea", component_property="value"),
    ],
    prevent_initial_call=True,
)
def update_config(n_clicks: int, name_value: str or None, content_value: str or None):
    """
    Updates `config-textarea` content of the selected in `config-dropdown`
    menu file after `config-update` trigger (button pressing).
    """
    if triggered_by("config-update.n_clicks") and name_value:
        config_handler.write_file(name=name_value, content=content_value)


@app.callback(
    Output(component_id="submit-output", component_property="children"),
    Input(component_id="submit-button", component_property="n_clicks"),
    prevent_initial_call=True,
)
def submit(n_clicks):
    """
    Calls `pipline.submit_tasks` function.
    """
    try:
        submit_tasks()
    except StopScriptRunnerExc:
        pass
