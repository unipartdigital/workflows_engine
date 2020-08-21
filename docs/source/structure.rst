***************
Basic Structure
***************

The basic structure of workflows is an JSON object with five keys (``validators``, ``components``, ``flow``, ``hash`` and ``context``).


The ``components`` key is a list of :ref:`components <component_objects>` which are visual elements.

The ``validator`` key contains a list of :ref:`validator <validator_objects>` which are then reference within :ref:`components <component_objects>` and pre/conditions.

The ``flow`` key contains the base task for the workflow (think the ``main`` function in a Java program).


.. code-block:: json

    {
        "validators": [ { "#": "validators objects" } ],
        "components": [ { "#": "components objects" } ],
        "flow": { "#": "Base flow" },
        "hash": "... hash of stringified workflow excluding hash and context keys ...",
        "context": { "#": "Initial values of the context" }
    }
