**********
Primitives
**********

.. contents::

jsonpath
########

jsonpaths are used extensively throughout workflows for looking up objects. The full docs can be found `here <https://goessner.net/articles/JsonPath/>`_.

A quick rundown for the sake to expediency is that a jsonpath is a way of representing a look up in a structured object for instance given the object::

    {"outer": {"inner": {"value": "Hello"}}}

the look up of ``$.outer.inner.value`` would return ``"Hello"``. Json path allows for filtering which will be useful for defining many things within workflows so we suggest that you the `full docs <https://goessner.net/articles/JsonPath/>`_.

.. _task_objects:

Tasks
#####

Tasks are actions, to be preformed by the client and take the form of specific objects types which is identified by the ``type`` keyword.

.. important::

    * All task names should be unique within a flow.
    * Flow task names should be unique within a workflow.

.. Schema
.. ******
.. .. jsonschema:: ../../src/core/schema/tasks/task.json


.. _flow_task:

Flow
****

Flow task are the base task for a workflow and act as context scopes which contain tasks to be executed within that scope.

Returning values from the context scope to the flow above is done by setting the ``result`` which is built from the `result_keys`. `result_keys` should be a list of objects which have the form of  ``{"key": "$.source", "result_key": "$.destination" }`` or ``{"result": "x", "result_key": "$.destination" }``, this form allows for renaming values and even the restructuring of data to build the ``result`` object.

.. note:: The ``result`` object should copied then updated by parsing the ``result_keys`` this allows meta-data/debug-info to be set by the provider of the workflow.

The `result` is either placed at ``destination_path`` or if ``destination_path = False`` the ``result`` is merged directly into the context above.


.. note:: ``destination_path = False`` means merge result with the above context where as ``destination_path = None`` (the default value) means no destination path is set, this maybe used for a flow or loop with no ``result``

.. warning:: Subflows (a flow within another flow) and see the context of the flow above it. However only state which is modified via the result objects will persist after leaving the flow.


A flow can be just as list of tasks to be performed, a :ref:`while_loop_task` or a :ref:`for_loop_task`. Looping tasks build a list of `result` objects if one is defined.

.. todo:: Having ``destination_path = False`` for loops should raise an error as this undefined behavior.


.. _while_loop_task:

While loop
----------

Repeat the flow tasks until a condition fails, the condition is a set of validators once one of these validators fails the loop is broken and the result is inserted into the context above.

.. _for_loop_task:

For loop
--------

Repeat the flow tasks for a given list of objects. Each iteration the object at that index of the list is merged into the context and then the tasks are evaluated. Once the list of objects has been exhausted the loop will break and the result will be inserted into the context above.


.. code-block::

    context = {
        "not_effected": "MC Hammer",
        "value": "a",
        "for_loop_list": [{"value": 1}, {"value": 2},]
    }


For example assuming the ``iterable_path="$.for_loop_list"`` and the context is before:

.. code-block::

    {
        "not_effected": "MC Hammer",
        "value": "a",
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }

then in the 1st Iteration the context will look like:

.. code-block::

    {
        "not_effected": "MC Hammer",
        "value": 1
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }

during the 2nd Iteration:

.. code-block::

    {
        "not_effected": "MC Hammer",
        "value": 2,
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }

then after if no ``result`` was set then the context returns to as it was before:

.. code-block::

    {
        "not_effected": "MC Hammer",
        "value": "a",
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }


There is no requirement for each iteration object to have the same type(structure). Although you have to deal with the consequences if you choose for them not to be.



Schema
------

.. jsonschema:: ../../src/core/schema/tasks/flow.json


.. _screen_task:

Screen
******

Screens are the only task type which display components to the screen (excluding status messages which can be presented by other tasks although they will be shown on the next screen task presented to the user).

.. Schema
.. ------

.. jsonschema:: ../../src/core/schema/tasks/screen.json


.. _jsonrpc_task:

JSON RPC
********

Are remote procedure calls.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/tasks/jsonrpc.json


.. _update_task:

Update
******

Change values in the context.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/tasks/update.json

.. _redirect_task:


Redirect
********

Change workflow to the one specified by the url.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/tasks/redirect.json


.. _condition_task:

Condition
*********

Selects (jumps to) a task to switch to based on if a condition is true or false.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/tasks/condition.json


.. _set_domain_task:

Domain param
************

Set a value which is added to url of :ref:`JSONRPC <jsonrpc_task>` calls.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/tasks/set_domain_param.json


.. _clear_domain_task:

Clear domain params
*******************

Clear values set using :ref:`Domain Param <set_domain_task>`.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/tasks/clear_domain_params.json


.. _validator_objects:

Validators
##########

Check the truth-y-ness of a condition, this is used in a verity of ways through out workflows:

* checking field inputs are acceptable
* conditions in a :ref:`condition task <condition_task>` or :ref:`while loop <while_loop_task>`
* all :ref:`tasks <task_objects>` and :ref:`components <component_objects>` have optional preconditions which decide if a task is run or a component is displayed

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/validator.json


.. _component_objects:

Components
##########

Components are screen elements to be displayed to and interacted by the user. Components are split into two parts.
The base component and the component look up. The base component is extracted into :ref:`components key <basic_structure>` in the workflow which is then used by the component look up, because of this components with the same name are required to have the same values, otherwise an error is thrown.

.. Schema
.. ------

.. .. jsonschema:: ../../src/core/schema/components/component.json
