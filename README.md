# Omix3 Schema Development

This repo utilises [gen3schemadev](https://github.com/AustralianBioCommons/gen3schemadev) to create and manage the Omix3 Gen3 data dictionary.

For full documentation, see the [gen3schemadev quickstart guide](https://github.com/AustralianBioCommons/gen3schemadev/blob/main/docs/gen3schemadev/quickstart.md).

## 1. Setup

Install [Poetry](https://python-poetry.org/docs/#installation), then install dependencies:

```bash
poetry install
```

Activate the Poetry environment:

```bash
poetry shell
```

Alternatively, prefix commands with `poetry run` (e.g. `poetry run gen3schemadev init`).

## 2. Create the input_yaml template

Learn how to create one [here](https://github.com/AustralianBioCommons/gen3schemadev/blob/main/docs/gen3schemadev/quickstart.md).

You can also create a template starting file with the command below:

```bash
gen3schemadev init
```

Alternatively you can define the template file name:

```bash
gen3schemadev init -o dictionary/input_dd.yaml
```

## 3. Generate Gen3 Schemas

Will convert the input_yaml to a folder of Gen3 schemas:

```bash
gen3schemadev generate -i dictionary/input_dd.yaml -o dictionary/test_dict/
```

### 3.1 Further Gen3 YAML Configuration (optional)

This step is for advanced users that want to edit Gen3 JSON Schemas manually. You can learn more about how to modify Gen3 schemas [here](https://github.com/AustralianBioCommons/gen3schemadev/blob/main/docs/gen3schemadev/quickstart.md).

## 4. Validate Schema

After you are happy with the folder of Gen3 schemas, validate them:

```bash
gen3schemadev validate -y dictionary/test_dict
```

This will validate against the Gen3 metaschema and run business rule validation.

## 5. Bundle Schemas

Bundle the Gen3 schemas into a single Gen3 Bundled Schema. This bundled JSON file is used to deploy the model into Gen3 via the sheepdog microservice.

```bash
gen3schemadev bundle -i dictionary/test_dict -f dictionary/test_dict/omix3_schema.json
```

## 6. Visualise the Gen3 Data Dictionary

**Important:** You must have [Docker Compose](https://docs.docker.com/compose/install/) installed.

```bash
gen3schemadev visualise -i dictionary/test_dict/omix3_schema.json
```

## Development Workflow

This repository uses a `dictionary/test_dict` folder for testing and a `dictionary/prod_dict` folder for production.

1. Generate and validate schema changes in `dictionary/test_dict/`
2. Copy to production when ready
3. The `dictionary/prod_dict/omix3_schema.json` file is what will be used for deployment

### Copying Files Between Folders

Copy from test to production:

```bash
bash dictionary/copy_to_prod.sh
```

Copy from production to test:

```bash
bash dictionary/copy_to_test.sh
```