import json
from pathlib import Path
from argparse import ArgumentParser


class MissingValidator(Exception):
    pass


def main():
    parser = ArgumentParser(description="")
    parser.add_argument(
        "-i",
        "--input",
        help=" ".join(("A file containing a workflow", "or '-' to read from stdin.",)),
    )
    args = parser.parse_args()
    with open("/dev/stdin" if args.input == "-" else args.input) as fid:
        workflow = json.load(fid)
    missing_validators = find_missing_validators(workflow)
    if missing_validators:
        raise MissingValidator(
            "Validators are used in the flow but are not found in the validator section: "
            ", ".join(missing_validators)
        )


def find_missing_validators(workflow):
    flow_validators = set(_get_validators_from_task(workflow["flow"], workflow["components"]))
    workflow_validators = set(workflow["validators"].keys())
    return flow_validators - workflow_validators


def _get_validators_from_task(task, component_dict):
    task_type = task["type"]

    if task_type == "flow":
        conditions = task.get("config", {}).get("conditions")
        if conditions:
            yield from conditions

        for sub_task in task["tasks"]:
            yield from _get_validators_from_task(sub_task, component_dict)

    elif task_type == "screen":
        yield from _get_validators_from_screen(task, component_dict)

    preconditions = task.get("preconditions")
    if preconditions:
        yield from preconditions


def _get_validators_from_screen(screen, component_dict):
    for row in screen["components"]:
        for lookup in row:
            component_name = lookup["name"]
            component = component_dict[component_name]
            preconditions = component.get("preconditions")
            if preconditions:
                yield from preconditions


if __name__ == "__main__":
    main()
