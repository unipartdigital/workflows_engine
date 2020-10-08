
****************
Tao of workflows
****************

Table of Contents
#################

.. toctree::
   :name: mastertoc
   :maxdepth: 1

   quickstart
   structure
   primitives
   library_api
   extending


This section is to explain the principle ideas of workflows.
**Workflows is a JSON object encoding actions to be taken by the client.**
With the focus being on the JSON object produced means that the library and client could be
replaced independently as required by the use case. The reason for this is to be technology
independent. The server should not care about the client and the client should not care about the
server (baring interfaces).

Workflows features should be written with some key principles in mind:

* **The client's job is to display information.** Processing and domain logic should be handled by the backend (note: handled might mean defining a task in the workflow).

* **Ease of execution of the JSON object should be top priority.** This means where possible complexity should be in the library producing the workflow. As it can be hidden from the user of the library by the tooling within the library.

* **Minimize surprise.** We should try to make things as least surprising as possible if there is a direct comparison with something in a programing language it should act the same.

* **Workflow primitives should be kept to a minimum.** It needs fit in someones head to be understandable. This is another place there tooling is key if you can construct a feature out of primitives do it. Then hide the construction behind tooling. This allows the things required to implement in the client to be minimal.

* **Primitives have clearly defined behavior.** It is up to the client to follow those definitions or it breaks the point of being able to drive multiple clients.

* **Context is transparent looking up the stack but not down.** This means a subflow can see everything in its parent can see but the parent can not look into its subflow. A parent flow only "sees" the result of the subflow. Think of a class function and its return value.

* **Write tools.** Extending using tools allows for backwards compatibility while also making usage richer.

*****************
Things to aim for
*****************

The aim of workflows is to ultimately enable non-technical users to build workflows with the aid of visual programing.

********
Glossary
********

This is a glossary of terms used throughout this documentation.

* **Context** is the datastore.
* **Subflow** is a flow/loop task which is a subtask of another flow.
