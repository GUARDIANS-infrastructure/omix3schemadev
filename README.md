# Omix3 Schema Development

This repository holds the Gen3 data dictionary for Omix3. It uses
[gen3schemadev](https://github.com/AustralianBioCommons/gen3schemadev) to turn a single readable
input file into the folder of Gen3 schemas that gets deployed.

---

## Where the source of truth is

**`dictionary/input_dd.yaml` is the only file you edit by hand.**

Everything under `dictionary/prod_dict/` is generated from it. Those files are committed so the
deployed model is visible and reviewable, but they are build output. If you edit one directly, the
next person to regenerate will destroy your change.

Because the input is the source of truth, regeneration always uses `--input-driven`:

```bash
poetry run gen3schemadev generate -i dictionary/input_dd.yaml -o dictionary/prod_dict/ --input-driven
```

That flag is not optional here. It tells gen3schemadev that this repository regenerates from its
input, so overwriting is expected — and it makes a file the input cannot reproduce an error rather
than a warning, which is what keeps the two in step. Without it, `generate` refuses to touch the
folder at all.

This matters more than it sounds. `input_dd.yaml` was unparseable on `main` for six weeks in 2026
and nobody noticed, because the previously generated files were still present and looked healthy.
The CI check described below exists to make that impossible to repeat.

---

## Repository layout

| Path | What it is | Edit by hand? |
| --- | --- | --- |
| `dictionary/input_dd.yaml` | The data model: nodes, properties, links | **Yes — this is the source** |
| `dictionary/prod_dict/` | The generated, deployed dictionary | No — generated |
| `dictionary/prod_dict/omix3_schema.json` | The bundled schema Gen3 actually loads | No — generated |
| `docs/` | Setup and command reference | Yes |
| `reference/` | HViC variable lists used when choosing the demographic and medical-history enums. Provenance only — nothing reads them | Reference material |

**There is one dictionary folder.** This repository previously kept a second `test_dict` copy that
was byte-identical to `prod_dict` in every commit, which doubled the size of every diff without ever
being used as a staging area. Branches and pull requests do that job: your branch is the proposed
dictionary, `main` is the deployed one.

---

## Making a change

Install first — see [Setup](docs/setup.md). All commands run from the repository root.

**1. Branch.**

```bash
git switch main && git pull
git switch -c feat/add-something-useful
```

**2. Edit `dictionary/input_dd.yaml`.** See [How to use gen3schemadev](docs/how_to_use.md) for the
input format and this repository's gotchas.

**3. Generate.** Always with `--input-driven` — see above for why.

```bash
poetry run gen3schemadev generate -i dictionary/input_dd.yaml -o dictionary/prod_dict/ --input-driven
```

**4. Validate.** Gen3 metaschema plus business-rule checks. Must exit 0.

```bash
poetry run gen3schemadev validate -y dictionary/prod_dict
```

**5. Review the diff, and check for drift.**

```bash
git diff --stat
poetry run gen3schemadev generate -i dictionary/input_dd.yaml -o dictionary/prod_dict/ --check
```

`--check` writes nothing and exits non-zero if the folder no longer matches the input. It should
report `OK`. CI runs the same check on your pull request.

**6. Bundle.**

```bash
poetry run gen3schemadev bundle -i dictionary/prod_dict -f dictionary/prod_dict/omix3_schema.json
```

**7. Visualise (optional).** Requires Docker Compose.

```bash
poetry run gen3schemadev visualise -i dictionary/prod_dict/omix3_schema.json
```

**8. Commit and open a pull request.** `input_dd.yaml` and the regenerated `prod_dict/` belong in
the same commit, so the input and the generated output never disagree in history.

---

## Continuous integration

`.github/workflows/dictionary.yml` runs on every pull request and on `main`, checking four things:

- **the dictionary matches its input** — `generate --check`, so a hand-edited schema or a forgotten
  regeneration fails the build
- **the dictionary is valid Gen3** — metaschema and business-rule validation
- **the bundled schema is up to date** — the JSON Gen3 loads is generated separately from the
  schemas, so this catches a branch that regenerated but forgot to re-bundle
- **the version is consistent** — `input_dd.yaml` and `_settings.yaml` agree

Every one of these is a command from the workflow above, so any failure reproduces locally.

---

## Versioning and deployment

The dictionary version lives at the top of `dictionary/input_dd.yaml`:

```yaml
version: 1.3.0
```

`generate` copies it into `_settings.yaml` as `_dict_version`, so the two cannot drift. Do not edit
`_settings.yaml` by hand. `pyproject.toml` has its own version describing the tooling in this
repository — leave it alone; it is not the dictionary version and has not tracked one for five
releases.

### How a change actually reaches Gen3

Merging does not deploy anything. The deployment fetches the bundled schema **by git tag**:

```
https://raw.githubusercontent.com/GUARDIANS-infrastructure/omix3schemadev/refs/tags/<tag>/dictionary/prod_dict/omix3_schema.json
```

so the release loop is:

1. **Tag this repository** — e.g. `v1.3.0`, matching `_dict_version`
2. **Bump `dictionary_version`** in `omix3-dataops` at `config/deploy_config.yaml`
3. **Run** its `services/dictionary/deploy_dd.sh <test|staging|prod>`

Because that URL contains the folder and filename, **`dictionary/prod_dict/` and `omix3_schema.json`
are an external contract.** Renaming either breaks deployment silently, with nothing in this
repository to warn you.

---

## Documentation

- [Setup and prerequisites](docs/setup.md) — Python, Poetry, Docker Compose, installation
- [How to use gen3schemadev](docs/how_to_use.md) — the commands in detail, and the input format
- [gen3schemadev documentation](https://github.com/AustralianBioCommons/gen3schemadev) — the tool
  itself, including its guide to running a dictionary repository
