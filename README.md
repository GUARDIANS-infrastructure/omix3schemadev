# Omix3 Schema Development

This repo utilises [gen3schemadev](https://github.com/AustralianBioCommons/gen3schemadev) to create and manage the Omix3 Gen3 data dictionary.

## Documentation

- [Setup & Prerequisites](docs/setup.md) — Python, Poetry, Docker Compose, and installation steps
- [How to Use gen3schemadev](docs/how_to_use.md) — init, generate, validate, bundle, and visualise commands

## Development Workflow

This repository uses a `dictionary/test_dict` folder for testing and a `dictionary/prod_dict` folder for production.

1. Generate and validate schema changes in `dictionary/test_dict/`
2. Copy to production when ready
3. The `dictionary/prod_dict/omix3_schema.json` file is what will be used for deployment

### Copying Files Between Folders

Copy from test to production:

```bash
bash scripts/copy_to_prod.sh
```

Copy from production to test:

```bash
bash scripts/copy_to_test.sh
```