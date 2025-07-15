import json
import os
import sys


def update_dict_version(release_version):
    try:
        current_directory = os.path.abspath(os.getcwd())
        print("Current Directory:", current_directory)

        schema_path = os.path.join(current_directory, "output", "schema", "json", "schema_dev.json")

        with open(schema_path, "r") as f:
            schema = json.load(f)

        schema["_settings.yaml"]["_dict_version"] = release_version
        print(f"settings.yaml dict version value = {schema['_settings.yaml']['_dict_version']}")

        with open(schema_path, "w") as f:
            json.dump(schema, f, indent=4)

        print(f"Dictionary version updated to {release_version} in {schema_path}")

    except FileNotFoundError:
        print(f"Error: The file {schema_path} does not exist.")
        sys.exit(1)

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the schema file.")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_dict_version.py <release_version>")
        sys.exit(1)

    release_version_arg = sys.argv[1]
    update_dict_version(release_version_arg)