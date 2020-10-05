****************
Tao of workflows
****************

.. contents::

This section is to explain the principle ideas of workflows.
**Workflows are a JSON object encoding actions to be taken by the client.**
With the focus being on the JSON object produced, the library and client could be
replaced independently as required by the use case. This is motivated by the idea of being technologically
independent, that is to say that a client or server which obeys the interfaces and patterns explained in these docs
will function irrespective of technology used to implement them; they are technologically agnostic.
The server should not care about the client, and in turn the client should not care about the
server (barring of course, the interfaces).

Workflows features should be written with some key principles in mind:

* **The job of the client is to display information.** Processing and domain logic should be handled by the backend (note: handled might mean defining a task in the workflow).

* **Ease of execution of the JSON object should be top priority.** This means where possible complexity should be in the library producing the workflow, rather than in the client. This may produce complex JSON, but this is obfuscated from the user of the library by tooling within it.

* **Minimize surprise.** We should try to make things the least surprising as possible: if there is a direct comparison with something in a programing language it should act the same.

* **Workflow primitives should be kept to a minimum.** It needs to fit in a developers head to be understandable and have utility. This is another place there tooling is key; if you can construct a feature from primitives, do. Hide this construction behind tooling. This keeps features the client is required to implement to a minimum.

* **Primitives have clearly defined behavior.** It is up to the client to follow those definitions, otherwise it violates the principle of being implementation indepedent.

* **Context is transparent up the stack but not down.** This means a subflow can access everything its parent can, but the parent can not do likewise for a subflow. A parent flow only "sees" the result of the subflow. Think of a class function and its return value.

* **Write tools.** Extension via tooling allows for backwards compatibility, while also making usage richer. Tools allow for complex flow composition, without the overhead of direct implementation - you can do more with less.

*****************
Prime directive
*****************

The ultimate aim of workflows is to enable non-technical users to build workflows with the aid of visual programming.


.. glossary::

********
Glossary
********

This is a glossary of terms used throughout this documentation.

* **Context** is the datastore.
* **Subflow** is a flow/loop task on another flow. That is to say, it is not a different type than a flow in general, but simply is a flow existent as a task on another flow. In this way flows can be nested to create richer, more complex workflows.


*****************
Table of Contents
*****************

.. toctree::
   :name: mastertoc
   :maxdepth: 1

   quickstart
   structure
   primitives
   library_api
   extending


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

