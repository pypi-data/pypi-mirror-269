"""
Module implementing the navbar header components
"""
import os
from typing import Dict
from typing import Optional

import dash_mantine_components as dmc
from dash import html


def app_logo(logo_path: str = '/assets/logo.png',
             ratio: float = 24/9):
    """
    Application logo component.
    """
    return dmc.AspectRatio(dmc.Image(src=logo_path), 
                           ratio=ratio,
                           style={'margin-left': '10px', 'width':'25%'})


def app_title(app_name: str | None = None, color='white'):
    """
    Application title component.
    """
    app_name = app_name or os.getenv('app_name')
    return html.Div(dmc.Title(os.getenv('app_name'), c=color, fz='2vw'))


logo = app_logo()
title = app_title()


def navbar_header(app_logo: html.Div = logo,
                  app_title: html.Div = title):
    """
    Application header, composed of an app logo and title components.
    """
    return dmc.GridCol(span='auto', children=[
                       dmc.Group([app_logo, app_title], 
                                 justify='space-around')
                   ])
