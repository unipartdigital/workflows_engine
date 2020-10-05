***************
Basic Structure
***************

.. _basic_structure:

The basic structure of workflows is a JSON object with five keys (``validators``, ``components``, ``flow``, ``hash`` and ``context``).


The ``components`` key is a list of :ref:`components <component_objects>` which are visual elements.

The ``validator`` key contains a list of :ref:`validator <validator_objects>` which are then reference within :ref:`components <component_objects>` and pre/conditions.

The ``flow`` key contains the base task for the workflow (think the ``main`` function in a Java program).

The ``hash`` key is a hash for representing the workflow (this is intended for use by the client to check for changes to the workflow - no need to grab the definition from the server if you already have it)

The ``context`` key contains the initial values used by the :ref:`context <glossary>` as defined in the index.

.. jsonschema:: ../../src/core/schema/workflow.json
