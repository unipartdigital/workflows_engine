**********
Primitives
**********

.. contents::
    :depth: 3

jsonpath
########

jsonpaths are used extensively throughout workflows for object lookups. Full documentation can be found `here <https://goessner.net/articles/JsonPath/>`_.

A quick primer for the sake of expediency: a jsonpath is a represention for a lookup in a structured object. For instance, given the object::

    {"outer": {"inner": {"value": "Hello"}}}

the lookup ``$.outer.inner.value`` returns ``"Hello"``. Jsonpath allows for filtering, this is useful for defining many things within workflows so we strongly suggest that you take a look at the `full docs <https://goessner.net/articles/JsonPath/>`_.

Schema
######

Json schemas forming the valid prototypical structures for workflow json.

.. _task_objects:

Tasks
#####

Tasks are actions to be performed by the client and take the form of specific objects types identified by the ``type`` keyword.

.. important::

    * All task names should be unique within a flow (remember, :ref:`subflows <glossary>` are themselves a flow).
    * Flow task names should be unique within a workflow.

Schema
******

.. jsonschema:: ../../src/core/schema/tasks/task.json


.. _flow_task:

Flow
****

Flow tasks are the base task for a workflow, they act as context scopes containing tasks to be executed within that scope.

Returning values from the context scope to the flow above is done by setting the ``result`` which is built from the `result_keys`. `result_keys` are a list of objects which of the form  ``{"key": "$.source", "result_key": "$.destination"}`` or ``{"result": "x", "result_key": "$.destination"}``, this form allows for renaming values and the restructuring of data to build the ``result`` object.

.. note:: The ``result`` object should copied then updated by parsing the ``result_keys`` this allows meta-data/debug-info to be set by the provider of the workflow.

The `result` is either placed at ``destination_path`` or if ``destination_path = False`` the ``result`` is merged directly into the parent context, that is the context of the flow on which this is a task.


.. note:: ``destination_path = False`` means merge result with the above context, whereas ``destination_path = None`` (the default value) means no destination path is set, this may be used for a flow or loop which does not define a ``result`` i.e. has no result keyword

.. warning:: Subflows (a flow within another flow) can see the context of the flow above them. However, only state which is modified via the result objects will persist after leaving the flow.


A flow can be as simple as a list of tasks to be performed, a :ref:`while_loop_task` or a :ref:`for_loop_task`. The looping tasks build a list of `result` objects if one is defined.

.. todo:: Having ``destination_path = False`` for loops should raise an error as this undefined behavior.


.. _while_loop_task:

While loop
----------

Repeat the flow tasks until a condition fails. The condition is a set of validators, when any of these validators fail the loop will exit at the end of its current iteration, the loop is in effect broken and the result is inserted into the context above. In order to leave the loop partway through an iteration an :ref:`event <event_task>` with an action of type break can be used

.. _for_loop_task:

For loop
--------

Repeat the flow tasks for a given list of objects. At each iteration the object at the current index of the list is merged into the context, this flows tasks are then evaluated. Once the list of objects has been exhausted, the loop will exit at the end of its current iteration and the result will be inserted into the context above. For example assuming the ``iterable_path="$.for_loop_list"`` and the context begins as:

.. code-block::

    {
        "not_affected": "MC Hammer",
        "value": "a",
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }

then in the 1st Iteration the context will look like:

.. code-block::

    {
        "not_affected": "MC Hammer",
        "value": 1,
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }

and during the 2nd Iteration:

.. code-block::

    {
        "not_effected": "MC Hammer",
        "value": 2,
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }

then after, if no ``result`` was set, then the context returns to its former state:

.. code-block::

    {
        "not_effected": "MC Hammer",
        "value": "a",
        "for_loop_list": [{"value": 1}, {"value": 2}]
    }


There is no requirement for each iteration object to have the same type(structure). Although you have to deal with the consequences if you choose for them to differ.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/flow.json


.. _screen_task:

Screen
******

Screen tasks are the sole task type used to display components to the user (excluding status messages which can be presented by other tasks, although they will be shown on the next screen task presented to the user).

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/screen.json


.. _jsonrpc_task:

