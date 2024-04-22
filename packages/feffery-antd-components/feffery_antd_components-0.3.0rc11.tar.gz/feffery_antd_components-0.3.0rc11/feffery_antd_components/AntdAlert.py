# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdAlert(Component):
    """An AntdAlert component.


Keyword arguments:

- id (string; optional)

- action (a list of or a singular dash component, string or number; optional)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- banner (boolean; default False)

- className (string | dict; optional)

- closable (boolean; default False)

- data-* (string; optional):
    `data-*`格式属性通配.

- description (a list of or a singular dash component, string or number; optional)

- key (string; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- message (a list of or a singular dash component, string or number; optional)

- messageRenderMode (a value equal to: 'default', 'loop-text', 'marquee'; default 'default')

- showIcon (boolean; default False)

- style (dict; optional)

- type (a value equal to: 'success', 'info', 'warning', 'error'; default 'info')"""
    _children_props = ['message', 'description', 'action']
    _base_nodes = ['message', 'description', 'action', 'children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdAlert'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, message=Component.UNDEFINED, description=Component.UNDEFINED, type=Component.UNDEFINED, showIcon=Component.UNDEFINED, closable=Component.UNDEFINED, messageRenderMode=Component.UNDEFINED, action=Component.UNDEFINED, banner=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'action', 'aria-*', 'banner', 'className', 'closable', 'data-*', 'description', 'key', 'loading_state', 'message', 'messageRenderMode', 'showIcon', 'style', 'type']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'action', 'aria-*', 'banner', 'className', 'closable', 'data-*', 'description', 'key', 'loading_state', 'message', 'messageRenderMode', 'showIcon', 'style', 'type']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AntdAlert, self).__init__(**args)
