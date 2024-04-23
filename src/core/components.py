from .translate import Translatable
from ..exceptions import InvalidArguments


__all__ = (
    "Component",
    "Input",
    "Button",
    "Metrics",
    "DisplayData",
    "Checkbox",
    "CheckboxList",
    "MessageBox",
    "Toggle",
    "Image",
    "Repeat",
    "Table",
    "Container",
    "ContainerRow",
    "Spacer",
    "InstructionBox",
)


def validate_style(style, extra_styles=None):
    supported_styles = ("default", "info", "success", "error", "warning")

    if extra_styles is not None:
        supported_styles += extra_styles

    if style not in supported_styles:
        raise InvalidArguments(
            f"Invalid style '{style}' specified. Style must be one of the following: "
            f"{', '.join(supported_styles)}"
        )
    return style


def validate_size(size):
    min_size = 1
    max_size = 12
    if not min_size <= size <= max_size:
        raise InvalidArguments(f"Size attributes must be between {min_size} and {max_size}")
    return size


class Component:
    __slots__ = [
        "_identifier",
        "destination_path",
        "flow_attrs",
        "update_context",
        "preconditions",
        "__weakref__",
        "json_validators",
    ]

    def __init__(
        self,
        identifier=None,
        destination_path=None,
        flow_attrs=None,
        update_context=None,
        preconditions=None,
        json_validators=None,
    ):
        self._identifier = identifier
        self.destination_path = destination_path
        self.flow_attrs = flow_attrs or {}
        self.update_context = update_context or []
        self.preconditions = preconditions or []
        self.json_validators = json_validators or {}

    def __iter__(self):
        yield self

    def _get_default_identifier(self):
        return self.__class__.__name__.lower()

    @property
    def identifier(self):
        return self._identifier or self._get_default_identifier()

    def get_flow_attrs(self):
        return self.flow_attrs

    def get_update_context(self):
        return self.update_context

    def get_preconditions(self):
        return [p.identifier for p in self.preconditions]

    def get_flow_component_dict(self):
        flow = {"name": self.identifier}

        if self.destination_path is not None:
            flow["destination_path"] = self.destination_path

        attrs = self.get_flow_attrs()
        if attrs:
            flow["attrs"] = attrs

        update_context = self.get_update_context()
        if update_context:
            flow["update_context"] = update_context

        preconditions = self.get_preconditions()
        if preconditions:
            flow["preconditions"] = preconditions

        return flow

    def get_base_component_dict(self):
        return {}

    def get_validators(self):
        yield from self.preconditions

    def get_json_validators(self):
        yield from self.json_validators

    def get_components(self):
        yield self


