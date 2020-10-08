#! /usr/bin/env python3

import pathlib
from jsonschema import RefResolver, Draft7Validator
import json


def generate_store(base_path):
    base_path = pathlib.Path(base_path)
    store = {}
    for fp in base_path.rglob(SCHEMA_NAME_GLOB):
        schema = json.load(fp.open())
        store[schema["$id"]] = schema
    return store


SUFFIX = ".json"
TEMPLATE = "http://udes.io/jsonschema/workflows/{name}.{suffix}"
SCHEMA_NAME_GLOB = "*.{}".format(SUFFIX.lstrip("."))
SCHEMA_INDEX = generate_store(pathlib.Path(__file__).parent.joinpath("../schema").absolute())


def get_validator_for(schema_name, schema_index=SCHEMA_INDEX, suffix=SUFFIX):
    schema = schema_index[TEMPLATE.format(name=schema_name, suffix=suffix.lstrip("."))]
    resolver = RefResolver.from_schema(schema, store=schema_index)
    return Draft7Validator(schema, resolver=resolver)
