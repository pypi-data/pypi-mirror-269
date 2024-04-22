# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdAvatar(Component):
    """An AntdAvatar component.


Keyword arguments:

- id (string; optional)

- alt (string; optional)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- className (string | dict; optional)

- crossOrigin (a value equal to: 'anonymous', 'use-credentials', ''; optional)

- data-* (string; optional):
    `data-*`格式属性通配.

- draggable (boolean | a value equal to: 'true', 'false'; optional)

- gap (number; default 4)

- icon (string; optional)

- iconRenderer (a value equal to: 'AntdIcon', 'fontawesome'; default 'AntdIcon')

- key (string; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- mode (a value equal to: 'text', 'icon', 'image'; default 'icon')

- shape (a value equal to: 'circle', 'square'; default 'circle')

- size (dict; default 'default')

    `size` is a number | a value equal to: 'large', 'small', 'default'
    | dict with keys:

    - lg (number; optional)

    - md (number; optional)

    - sm (number; optional)

    - xl (number; optional)

    - xs (number; optional)

    - xxl (number; optional)

- src (string; optional)

- srcSet (string; optional)

- style (dict; optional)

- text (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdAvatar'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, mode=Component.UNDEFINED, gap=Component.UNDEFINED, text=Component.UNDEFINED, icon=Component.UNDEFINED, iconRenderer=Component.UNDEFINED, alt=Component.UNDEFINED, src=Component.UNDEFINED, srcSet=Component.UNDEFINED, draggable=Component.UNDEFINED, crossOrigin=Component.UNDEFINED, size=Component.UNDEFINED, shape=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'alt', 'aria-*', 'className', 'crossOrigin', 'data-*', 'draggable', 'gap', 'icon', 'iconRenderer', 'key', 'loading_state', 'mode', 'shape', 'size', 'src', 'srcSet', 'style', 'text']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'alt', 'aria-*', 'className', 'crossOrigin', 'data-*', 'draggable', 'gap', 'icon', 'iconRenderer', 'key', 'loading_state', 'mode', 'shape', 'size', 'src', 'srcSet', 'style', 'text']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AntdAvatar, self).__init__(**args)
