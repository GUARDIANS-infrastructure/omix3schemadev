# Setup

## Prerequisites

| Dependency | Version | Notes |
|---|---|---|
| [Python](https://www.python.org/downloads/) | ≥ 3.12.10 | |
| [Poetry](https://python-poetry.org/docs/#installation) | ≥ 2.1.3 | |
| [Docker Compose](https://docs.docker.com/compose/install/) | latest | Optional — required only for dictionary visualisation |

## Installation

Clone the repository:

```bash
git clone https://github.com/AustralianBioCommons/omix3schemadev.git
cd omix3schemadev
```

Install Poetry (if not already installed):

```bash
pipx install poetry
```

Install project dependencies:

```bash
poetry install
```

Activate the Poetry environment:

```bash
eval $(poetry env activate)
```

Alternatively, prefix commands with `poetry run` (e.g. `poetry run gen3schemadev init`).
