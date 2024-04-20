# Flake8 One Dot Per Line Plugin

`flake8-one-dot` is a Flake8 plugin that enforces the Object Calisthenics principle of "One Dot Per Line" to promote better encapsulation and minimize the violation of the law of Demeter in Python code. It achieves this by flagging lines that contain multiple attribute accesses, which can indicate a code smell related to excessive knowledge of internal structures.

## Installation

Install `flake8-one-dot` via pip:

```bash
pip install flake8-one-dot
```

## Usage

After installation, the plugin will automatically be activated when you run Flake8:

```bash
flake8 your_project_directory
```

Any line with more than one dot will be reported as a violation, prompting a refactoring suggestion to improve encapsulation.

## Configuration

`flake8-one-dot` does not require any specific configurations and works out-of-the-box with the default Flake8 settings.

## Rules Enforced

- **FOD100**: Too many dots per line (more than one dot found)

This rule helps developers recognize lines of code that may be overly reliant on object internals or chain multiple method calls in ways that could complicate future refactoring and maintenance.

## Motivation

The "One Dot Per Line" rule helps maintain clean separation between objects and their internal data, encouraging methods to be short and ensuring that objects interact with each other through well-defined interfaces. This reduces coupling and enhances modularity, making the codebase easier to understand and maintain.

## Contributing

We appreciate contributions from the community to make `flake8-one-dot` more effective or to fix potential bugs. If you have suggestions or want to contribute code, please feel free to fork the repository, make your changes, and submit a pull request.

## License

This plugin is distributed under the MIT License. The full license text can be found in the `LICENSE` file included with the source code.
