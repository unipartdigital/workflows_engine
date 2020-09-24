from itertools import chain
from .translate import Translatable

__all__ = (
    "Component",
    "Input",
    "Button",
    "DisplayData",
    "Checkbox",
    "MessageBox",
    "Toggle",
    "Image",
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
                "target": self.target,
                "validator": [v.identifier for v in self.validators],
            }
        )

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
    Allowed "display_type" are currently "list" and "details"
    - "list": will list all the values so "data" will have to produces a list of strings
    - "details": requires a list of "{'label': '...', 'value': '...'}" so "data" will have
                 point to such an object in the context
    """

    __slots__ = [
        "display_type",
        "data",
    ]

    title = Translatable()
    subtitle = Translatable()

    def __init__(self, display_type, title, data, subtitle=None, **kwargs):
        super().__init__(**kwargs)
        self.display_type = display_type
        self.title = title
        self.data = data
        self.subtitle = subtitle

    def _get_default_identifier(self):
        return "_".join([self.display_type, self.title.lower().replace(" ", "_")])

    def get_base_component_dict(self):
        component = {
            "type": self.display_type,
            "title": self.title,
            "data": self.data,
        }
        if self.subtitle:
            component.update(subtitle=self.subtitle)

        return component


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
