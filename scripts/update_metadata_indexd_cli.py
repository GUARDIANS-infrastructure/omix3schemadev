import argparse
import os
import sys
import json
from gen3.auth import Gen3Auth

# Ensure module-level imports are at the top
sys.path.append(os.path.abspath('gen3schemadev'))
from gen3schemadev import gen3synthdata as g3s

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Update metadata for given projects with indexd GUIDs."
    )
    parser.add_argument(
        "-d", "--base_dir", type=str, required=True,
        help="The base directory containing the metadata files."
    )
    parser.add_argument(
        "-a", "--auth_file", type=str, required=True,
        help="The path to the authentication file."
    )
    parser.add_argument(
        "-i", "--indexd_guid_file", type=str, required=True,
        help="The path to the indexd GUID file."
    )
    parser.add_argument(
        "-p", "--project_ids", type=str, nargs='+', required=True,
        help="The list of project IDs."
    )
    return parser.parse_args()

def update_metadata(base_dir, auth_file, indexd_guid_file, project_id):
    """
    Update metadata for a given project.

    Args:
        base_dir (str): The base directory containing the metadata files.
        auth_file (str): The path to the authentication file.
        indexd_guid_file (str): The path to the indexd GUID file.
        project_id (str): The project ID.
    """
    g3s.update_metadata(base_dir, auth_file, indexd_guid_file, project_id=project_id)

def main():
    args = parse_arguments()

    if not os.path.exists(args.base_dir):
        print(f"Error: Base directory {args.base_dir} does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.auth_file):
        print(f"Error: Authentication file {args.auth_file} does not exist.")
        sys.exit(1)

    if not os.path.isfile(args.indexd_guid_file):
        print(f"Error: Indexd GUID file {args.indexd_guid_file} does not exist.")
        sys.exit(1)

    for project_id in args.project_ids:
        project_base_dir = os.path.join(args.base_dir, project_id)
        if not os.path.exists(project_base_dir):
            print(
                f"Warning: Project base directory {project_base_dir} does not exist. Skipping project {project_id}."
            )
            continue

        update_metadata(project_base_dir, args.auth_file, args.indexd_guid_file, project_id)
        print(f"Metadata update for project {project_id} completed successfully.")

if __name__ == "__main__":
    main()