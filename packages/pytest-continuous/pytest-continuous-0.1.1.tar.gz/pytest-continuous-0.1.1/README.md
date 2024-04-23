# Pytest Continuous

This plugin allows running pytest tests continuously until they fail or the process is manually stopped (e.g., via CTRL+C).

## Installation

Install using pip:

```bash
pip install pytest-continuous
```

## Usage

Add the --continuous option to your pytest command.

```bash
pytest --continuous
```

## Example

```bash
pytest test_example.py --continuous
```
