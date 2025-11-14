# BioTrackr

[![PyPI](https://img.shields.io/pypi/v/biotrackr.svg)](https://pypi.org/project/biotrackr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/miotsdata/biotrackr.svg)](https://github.com/miotsdata/biotrackr/issues)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/miotsdata/biotrackr.svg)](https://github.com/miotsdata/biotrackr)

**BioTrackr** is a lightweight CLI tool for managing, analyzing, and reporting biological data.

---

## Features
- Easy-to-use command-line interface
- YAML configuration support
- HTML report generation
- Flexible filtering (`--since_days`) and offline mode (`--no-fetch`)
- Output to custom files (`--output_file`)

---

## Installation

Install via PyPI:

```bash
pip install biotrackr
```

Or install the latest version from GitHub:
```
pip install git+https://github.com/miotsdata/biotrackr.git
```

--- 

## Usage

Run with default configuration:
```
biotrackr
```

Use a custom config:
```
biotrackr --config path/to/config.yaml
```

Examples:

No data fetching:
```
biotrackr --no-fetch
```

Last 14 days only:
```
biotrackr --since_days 14
```

Save output to a file:
```
biotrackr --output_file report.html
```

---

## Configuration

BioTrackr uses YAML configuration files. The default is included in:
```
src/biotrackr/config/base.yaml
```

Override it with --config.

---

## Contributing

Contributions are welcome! Open issues or submit pull requests on GitHub

## License

MIT License. See LICENSE

