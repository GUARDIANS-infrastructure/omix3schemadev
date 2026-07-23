# How to Use gen3schemadev

This page covers the commands used in this repository and the shape of the input file. For the
overall workflow and where the source of truth lives, start with the [README](../README.md).

For the tool's own documentation, see the
[gen3schemadev repository](https://github.com/AustralianBioCommons/gen3schemadev).

---

## The input file

`dictionary/input_dd.yaml` describes the whole model in four top-level keys:

```yaml
version: 1.3.0                              # the dictionary version
url: https://omix3.test.biocommons.org.au/  # becomes each node's namespace
nodes: [...]                                # the tables in the model
links: [...]                                # the relationships between them
```

### Nodes

Each node needs a name, a category, a description and its properties:

```yaml
- name: sample
  category: biospecimen
  description: >
    A biospecimen collected from a participant.
  properties:
    - name: sample_type
      description: "The kind of material sampled."
      type: string
```

`category` matters. Nodes with `category: data_file` are treated specially — gen3schemadev adds the
standard file properties and a link to `core_metadata_collection`.

### Links

Links are declared as a flat list at the bottom of the file, read as "one parent is linked to
*multiplicity* children":

```yaml
links:
  - parent: subject
    multiplicity: one_to_many
    child: sample
```

**Optional parents.** Every link is required by default. Add `required: false` when a parent is
optional — this repository uses it for the nine measurement links that may be recorded without a
site:

```yaml
  - parent: site
    multiplicity: one_to_one
    child: anthropometric_measurements
    required: false
```

`required` is set per link, so where a node has two or three parents each is answered
independently. When a node has more than one parent the links are collected into a subgroup
automatically; that subgroup means "at least one of these", so a node whose links are all optional
is still never orphaned. See
[Defining Links in Gen3](https://github.com/AustralianBioCommons/gen3schemadev/blob/main/docs/gen3_data_modelling/links.md)
for the detail.

**Do not declare links whose child is `program`, `project` or `core_metadata_collection`.** Those
nodes come from gen3schemadev's packaged templates complete with their links, so such a declaration
is discarded. The link from a `data_file` node *to* `core_metadata_collection` is added for you.

### Property types

| `type:` | Produces | Notes |
| --- | --- | --- |
| `string` | A plain string with your description | The safe default |
| `integer`, `number`, `boolean` | The matching JSON Schema type | |
| `enum` | A closed list of values | Requires an `enums:` list |
| `array` | A list of strings | Items are always strings |
| `datetime` | A reference to the shared datetime definition | Requires a **full RFC 3339 timestamp**, so a date-only field should be `type: string` |

**Removing an enum value is a breaking change** — data already submitted with that value stops
validating. Adding values is safe.

---

## Commands

All commands run from the repository root. Prefix with `poetry run`, or activate the environment
first with `eval $(poetry env activate)`.

### Generate

```bash
poetry run gen3schemadev generate -i dictionary/input_dd.yaml -o dictionary/prod_dict/ --input-driven
```

`generate` **refuses to overwrite existing files** unless told to. `--input-driven` is the right
flag here: it declares that `input_dd.yaml` is the source of truth, so regenerating is expected and
safe, and it turns an unreproducible leftover file into an error rather than a warning.

The other options, for reference:

| Flag | Effect |
| --- | --- |
| `--input-driven` | Regenerate everything; fail on files the input cannot produce |
| `--only <node>` | Regenerate named nodes, leave every other file untouched |
| `--check` | Report drift, write nothing, exit non-zero if the folder does not match |
| `--force` | Overwrite everything, **discarding any hand edits** |

### Validate

```bash
poetry run gen3schemadev validate -y dictionary/prod_dict
```

Runs Gen3 metaschema validation and business-rule checks. Must exit 0.

### Bundle

```bash
poetry run gen3schemadev bundle -i dictionary/prod_dict -f dictionary/prod_dict/omix3_schema.json
```

Combines the folder into the single JSON file Gen3 loads via the sheepdog microservice. It includes
**every** YAML in the folder, whether or not the input produced it, so a leftover schema still
ships — which is why `--check` reporting an orphan is worth acting on.

### Visualise

```bash
poetry run gen3schemadev visualise -i dictionary/prod_dict/omix3_schema.json
```

Renders the model as a graph at `http://localhost:8080`. Requires Docker Compose — see
[Setup](setup.md#prerequisites).

### Removing a node

`generate` writes the nodes your input declares. It does not delete the schema for a node you have
removed from `input_dd.yaml`, so take the file out yourself:

```bash
git rm dictionary/prod_dict/<node>.yaml
```

Until you do, `--check` reports it as an orphan and `bundle` keeps shipping it.

---

## Checking your change did what you meant

CI runs these checks on every pull request, but catching a problem locally is faster than catching
it in a failed build.

```bash
git diff --stat
poetry run gen3schemadev generate -i dictionary/input_dd.yaml -o dictionary/prod_dict/ --check
```

A healthy repository reports `OK`. Otherwise `--check` names the problem in one of three categories:

- **Changed** — the file on disk differs from what the input produces. Someone hand-edited it, or
  the input changed without regenerating
- **Missing** — the input describes a node that is not in the folder, so it will not be deployed
- **Orphaned** — a file the input cannot produce, which still ships in the bundle

---

## Troubleshooting

**A YAML parse error** is usually a missing colon after a node name — `- name_of_node` where
`- name: name_of_node` was meant. The reported line can be slightly below the line at fault. This
exact typo made the input unparseable for six weeks in 2026, which is why the drift check now runs
in CI.

**Pydantic validation errors** mean the input does not match the expected structure. The error
location reads as a path into the file, so `nodes.3.properties.2.type` is the type of the third
property of the fourth node. Unknown field names are rejected rather than ignored, so a misspelled
key fails here rather than silently dropping the field.

**A property or link you added does not appear.** Check it is not on `program`, `project` or
`core_metadata_collection`, whose declarations come from packaged templates.
