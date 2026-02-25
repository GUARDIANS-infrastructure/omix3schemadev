# Omix3 Schema Development

This repo utilises [gen3schemadev](https://github.com/AustralianBioCommons/gen3schemadev) to create and manage the Omix3 Gen3 data dictionary.

## Documentation

- [Setup & Prerequisites](docs/setup.md) — Python, Poetry, Docker Compose, and installation steps
- [How to Use gen3schemadev](docs/how_to_use.md) — init, generate, validate, bundle, and visualise commands

## Development Workflow

This repository uses two folders for the Gen3 schema files:

- **`dictionary/test_dict/`** — where you make and test changes
- **`dictionary/prod_dict/`** — the production-ready version used for deployment

When making changes to the data dictionary, follow these steps in order:

1. **Edit the input file** — Make your changes in `dictionary/input_dd.yaml` (add nodes, properties, links, etc.)
2. **Generate YAML schemas** — Convert the input file into individual Gen3 YAML schema files in `dictionary/test_dict/`
3. **Validate** — Run validation to check for errors against the Gen3 metaschema and business rules
4. **Visualise** — Spin up a local visualisation to review the data model graph (requires Docker Compose)
5. **Update the version** — Bump the version number in `dictionary/test_dict/_settings.yaml`
6. **Bundle** — Combine the YAML schemas into a single bundled JSON file (`omix3_schema.json`)
7. **Copy to production** — Run `bash scripts/copy_to_prod.sh` to copy `test_dict` into `prod_dict`
8. **Cut a Git release** — Commit, push, and create a tagged release

See [How to Use gen3schemadev](docs/how_to_use.md) for the exact commands for each step.