JSON RPC
********

Are remote procedure calls. ``payload_paths`` and ``payload`` are analogous to ``result_keys`` and ``result`` in the :ref:`flow task <flow_task>` in that the payload sent to endpoint defined by ``url`` is constructed by copying the ``payload`` object and ``payload_paths`` are used to update the payload sent. The expectation is that the endpoint will respond with json stored in the ``response_path``.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/jsonrpc.json


.. _update_task:

Update
******

Update tasks are used to change values in the context. An update task itself may contain multiple distinct updates to perform, these essentially act as subtasks. The subtasks come in three major forms, dictated by the keywords used in their invocation as shown below:

1. updating the context with a raw value (keyword - "result"):

.. code-block::

    {"result": "x", "result_key": "$.destination"}

2. renaming a context value (keyword - "key"):

.. code-block::

    {"key": "x", "result_key": "$.destination"}

3. creating a new value using a string template (key word - "template"):

.. code-block::

    {"template": "{$.value}{$.another}", "result_key": "$.destination"}

There are also extra flags ``append`` and ``extend``, which are mutually exclusive, they act by modifying the above major cases, updating a destination which must be a list. Extend and append are used with their conventional meanings i.e. extend will concatenate lists and append will add a value to the end of a list. As such the result for extend needs to be a list and the result for append needs to be a value.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/update.json


.. _redirect_task:


Redirect
********

Redirect tasks switch the workflow to that found at the url provided.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/redirect.json


.. _condition_task:

Condition
*********

Selects a task to switch to based on whether a condition is true or false. This requires the flow and name of the task we wish to select to be specified, using a :ref:`TaskTarget container<target_task_container>`.

.. warning:: Jumps are only allowed to the same flow or ancestors of the flow.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/condition.json


.. _set_domain_task:

Domain param
************

Set a value in the local store which is added to the url of :ref:`JSONRPC <jsonrpc_task>` calls.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/set_domain_param.json


.. _clear_domain_task:

Clear domain params
*******************

Clear values set using :ref:`Domain Param <set_domain_task>`.

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/clear_domain_params.json




.. _event_task:

Event
*****

An event task can be used to break loops ...

.. todo:: Add payload_paths

Schema
------

.. jsonschema:: ../../src/core/schema/tasks/event.json


.. _validator_objects:

Validators
##########

Check the truth-y-ness of a condition, this is used in a variety of ways throughout workflows:

* checking field inputs are valid
* conditions in a :ref:`condition task <condition_task>` or :ref:`while loop <while_loop_task>`
* all :ref:`tasks <task_objects>` and :ref:`components <component_objects>` have optional preconditions, the evaluation of which decide if a task is run or a component is displayed

When defining a validator there must be a function to be evaluated in the client, this is represented by the string in the ``type`` attribute. For field validation ``value_key`` is ignored. For others ``validator_value`` is a raw comparison value passed to the validator, whereas ``validator_key`` is a jsonpath used to lookup the comparison value in the context. The ``valid_when`` flag allows you to switch the truth-y-ness of the comparison, i.e. whether it's valid when true or when false.

Schema
******

.. jsonschema:: ../../src/core/schema/validator.json


.. _component_objects:

Components
##########

Components are screen elements to be interacted with and viewed by the user. Components are split into two parts: the base component and the component look up. The base component is extracted into :ref:`components key <basic_structure>` in the workflow, this is then used by the component look up. As such, components with the same name are required to have the same values, otherwise an error is thrown. As with task components, these have preconditions which dictate if they are shown.

Schema
******

.. jsonschema:: ../../src/core/schema/components/component.json


.. _container_objects:

Containers
##########

Containers are used to specify the format and enforce the validity of commonly used structures. The current types are `Message`, `TaskTarget` and `Populate`.

.. _target_task_container:

TaskTarget
**********

Used to specify a task via its name and that of the flow it is in.

.. _populate_container:

Populate
********

Specifies if and how a field should be populated based on a condition being met.

.. _message_container:

Message
*******

Defines a message in terms of a template and type (e.g. "success" or "error"). It is not currently used when the type of the message is predefined.