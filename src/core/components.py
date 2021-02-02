from itertools import chain
from .translate import Translatable
from ..exceptions import InvalidArguments


__all__ = (
    "Component",
    "Input",
    "Button",
    "DisplayData",
    "Checkbox",
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
            component["target"]: self.target
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
        return component

    def get_validators(self):
        yield from super().get_validators()
        yield from self.validators
        if self.populate:
            self.populate.get_validators()


class DateTime(Input):
    __slots__ = [
        "datetime_type",
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

    def __init__(
        self, datetime_type="datetime", **kwargs
    ):
        super().__init__(**kwargs)
        self.component_type = self.get_datetime_type(datetime_type)


class Button(Component):
    __slots__ = [
        "action",
        "style",
        "value",
        "load_values",
        "destination_path",
        "show_confirmation",
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

    def _get_default_identifier(self):
        return "_".join([self.action, "button"])

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

        return button


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
        "display_type"
    ]

    title = Translatable()
    subtitle = Translatable()

    def __init__(self, display_type, title, data, subtitle=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.data = data
        self.subtitle = subtitle
        self.display_type = display_type

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


class Checkbox(Component):
    """
    - "data": requires a list of "{'id': 1, 'label': '...', 'value': '...'}"
    """

    __slots__ = [
        "data",
        "target",
    ]

    title = Translatable()

    def __init__(self, title, data, target, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.data = data
        self.target = target

    def _get_default_identifier(self):
        return "_".join([self.title.lower().replace(" ", "_")])

    def get_base_component_dict(self):
        return {
            "type": "checkbox",
            "title": self.title,
            "data": self.data,
            "target": self.target,
        }


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
        quantity: Int
            number of times the field should be repeated
        quantity_path: Str:
            a jsonpath to look up how many times the field should be repeated
        validators: List[Validators]
            the list of names of the validators to act on the result of the all the repeat fields
        components: List[Component]
            a list of components in the group
    """

    __slots__ = [
        "quantity",
        "quantity_path",
        "components",
        "validators",
    ]

    def __init__(self, components, quantity=None, quantity_path=None, validators=None, **kwargs):
        self._validate_args(quantity, quantity_path)
        super().__init__(**kwargs)
        self.components = components
        self.quantity = quantity
        self.quantity_path = quantity_path
        self.validators = validators or []

    @staticmethod
    def _validate_args(quantity, quantity_path):
        if quantity is not None and quantity_path is not None:
            raise InvalidArguments("'quantity' and 'quantity_path' attribute cannot be used together")

        if quantity is None and quantity_path is None:
            raise InvalidArguments("Either 'quantity' or 'quantity_path' attribute must be used")

    def get_base_component_dict(self):
        component = {
            "type": "repeated_field",
            "components": [c.get_flow_component_dict() for c in self.components],
            "validators": [v.identifier for v in self.validators],
        }

        if self.quantity is not None:
            component["quantity"] = self.quantity
        else:
            component["quantity_path"] = self.quantity_path

        return component

    def get_components(self):
        yield from super().get_components()
        yield from self.components
