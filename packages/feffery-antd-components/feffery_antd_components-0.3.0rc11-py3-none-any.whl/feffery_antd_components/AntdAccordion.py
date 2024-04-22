# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdAccordion(Component):
    """An AntdAccordion component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional)

- accordion (boolean; default True)

- activeKey (string | list of strings | number | list of numbers; optional)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- bordered (boolean; default True)

- className (string | dict; optional)

- collapsible (a value equal to: 'header', 'disabled', 'icon'; optional)

- data-* (string; optional):
    `data-*`格式属性通配.

- defaultActiveKey (string | list of strings | number | list of numbers; optional)

- expandIconPosition (a value equal to: 'left', 'right'; default 'left')

- ghost (boolean; default False)

- items (list of dicts; optional)

    `items` is a list of dicts with keys:

    - children (a list of or a singular dash component, string or number; optional)

    - className (string | dict; optional)

    - collapsible (a value equal to: 'header', 'disabled', 'icon'; optional)

    - extra (a list of or a singular dash component, string or number; optional)

    - forceRender (boolean; optional)

    - key (string | number; required)

    - showArrow (boolean; optional)

    - style (dict; optional)

    - title (a list of or a singular dash component, string or number; optional)

- key (string; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- style (dict; optional)"""
    _children_props = ['items[].children', 'items[].title', 'items[].extra']
    _base_nodes = ['children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdAccordion'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, items=Component.UNDEFINED, accordion=Component.UNDEFINED, activeKey=Component.UNDEFINED, defaultActiveKey=Component.UNDEFINED, bordered=Component.UNDEFINED, collapsible=Component.UNDEFINED, expandIconPosition=Component.UNDEFINED, ghost=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accordion', 'activeKey', 'aria-*', 'bordered', 'className', 'collapsible', 'data-*', 'defaultActiveKey', 'expandIconPosition', 'ghost', 'items', 'key', 'loading_state', 'style']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'accordion', 'activeKey', 'aria-*', 'bordered', 'className', 'collapsible', 'data-*', 'defaultActiveKey', 'expandIconPosition', 'ghost', 'items', 'key', 'loading_state', 'style']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AntdAccordion, self).__init__(children=children, **args)
