## Setup

### 1. Set up environment
```bash
git clone --recurse-submodules "https://github.com/GUARDIANS-infrastructure/omix3schemadev.git"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cd gen3schemadev && pip install -e .
cd acdc-tools && pip install -e .
```
### 2. Install Docker
To install Docker Desktop, download it from the [Docker website](https://www.docker.com/products/docker-desktop) and follow the installation instructions for your operating system. After installation, verify by running `docker --version` in the terminal.

### 3. Spin up containers
```bash
cd umccr-dictionary
make down
make pull
make up
make ps
cd ..
```