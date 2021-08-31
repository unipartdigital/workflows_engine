import pytest
from workflows_engine.core.translate import Translatable
from workflows_engine.core.components import *


@pytest.fixture
def translate():
    func = lambda x: "{} has been translated!".format(x)

    old_translator = Translatable._translator
    Translatable._translator = staticmethod(func)

    yield func

    Translatable._translator = old_translator


def test_button(translate):
    button_text = "Button"
    button = Button(text=button_text, action="submit", style="primary")
    assert button.text == translate(button_text), "Button text not translated"
