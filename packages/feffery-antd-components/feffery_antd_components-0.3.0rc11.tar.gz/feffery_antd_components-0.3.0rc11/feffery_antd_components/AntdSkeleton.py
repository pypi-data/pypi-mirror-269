# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdSkeleton(Component):
    """An AntdSkeleton component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional)

- active (boolean; default False)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- avatar (dict; default False)

    `avatar` is a boolean | dict with keys:

    - active (boolean; optional)

    - shape (a value equal to: 'circle', 'square'; optional)

    - size (number | a value equal to: 'large', 'small', 'default'; optional)

- className (string | dict; optional)

- data-* (string; optional):
    `data-*`格式属性通配.

- debug (boolean; default False)

- delay (number; default 0):
    设置加载延时时长，单位：毫秒  默认：0.

- excludeProps (list of strings; optional)

- includeProps (list of strings; optional)

- key (string; optional)

- listenPropsMode (a value equal to: 'default', 'exclude', 'include'; default 'default')

- loading (boolean; default False)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- paragraph (dict; default True)

    `paragraph` is a boolean | dict with keys:

    - rows (number; optional)

    - width (number | string | list of number | strings; optional)

- round (boolean; default False)

- style (dict; optional)

- title (dict; default True)

    `title` is a boolean | dict with keys:

    - width (number | string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdSkeleton'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, loading=Component.UNDEFINED, active=Component.UNDEFINED, delay=Component.UNDEFINED, avatar=Component.UNDEFINED, paragraph=Component.UNDEFINED, title=Component.UNDEFINED, round=Component.UNDEFINED, debug=Component.UNDEFINED, listenPropsMode=Component.UNDEFINED, excludeProps=Component.UNDEFINED, includeProps=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'active', 'aria-*', 'avatar', 'className', 'data-*', 'debug', 'delay', 'excludeProps', 'includeProps', 'key', 'listenPropsMode', 'loading', 'loading_state', 'paragraph', 'round', 'style', 'title']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'active', 'aria-*', 'avatar', 'className', 'data-*', 'debug', 'delay', 'excludeProps', 'includeProps', 'key', 'listenPropsMode', 'loading', 'loading_state', 'paragraph', 'round', 'style', 'title']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AntdSkeleton, self).__init__(children=children, **args)
