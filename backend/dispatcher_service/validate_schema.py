#!/usr/bin/env python3
import os
import json
from jsonschema import validate, ValidationError

# ------- Configuration -------
BASE_DIR = os.path.dirname(__file__)
SCHEMAS_DIR = os.path.join(BASE_DIR, "schemas")
SCHEMA_PATH = os.path.join(SCHEMAS_DIR, "dispatch_task_schema.json")
# -----------------------------

def load_schema(path):
    with open(path) as f:
        return json.load(f)

def load_examples():
    # ensure schemas is a package
    examples_path = os.path.join(SCHEMAS_DIR, "examples.py")
    if not os.path.exists(examples_path):
        raise FileNotFoundError(f"No examples.py at {examples_path}")
    # import examples
    from schemas.examples import example_messages
    return example_messages

def test_example(name, msg, schema):
    print(f"▶️ Testing {name}")
    try:
        validate(instance=msg, schema=schema)
        print(f"{name}: ✅ Validation passed")
    except ValidationError as e:
        print(f"{name}: ❌ Validation error: {e.message}")

def main():
    print("⏳ Starting validate_schema.py")

    # Load schema
    try:
        schema = load_schema(SCHEMA_PATH)
        print("📄 Loaded dispatch_task_schema.json successfully")
    except Exception as e:
        print(f"❌ Failed to load schema: {e}")
        return

    # Load examples
    try:
        example_messages = load_examples()
        print(f"🔍 example_messages keys: {list(example_messages.keys())}")
    except Exception as e:
        print(f"❌ Failed to import example_messages: {e}")
        return

    # Run tests
    for name, msg in example_messages.items():
        test_example(name, msg, schema)

if __name__ == "__main__":
    main()




#To run: 
# cd backend/dispatcher_service
# python validate_schema.py
