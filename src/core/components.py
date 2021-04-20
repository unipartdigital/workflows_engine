from itertools import chain
from .translate import Translatable
from ..exceptions import InvalidArguments


__all__ = (
    "Component",
    "Input",
    "Button",
    "DisplayData",
    "Checkbox",
    "CheckboxList",
    "MessageBox",
    "Toggle",
    "Image",
    "Repeat",
)


class Component:
    __slots__ = [
        "_identifier",
        "destination_path",
        "flow_attrs",
        "update_context",
        "preconditions",
        "__weakref__",
    ]

    def __init__(
        self,
        identifier=None,
        destination_path=None,
        flow_attrs=None,
        update_context=None,
        preconditions=None,
    ):
        self._identifier = identifier
        self.destination_path = destination_path
        self.flow_attrs = flow_attrs or {}
        self.update_context = update_context or []
        self.preconditions = preconditions or []

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

    def get_components(self):
        yield self


class Textbox(Component):
    __slots__ = [
        "content",
    ]

    def __init__(self, content=None, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def get_base_component_dict(self):
        return {
            "type": "textbox",
            "content": self.content
        }


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
        "default_value"
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
        return component

    def get_validators(self):
        yield from super().get_validators()
        yield from self.validators
        if self.populate:
            self.populate.get_validators()


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
    """

    def _get_type(self):
        return "optionlist"


class Modal(Component):
    """
        A data structure to render a modal popup on the frontend, which itself
        can contain components.
    """
    __slots__ = [
        "title",
        "components",
        "trigger_conditions",
    ]

    def __init__(self, title, components, trigger_conditions=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.components = components
        self.trigger_conditions = trigger_conditions or []

    def get_base_component_dict(self):
        return {
            "type": "modal",
            "title": self.title,
            "components": [[component.get_flow_component_dict() for component in row] for row in self.components],
            "trigger_conditions": [trigger_condition.identifier for trigger_condition in self.trigger_conditions],
        }

    def get_components(self):
        yield from super().get_components()
        yield from self.components

    def get_validators(self):
        yield from super().get_validators()
        yield from self.trigger_conditions


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
        self, label, style="default", is_required=False, validators=None, value=None, destination_path=None, options_key=None, options_values=None, **kwargs
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


class Image(Component):
    __slots__ = [
        "url",
    ]

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def get_base_component_dict(self):
        return {
            "type": "image",
            "url": self.url,
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
