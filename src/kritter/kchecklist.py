#
# This file is part of Kritter 
#
# All Kritter source code is provided under the terms of the
# GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
# Those wishing to use Kritter source code, software and/or
# technologies under different licensing terms should contact us at
# support@charmedlabs.com. 
#

import dash_bootstrap_components as dbc
from dash_devices.dependencies import Input, Output
import dash_html_components as html
from kritter import Kritter, Kcomponent
from functools import wraps

HEIGHT = 150

class Kchecklist(Kcomponent):
    def __init__(self, **kwargs):
        super().__init__('Kchecklist', **kwargs)

        options = kwargs['options'] if 'options' in kwargs else []
        value = kwargs['value'] if 'value' in kwargs else [] 
        scrollable = kwargs['scrollable'] if 'scrollable' in kwargs else False
        clear_check_all = kwargs['clear_check_all'] if 'clear_check_all' in kwargs else False

        button = dbc.Button(Kritter.icon("chevron-right", padding=0), disabled=self.disabled, size="sm")
        options = [{'label': option, 'value': option} for option in options]
        self.checklist = dbc.Checklist(options=options, value=value, id=self.id+"-checklist")
        if clear_check_all:
            check_all = html.Button(Kritter.icon("check-square", padding=0), id=self.id+"-checkall", style={"margin": "2px 2px 2px 0", "border-width": "0"})
            clear_all = html.Button(Kritter.icon("square-o", padding=0), id=self.id+"-clearall", style={"margin": "2px", "border-width": "0"})
            po_children = [
                html.Div([check_all, clear_all]),
                html.Div(self.checklist)]

            @self.kapp.callback(None, [Input(check_all.id, "n_clicks")], service=self.service)
            def func(val):
                value = [option['value'] for option in self.checklist.options]
                return Output(self.checklist.id, "value", value)

            @self.kapp.callback(None, [Input(clear_all.id, "n_clicks")], service=self.service)
            def func(val):
                return Output(self.checklist.id, "value", [])
        else:
            po_children = self.checklist

        if scrollable:
            style = {"padding": "5px", "max-height": f"{HEIGHT}px", "overflow-y": "auto"}
        else:
            style = {"padding": "5px"}
        po_body = html.Div(po_children, style=style)
        po = dbc.Popover(po_body, id=self.id+"po", trigger="legacy", hide_arrow=True)
        self.set_layout(button)
        self.cols.append(po)
        po.target = button.id

        @self.kapp.callback(None, [Input(po.id, "is_open")])
        def func(_open):
            icon = "chevron-left" if _open else "chevron-right"
            return Output(button.id, "children", Kritter.icon(icon, padding=0))

    def callback(self, state=()):
        def wrap_func(func):
            @wraps(func)
            @self.kapp.callback(None,
                [Input(self.checklist.id, 'value')], state, self.service)
            def _func(*args):
                return func(*args)
        return wrap_func

    def out_options(self, options):
        options = [{'label': option, 'value': option} for option in options]
        return [Output(self.checklist.id, "options", options)]

    def out_value(self, value):
        return [Output(self.checklist.id, "value", value)]
