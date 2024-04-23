- [flake8-deep-calls](#flake8-deep-calls)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Rules Enforced](#rules-enforced)
  - [Motivation](#motivation)
  - [Contributing](#contributing)
  - [License](#license)


# flake8-deep-calls

`flake8-deep-calls` is a Flake8 plugin aimed at reducing complexity in Python code by enforcing the Object Calisthenics rule to "Limit Nesting to One Level." This plugin identifies functions that call other functions in a nested manner, going beyond one level deep, which may indicate overly complex code structures.

## Installation

To install `flake8-deep-calls`, you can use pip:

```bash
pip install flake8-deep-calls
```

## Usage

Once installed, the plugin will automatically be included when you run Flake8. To analyze your project, simply use:

```bash
flake8 your_project_directory
```

The plugin will flag functions with excessive call depth, helping you recognize areas where the code could be refactored to reduce complexity.

## Configuration

`flake8-deep-calls` works out-of-the-box with the default settings of Flake8. There are no additional configuration options needed specifically for this plugin as it leverages existing Flake8 configurations.

## Rules Enforced

- **FDC100**: Indicates functions that call other local functions more than one level deep.

Each violation specifies the function name and the depth of calls, guiding developers to consider flattening their function interactions or refactoring into simpler, more decoupled functions.

## Motivation

The motivation behind this plugin is to help developers adhere to clean code principles that facilitate easier maintenance, testing, and understanding of the code. By limiting the depth of nested function calls, the code remains straightforward and more aligned with the Single Responsibility Principle.

## Contributing

Contributions to improve `flake8-deep-calls` are welcome! If you have suggestions for improvements, bug reports, or new features, please feel free to contribute to the project by opening issues or submitting pull requests on our GitHub repository.

## License

`flake8-deep-calls` is open-sourced software licensed under the MIT License. See the `LICENSE` file for more details.
