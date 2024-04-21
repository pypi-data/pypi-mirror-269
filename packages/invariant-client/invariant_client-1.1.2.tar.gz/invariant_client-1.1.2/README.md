# Invariant CLI and Python SDK

## Installation

The Invariant client is available as a Python package. You can install it through pip or pipx like so:

```bash
pip install invariant-client

# Or using pipx
pipx install invariant-client
```

The Invariant CLI can be used to run Invariant from your test automation workflow. This example shows one way to install it for Github Actions:

```yaml
steps:
- uses: actions/checkout@v4
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'
- name: Install dependencies
  run: python -m pip install --upgrade pip invariant-client
- name: Evaluate current directory using Invariant
  run: |
    python -m invariant-client run
```

## Usage: Command Line Interface

The Invariant CLI can analyize local changes to network configuration files.

```bash
$ invariant login
Open this link in your browser to log in:
https://invariant.tech/login?code=320664
Login successful.

$ invariant run
Uploading snapshot...
Processing... (51643c3e-9a08-47b9-968e-1d2d7e2ca42e)
Analysis complete.

+---------------+----------+
| File          | RowCount |
+---------------+----------+
| exposed_ports |       15 |
+---------------+----------+

$ invariant show exposed_ports --json
# JSON report here
```

