# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class KvideoComp(Component):
    """A KvideoComp component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- click_data (list; optional):
    click_data.

- height (number; optional):
    The height used to specify height of video window.

- overlay_id (string; optional):
    The ID used to identify an overlay component that we register
    mouse events.

- width (number; optional):
    The width used to specify width of video window."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, overlay_id=Component.UNDEFINED, click_data=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'click_data', 'height', 'overlay_id', 'width']
        self._type = 'KvideoComp'
        self._namespace = 'kvideocomp'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'click_data', 'height', 'overlay_id', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(KvideoComp, self).__init__(**args)
