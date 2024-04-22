# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdSpin(Component):
    """An AntdSpin component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the tab - will only be displayed if this tab is
    selected.

- id (string; optional)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- className (string | dict; optional)

- data-* (string; optional):
    `data-*`格式属性通配.

- debug (boolean; default False)

- delay (number; optional)

- excludeProps (list of strings; optional)

- fullscreen (boolean; default False)

- includeProps (list of strings; optional)

- indicator (a list of or a singular dash component, string or number; optional)

- key (string; optional)

- listenPropsMode (a value equal to: 'default', 'exclude', 'include'; default 'default')

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- size (a value equal to: 'small', 'middle', 'large'; default 'middle')

- spinning (boolean; default False)

- style (dict; optional)

- text (string; optional)

- wrapperClassName (string | dict; optional)"""
    _children_props = ['indicator']
    _base_nodes = ['indicator', 'children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdSpin'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, wrapperClassName=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, spinning=Component.UNDEFINED, size=Component.UNDEFINED, delay=Component.UNDEFINED, text=Component.UNDEFINED, fullscreen=Component.UNDEFINED, debug=Component.UNDEFINED, listenPropsMode=Component.UNDEFINED, excludeProps=Component.UNDEFINED, includeProps=Component.UNDEFINED, indicator=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'className', 'data-*', 'debug', 'delay', 'excludeProps', 'fullscreen', 'includeProps', 'indicator', 'key', 'listenPropsMode', 'loading_state', 'size', 'spinning', 'style', 'text', 'wrapperClassName']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'className', 'data-*', 'debug', 'delay', 'excludeProps', 'fullscreen', 'includeProps', 'indicator', 'key', 'listenPropsMode', 'loading_state', 'size', 'spinning', 'style', 'text', 'wrapperClassName']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AntdSpin, self).__init__(children=children, **args)
