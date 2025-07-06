# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
- Run tests: `uv run pytest tests/ --cov=src --cov-report=term-missing -v`
- Run tests with coverage: `uv run pytest tests/ --cov=src --cov-report=xml --cov-report=term-missing -v`
- Run tests using tox: `tox`

### Linting and Formatting
- Run pre-commit hooks: `uv run pre-commit run --all-files`
- Format code: `uv run ruff format`
- Lint code: `uv run ruff check --fix`

### Dependencies
- Install dependencies: `uv sync --group dev`
- Install pre-commit hooks: `uv run pre-commit install --install-hooks`

### Building
- Build package: `uv build`

## Architecture

### Core Components

**munge** is a data manipulation library and CLI tool that provides codec-based data transformation between different formats (JSON, YAML, TOML, etc.).

#### Key Modules

- **`base.py`**: Contains `CodecBase` metaclass and abstract base class for all codecs. Implements URL opening, loading, and dumping functionality.
- **`codec/`**: Directory containing format-specific codecs (JSON, YAML, TOML, MySQL). Each codec extends `CodecBase` and registers itself via metaclass.
- **`config.py`**: Configuration management with `Config` and `MungeConfig` classes. Handles reading/writing config files and URL parsing.
- **`cli.py`**: Command-line interface implementation using Click. Provides main entry point for data format conversion.

#### Architecture Patterns

1. **Codec Registration**: Codecs self-register via metaclass `Meta` in `base.py:10-30`
2. **URL-based Data Sources**: Supports file paths, HTTP(S) URLs, and custom schemes via `parse_url()` in `config.py:205-253`
3. **Plugin System**: Codecs are dynamically loaded and registered in `codec/__init__.py`

#### Data Flow

1. CLI parses input/output arguments
2. `parse_url()` determines codec from file extension or URL scheme
3. Source codec loads data using `loadu()` method
4. Data is transformed/manipulated as needed
5. Destination codec saves data using `dumpu()` method

The library supports both programmatic use via the `munge` module and command-line usage via the `munge` CLI tool.