class Textbox(Component):
    __slots__ = [
        "content",
        "align",
    ]

    def __init__(self, content=None, align=None, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.align = align

    def get_base_component_dict(self):
        return {
            "type": "textbox",
            "content": self.content,
            "align": self.align
        }


class Metrics(Component):
    """ A simple component to display a metrics icon that when clicked shows
    the timing information of all the http and jsonrpc requests made by the client.
    Label is the text beside the icon"""

    __slots__ = [
        "label",
    ]

    def __init__(self, label="Metrics", **kwargs):
        super().__init__(**kwargs)
        self.label = label

    def get_base_component_dict(self):
        return {"type": "metrics", "label": self.label}


class Input(Component):
    __slots__ = [
        "component_type",
        "target",
        "input_key",
        "input_ref",
        "output_ref",
        "output",
        "obscure",
        "validators",
        "populate",
        "default_value",
        "url",
        "method",
        "payload_paths",
        "payload",
        "response_path",
        "json_validators",
        "max_length",
    ]

    label = Translatable()

    def __init__(
        self,
        component_type=None,
        target=None,
        label=None,
        input_key=None,
        input_ref=None,
        output_ref=None,
        output=None,
        obscure=False,
        validators=None,
        populate=None,
        default_value=None,
        url=None,
        method=None,
        payload_paths=None,
        payload=None,
        response_path=None,
        json_validators=None,
        max_length=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.component_type = component_type or self.__class__.__name__.lower()
        self.target = target or ""
        self.label = label or ""
        self.input_key = input_key
        self.input_ref = input_ref
        self.output_ref = output_ref
        self.output = output
        self.obscure = obscure
        self.validators = validators or []
        self.populate = populate
        self.default_value = default_value
        self.url = url
        self.method = method
        self.payload_paths = payload_paths or []
        self.payload = payload or {}
        self.response_path = response_path
        self.json_validators = json_validators or []
        # By default, limit to max 100 characters
        self.max_length = max_length or 100

    def _get_default_identifier(self):
        return "_".join([self.component_type, self.target.lower().replace(" ", "_")])

    def get_base_component_dict(self):
        component = super().get_base_component_dict()
        component.update(
            {
                "type": self.component_type,
                "label": self.label,
                "validator": [v.identifier for v in self.validators],
            }
        )

        if self.target:
            component["target"] = self.target
        if self.obscure:
            component["obscure"] = self.obscure
        if self.input_key:
            component["input_key"] = self.input_key
        if self.input_ref:
            component["input_ref"] = self.input_ref
        if self.output_ref:
            component["output_ref"] = self.output_ref
        if self.output:
            component["output"] = self.output
        if self.populate:
            component["populate"] = self.populate.as_dict()
        if self.default_value:
            component['default_value'] = self.default_value
        if self.url:
            component["url"] = self.url
        if self.method:
            component["method"] = self.method
        if self.payload_paths:
            component["payload_paths"] = self.payload_paths
        if self.payload:
            component["payload"] = self.payload
        if self.response_path:
            component["response_path"] = self.response_path
        if self.max_length:
            component["max_length"] = self.max_length
        if self.json_validators:
            component.update(
                {
                    "json_validators": [v.identifier for v in self.json_validators],
                }
            )
        return component

    def get_validators(self):
        yield from super().get_validators()
        yield from self.validators
        if self.populate:
            self.populate.get_validators()

    def get_payload(self):
        return self.payload

    def get_payload_paths(self):
        return self.payload_paths

    def get_json_validators(self):
        return self.json_validators


class InputNumber(Input):
    __slots__ = [
        "max_number",
        "min_number",
        "readonly",
        "step",
        "disabled",
        "max_number_path",
        "min_number_path",
        "disabled_path",
        "second_style",
    ]

    def get_base_component_dict(self):
        component = super().get_base_component_dict()
        component["type"] = "input_number"
        component["max_number"] = self.max_number
        component["min_number"] = self.min_number
        component["readonly"] = self.readonly
        component["step"] = self.step
        component["disabled"] = self.disabled
        component["max_number_path"] = self.max_number_path
        component["min_number_path"] = self.min_number_path
        component["disabled_path"] = self.disabled_path
        component["second_style"] = self.second_style
        return component

    def __init__(
        self,
        max_number=None,
        min_number=None,
        readonly=None,
        step=None,
        disabled=None,
        max_number_path=None,
        min_number_path=None,
        disabled_path=None,
        second_style=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.max_number = max_number
        self.min_number = min_number
        self.readonly = readonly or False
        self.step = step or 1
        self.disabled = disabled or False
        self.max_number_path = max_number_path or ""
        self.min_number_path = min_number_path or ""
        self.disabled_path = disabled_path or ""
        self.second_style = second_style is None and True or second_style


class InputWithSuggestions(Input):
    __slots__ = [
        "suggestions_path",
        "suggestions",
    ]

    def get_suggestions(self, suggestions_path, suggestions):
        """Only suggestions or suggestions_path should be specified, this function validates this condition"""
        validate = self.validate_suggestions(suggestions_path, suggestions)
        if validate:
            return suggestions_path, suggestions

    def validate_suggestions(self, suggestions_path, suggestions):
        if suggestions is not None and suggestions_path is not None:
            raise InvalidArguments("'suggestions' and 'suggestions_path' attribute cannot be used together")

        if suggestions is None and suggestions_path is None:
            raise InvalidArguments("Either 'suggestions' or 'suggestions_path' attribute must be used")

        if suggestions and type(suggestions) is not list and type(suggestions[0]) is not dict:
            raise InvalidArguments("If 'suggestions' is supplied, it must be a list of dicts")

        return True

    def __init__(
        self,
        suggestions_path=None,
        suggestions=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.suggestions_path, self.suggestions = self.get_suggestions(suggestions_path, suggestions)

    def get_base_component_dict(self):
        component = super().get_base_component_dict()
        component["type"] = "input_with_suggestions"
        if self.suggestions is not None:
            component["suggestions"] = self.suggestions
        else:
            component["suggestions_path"] = self.suggestions_path
        return component


class DateTime(Input):
    __slots__ = [
        "datetime_type",
        "open_to",
    ]

    def get_datetime_type(self, datetime_type):
        validate = self.validate_datetime(datetime_type)
        if validate:
            return datetime_type

    def validate_datetime(self, datetime_type):
        if datetime_type not in ["datetime", "time", "date"]:
            raise InvalidArguments(
                "'datetime_type' must be one of expected datetimes types: 'datetime', 'time' or 'date'."
            )
        return True

    def get_open_to(self, open_to):
        validate = self.validate_open_to(open_to)
        if validate:
            return open_to

    def validate_open_to(self, open_to):
        if open_to not in [None, "date", "year", "month", "hours", "minutes"]:
            raise InvalidArguments(
                "'open_to' must be one of expected values: 'date', 'year', 'month', 'hours' or 'minutes'."
            )
        return True

    def __init__(
        self, datetime_type="datetime", open_to=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.component_type = self.get_datetime_type(datetime_type)
        self.open_to = self.get_open_to(open_to)

    def get_base_component_dict(self):
        component = super().get_base_component_dict()
        if self.open_to:
            component["open_to"] = self.open_to
        return component


class Button(Component):
    __slots__ = [
        "action",
        "style",
        "value",
        "load_values",
        "destination_path",
        "show_confirmation",
        "disabling_validators",
    ]

    text = Translatable()

    def __init__(
        self,
        action,
        style,
        text,
        value=True,
        load_values=None,
        destination_path=None,
        show_confirmation=False,
        disabling_validators=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.action = action
        self.style = style
        self.text = text
        self.value = value
        self.destination_path = destination_path
        self.show_confirmation = show_confirmation
        self.load_values = load_values
        self.disabling_validators = disabling_validators or []

    def _get_default_identifier(self):
        return "_".join([self.action, "button"])

    def get_disabling_validators(self):
        return [validator.identifier for validator in self.disabling_validators]

    def get_base_component_dict(self):
        button = {
            "type": "button",
            "action": self.action,
            "style": self.style,
            "text": self.text,
        }

        if self.show_confirmation:
            button["show_confirmation"] = self.show_confirmation

        if self.destination_path:
            button.update({"value": self.value, "destination_path": self.destination_path})
        if self.load_values is not None:
            button["load_values"] = self.load_values

        disabling_validators = self.get_disabling_validators()
        if disabling_validators:
            button["disabled"] = disabling_validators

        return button

    def get_validators(self):
        yield from super().get_validators()
        if self.disabling_validators:
            yield from self.disabling_validators


class DisplayData(Component):
    """
    Produces a display component which can list data in two different formats depending on the display_type,
    this can be "list" or "details" and requires the following formats provided as data:
        - "list": will list all the values provided, "data" should point to a list of strings
        - "details": requires a list of "{'label': '...', 'value': '...'}", "data" should
                 point to such an object in the context
    """

    __slots__ = [
        "data",
        "display_type",
        "max_height"
    ]

    title = Translatable()
    subtitle = Translatable()

    def __init__(self, display_type, title, data, subtitle=None, max_height=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.data = data
        self.subtitle = subtitle
        self.display_type = display_type
        self.max_height = max_height

    def _get_default_identifier(self):
        return "_".join([self.display_type, self.title.lower().replace(" ", "_")])

    def _get_type(self):
        return self.display_type

    def get_base_component_dict(self):
        component = {
            "type": self._get_type(),
            "title": self.title,
            "data": self.data,
        }
        if self.subtitle:
            component.update(subtitle=self.subtitle)
        if self.max_height and self.display_type in ["list", "details"]:
            component.update(max_height=self.max_height)

        return component


class OptionList(DisplayData):
    """
    This component is a selectable analogue to the DisplayData component.
    Elements are displayed as in the "details" case of  DisplayData,
    and upon selection a defined value is added to the context.
    This requires data to be a list of 
        {
            'details': [
                    {'label': 'label1', 'value': 'value1'},
                    {'label': 'label2', 'value': 'value2'}
                ],
            'submitted_value': '...',
            'submitted_key': '...',
        }
        where,
        'details': a list whose elements are rendered as a label and
            value,
        'submitted_value': the value submitted upon selection of
        the option,
        'submitted_key': a value to submit is taken from the context
        attribute corresponding to this key.
        Note, 'submitted_value' and 'submitted_key' are mutually exclusive.

    grid can be set to True to change the display_type to "optionlist_grid"
    grid_min_item_width can be set to a pixel value to determine the minimum width of each
        item within the grid. The default is 250.
    """

    def __init__(self, display_type, title, data, subtitle=None, max_height=None, grid=False, grid_min_item_width=250, **kwargs):
        # Don't pass grid or grid_min_item_width down to DisplayData initialisation.
        super().__init__(display_type, title, data, subtitle=subtitle, max_height=max_height, **kwargs)
        self.grid = grid
        self.grid_min_item_width = grid_min_item_width

    def get_base_component_dict(self):
        component = super().get_base_component_dict()
        if self.grid:
            component["grid_min_item_width"] = self.grid_min_item_width
        return component

    def _get_type(self):
        return "optionlist_grid" if self.grid else "optionlist"


class Modal(Component):
    """
        A data structure to render a modal popup on the frontend, which itself
        can contain components.
    """
    __slots__ = [
        "title",
        "components",
        "trigger_conditions",
        "trigger"
    ]

    def __init__(self, title, components, trigger_conditions=None, trigger="onSubmit", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.components = components
        self.trigger_conditions = trigger_conditions or []
        self.trigger = self.validate_trigger(trigger)

    def validate_trigger(self, trigger):
        trigger_values = ["onLoad", "onBlur", "onSubmit"]
        if trigger in trigger_values:
            return trigger
        else:
            raise InvalidArguments(f"Trigger must be one of the following: {', '.join(trigger_values)}")
    def get_base_component_dict(self):
        return {
            "type": "modal",
            "title": self.title,
            "components": [[component.get_flow_component_dict() for component in row] for row in self.components],
            "trigger_conditions": [trigger_condition.identifier for trigger_condition in self.trigger_conditions],
            "trigger": self.trigger,
        }

    def get_components(self):
        yield from super().get_components()
        yield from self.components

    def get_validators(self):
        yield from super().get_validators()
        yield from self.trigger_conditions
        for row in self.components:
            for component in row:
                yield from component.get_validators()


class Checkbox(Component):
    """
    label: Label to show next to the checkbox
    destination_path: The JSON path key in which to store the value/value_path
    value: The value to be stored at the destination_path
    value_path: A JSON path lookup (to provide a list of values, put them into the context and then use the lookup),
    """

    __slots__ = [
        "label",
        "destination_path",
        "value_path",
        "value",
    ]

    def get_value(self, value_path, value):
        """Only value or value_path should be specified, this function validates this condition"""
        validate = self.validate_value(value_path, value)
        if validate:
            return value_path, value

    def validate_value(self, value_path, value):
        if value is not None and value_path is not None:
            raise InvalidArguments("'value' and 'value_path' attribute cannot be used together")

        if value is None and value_path is None:
            raise InvalidArguments("Either 'value' or 'value_path' attribute must be used")

        if value and type(value) is not str and type(value) is not bool:
            raise InvalidArguments("If 'value' is supplied, it must be a string or boolean")

        return True

    def __init__(self, label, destination_path=None, value=None, value_path=None, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.value_path, self.value = self.get_value(value_path, value)
        self.destination_path = destination_path

    def get_base_component_dict(self):
        base_component_dict = {
            "type": "checkbox",
            "label": self.label,
        }
        if self.destination_path is not None:
            base_component_dict["destination_path"] = self.destination_path
        if self.value is not None:
            base_component_dict["value"] = self.value
        else:
            base_component_dict["value_path"] = self.value_path
        return base_component_dict

    def _checkboxlist_dict(self):
        """Produces the reduced data from a checkbox that would be used in a checkboxlist"""
        return {
            "label": self.label,
            "value": self.value
        }


class CheckboxList(Component):
    """
    title: Title to show for the checkbox list
    destination_path: JSON path to store the outcome of the checkbox list
    data: A hardcoded list of checkbox like signatures
    data_path: A JSON path pointing to a list of checkbox like signatures
    (without destination path, as this comes from the checkbox list itself):
        [
            '{
                "label": "Label of checkbox 1",
                "value": "Some value to put at destination_path",
            }',
            '{
                "label": "Label of checkbox 2",
                "value": "Some value to put at destination_path",
            }'
        ]
        for each checkbox to be displayed
        Note that if value is the same between data entries, each checkbox with that value will be set
        as ticked if any matching entry is set. This owes to the values put into the destination path
        defining the relative state of the checkbox itself.
    """
    # TODO: Potentially we could have destination_path for each checkbox, to create a hierarchical structure at the
    # checkbox list destination_path, but no use case currently reveals itself.

    __slots__ = [
        "destination_path",
        "data_path",
        "data",
    ]

    title = Translatable()

    def get_data(self, data_path, data):
        """Only data or data_path should be specified, this function validates this condition"""
        validate = self.validate_data(data_path, data)
        if validate:
            return data_path, data

    def validate_data(self, data_path, data):
        if data is not None and data_path is not None:
            raise InvalidArguments("'data' and 'data_path' attribute cannot be used together")

        if data is None and data_path is None:
            raise InvalidArguments("Either 'data' or 'data_path' attribute must be used")

        if data and type(data) is not list and type(data[0]) is not dict:
            raise InvalidArguments("If 'data' is supplied, it must be a list of dictionaries")

        return True

    def __init__(self, title, destination_path, data_path=None, data=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.destination_path = destination_path
        self.data_path, self.data = self.get_data(data_path, data)

    def get_base_component_dict(self):
        base_component_dict = {
            "type": "checkbox_list",
            "title": self.title,
            "destination_path": self.destination_path,
        }
        if self.data_path is not None:
            base_component_dict["data_path"] = self.data_path
        else:
            base_component_dict["data"] = self.data
        return base_component_dict


class MessageBox(Component):
    __slots__ = [
        "type",
        "size",
    ]

    template = Translatable()

    def __init__(self, template, message_type, size=None, **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.type = message_type
        self.size = size

    def get_message(self):
        return {
            "template": self.template,
            "type": self.type,
        }

    def get_base_component_dict(self):
        return {
            "type": "message_box",
            "message": self.get_message(),
            "size": self.size,
        }


class Toggle(Component):
    __slots__ = [
        "style",
        "preconditions",
        "value",
        "destination_path",
    ]

    label = Translatable()

    def __init__(self, style, label, value=None, destination_path=None, **kwargs):
        super().__init__(**kwargs)
        self.style = style
        self.label = label
        self.value = value
        self.destination_path = destination_path

    def get_base_component_dict(self):
        return {
            "type": "toggle",
            "style": self.style,
            "label": self.label,
            "value": self.value,
            "destination_path": self.destination_path,
        }


class Selection(Component):
    __slots__ = [
        "style",
        "validators",
        "is_required",
        "destination_path",
        "options_key",
        "options_values",
        "default_value",
    ]

    label = Translatable()

    def get_options(self, options_key, options_values):
        """Only key or values should be specified, this function validates this condition"""
        validate = self.validate_options(options_key, options_values)
        if validate:
            return options_key, options_values

    def validate_options(self, options_key, options_values):
        if options_key is not None and options_values is not None:
            raise InvalidArguments("'options_key' and 'options_values' attribute cannot be used together")

        if options_key is None and options_values is None:
            raise InvalidArguments("Either 'options_key' or 'options_values' attribute must be used")

        if options_values and type(options_values) is not list and type(options_values[0]) is not dict:
            raise InvalidArguments("If 'options_values' is supplied, it must be a list of dictionaries")

        return True

    def __init__(
        self, label, style="default", is_required=False, validators=None, value=None, destination_path=None, options_key=None, options_values=None, default_value=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.style = style
        self.label = label
        self.is_required = is_required
        self.validators = validators or []
        self.options_key, self.options_values = self.get_options(options_key, options_values)
        self.destination_path = destination_path
        self.default_value = default_value

    def get_base_component_dict(self):
        return {
            "type": "select",
            "style": self.style,
            "label": self.label,
            "is_required": self.is_required,
            "validator": [validator.identifier for validator in self.validators],
            "options_values": self.options_values,
            "options_key": self.options_key,
            "destination_path": self.destination_path,
            "default_value": self.default_value,
        }

    def get_validators(self):
        yield from super().get_validators()
        yield from self.validators


class Image(Component):
    __slots__ = [
        "url",
        "max_Height",
        "max_Width",
    ]

    def __init__(self, url, max_Height=None, max_Width=None, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.max_Height = max_Height
        self.max_Width = max_Width

    def get_base_component_dict(self):
        return {
            "type": "image",
            "url": self.url,
            "max_Height": self.max_Height,
            "max_Width": self.max_Width,
        }


class Repeat(Component):
    """
    A meta component which can be used to repeat the same field.

    Args:
        times_to_repeat: Int
            number of times the field should be repeated
        times_to_repeat_path: Str:
            a jsonpath to look up how many times the field should be repeated
        components: List[List[Component]]
            a list of rows of components in the group
        destination_path: Str:
            a jsonpath to put the list of results into (if components have a destination_path)
    """

    __slots__ = [
        "times_to_repeat",
        "times_to_repeat_path",
        "components",
        "destination_path",
    ]

    def __init__(self, components, times_to_repeat=None, times_to_repeat_path=None, destination_path=None, **kwargs):
        self._validate_args(times_to_repeat, times_to_repeat_path)
        super().__init__(**kwargs)
        self.components = components
        self.times_to_repeat = times_to_repeat
        self.times_to_repeat_path = times_to_repeat_path
        self.destination_path = destination_path

    @staticmethod
    def _validate_args(times_to_repeat, times_to_repeat_path):
        if times_to_repeat is not None and times_to_repeat_path is not None:
            raise InvalidArguments("'times_to_repeat' and 'times_to_repeat_path' attribute cannot be used together")

        if times_to_repeat is None and times_to_repeat_path is None:
            raise InvalidArguments("Either 'times_to_repeat' or 'times_to_repeat_path' attribute must be used")

    def get_base_component_dict(self):
        # As we expect rows of components, keep the structure but parse out the component dicts
        components_dicts = [
            [
                component.get_flow_component_dict() for component in row
            ] for row in self.components
        ]
        component = {
            "type": "repeated_field",
            "components": components_dicts,
            "destination_path": self.destination_path,
        }

        if self.times_to_repeat is not None:
            component["times_to_repeat"] = self.times_to_repeat
        else:
            component["times_to_repeat_path"] = self.times_to_repeat_path

        return component

    def get_components(self):
        yield from super().get_components()
        yield from self.components

    def get_validators(self):
        yield from super().get_validators()
        for component in self.components:
            yield from component.get_validators()

class Table(Component):
    """
    A meta component which can be used to put other components into a table.

    The idea with this component is to have data in context
    which controls the data which is held in the table.
    For instance, given a table where we want to display the following:

    | Header 1  | Header 2  | Header 3  |
    |-----------|-----------|-----------|
    | Value 1   | Value 2   | Value 3   |
    | Value 100 | Value 200 | Value 300 |

    we would have a data structure in context like so:
        {"table_data": [
            {
                "h1": "Value 1",
                "h2": "Value 2",
                "h3": "Value 3",
            },
            {
                "h1": "Value 100",
                "h2": "Value 200",
                "h3": "Value 300",
            },
        ],
        "table_headers": ["Header 1", "Header 2", "Header 3"],
        }

    The components passed to table_components determine the component used for each column in the table.
    The ordering is important as it will determine which column the component is used for.
    Additional keys may exist in each list item in the table_data_path, but missing keys will not be supported.

        table_component = core_components.Table(
            identifier="test_table_component",
            table_data_path="$.table_data",
            table_headers_path="$.table_headers",
            table_components=[textbox_component1, textbox_component2, input_component],
            table_container_width=1000,
        )

    The components will look up their defaults, or value_paths as if table_data_path is the root of their lookup.
    The components setters (i.e destination_path) will treat table_data_path as the root of their lookup.

    This means, with the above example - if we wish to update "h3" values inline in the "table_data" key on submit,
    then the component should be defined as such:

        input_component = core_components.Input(
            identifier="test_component",
            label="Some Label",
            destination_path="$.h3",
            default_value="$.h3",
        )

    If we wished to preserve the original context keys values (say, if we needed to diff the original vs the new)
    then the destination_path should be set to a new key, in which case, it will be added to the object inside table_data.

    NOTE: Static table data is not supported, but we see no real need for this.
          If we wish to display some static data, then we can add it to context and display that.
          Supporting it would complicate the component too much.

    NOTE: Multiple components per cell is not supported.
    NOTE: Multiple components per column is not supported.

    Components are sent as a list of lists solely to be consistent
    with other places handling components in rows.

    Args:
        table_components: List[Component]
            a list of components
        table_data_path: Str:
            a jsonpath to look up table data.
        table_headers_path: Str:
            a jsonpath to look up table headers.
        table_container_width : Integer:
            Number of pixels the table wrapper will be, if specified and table is wider than the container
            Horizontal scrolling will be automatically shown on front end
    """

    __slots__ = [
        "table_components",
        "table_data_path",
        "table_headers_path",
        "table_container_width",
    ]

    def __init__(
            self,
            table_components,
            table_data_path,
            table_headers_path,
            table_container_width=None,
            **kwargs,
            ):
        super().__init__(**kwargs)
        self.table_components = table_components
        self.table_data_path = table_data_path
        self.table_headers_path = table_headers_path
        self.table_container_width = table_container_width

    def get_base_component_dict(self):
        components_dicts = [
            component.get_flow_component_dict() for component in self.table_components
        ]

        component = {
            "type": "table",
            "components": [components_dicts],
            "table_data_path": self.table_data_path,
            "table_headers_path": self.table_headers_path,
        }
        if self.table_container_width is not None:
            component["table_container_width"] = self.table_container_width
        return component

    def get_components(self):
        yield from super().get_components()
        yield from self.table_components

    def get_validators(self):
        yield from super().get_validators()
        for component in self.table_components:
            yield from component.get_validators()


class Container(Component):
    """A container with components and optional styling."""

    __slots__ = [
        "components",
        "width",
        "style",
    ]

    def __init__(self, components, width=12, style="default", **kwargs):
        super().__init__(**kwargs)
        self.components = self.validate_components(components)
        self.width = validate_size(width)
        self.style = validate_style(style, ("transparent",))

    def validate_components(self, components):
        """Ensure no Container or ContainerRow components are added to Containers"""
        invalid_component_types = (Container, ContainerRow, Modal)
        if any(isinstance(component, invalid_component_types) for component in components):
            raise InvalidArguments(
                "Container components cannot include Modals, Container Rows or other Containers."
            )
        return components

    def get_base_component_dict(self):
        return {
            "type": "container",
            "width": self.width,
            "style": self.style,
            "components": [
                [component.get_flow_component_dict() for component in row]
                for row in self.components
            ],
        }

    def get_components(self):
        yield from super().get_components()
        yield from self.components


class ContainerRow(Component):
    """A row of containers, where the height of all containers in the row is set."""

    __slots__ = [
        "components",
        "height",
    ]

    def __init__(self, components, height=12, **kwargs):
        super().__init__(**kwargs)
        self.components = self.validate_components(components)
        self.height = validate_size(height)

    def validate_components(self, components):
        """Ensure only Container components are added to ContainerRows"""
        if any(not isinstance(component, Container) for component in components):
            raise InvalidArguments("Only Container components can be added to Container Rows.")
        return components

    def get_base_component_dict(self):
        return {
            "type": "container_row",
            "height": self.height,
            "components": [
                [component.get_flow_component_dict() for component in row]
                for row in self.components
            ],
        }

    def get_components(self):
        """Include components of child components if applicable (e.g. child container components)"""
        yield from super().get_components()
        yield from self.components

        for component in self.components:
            yield from component.get_components()

    def get_validators(self):
        """Include validators of child components if applicable (e.g. child container validators)"""
        yield from super().get_validators()
        for container in self.components:
            for container_component_list in container.components:
                if not isinstance(container_component_list, list):
                    container_component_list = [container_component_list]
                for container_component in container_component_list:
                    yield from container_component.get_validators()


class Spacer(Component):
    """A component used for spacing."""

    __slots__ = ["amount"]

    def __init__(self, amount=1, **kwargs):
        super().__init__(**kwargs)
        self.amount = self.validate_amount(amount)

    def validate_amount(self, amount):
        if amount < 1:
            raise InvalidArguments("Amount cannot be below 1.")
        return amount

    def get_base_component_dict(self):
        return {
            "type": "spacer",
            "amount": self.amount,
        }


class InstructionBox(Component):
    """A box containing a message along with optional directional arrow."""

    __slots__ = [
        "message",
        "direction",
        "style",
    ]

    def __init__(self, message, direction="none", style="default", **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.direction = self.validate_direction(direction)
        self.style = validate_style(style)

    def validate_direction(self, direction):
        supported_directions = ("none", "left", "right", "up", "down")

        if direction not in supported_directions:
            raise InvalidArguments(
                f"Invalid direction '{direction}' specified."
                " If set, direction must be one of the following: "
                f"{', '.join(supported_directions)}"
            )
        return direction

    def get_base_component_dict(self):
        return {
            "type": "instruction_box",
            "message": self.message,
            "direction": self.direction,
            "style": self.style,
        }
