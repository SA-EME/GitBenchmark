<h1 align=center>Git Benchmark</h1>

<p align=center>
  <a href="https://github.com/SA-EME/GitBenchmark"><img src="https://img.shields.io/badge/GB-0.8.4-%23f7df1e?style=for-the-badge" alt="GitBenchmarkVersion"/></a>
  <img src="https://img.shields.io/badge/LANGUAGE-PYTHON-ad2828?style=for-the-badge" alt="PythonProject"/>
</p>

GitBenchmark is a command-line tool designed to facilitate Git usage and ensure compliance with commit standards. It provides commands for managing scopes, commit types, and commits.

## Installation

1. **Prerequisites**: Make sure you have Git installed. You can check your Git version by running the following command:

    ```bash
    git --version
    ```

    If Git is not installed, please install it before proceeding.

2. **Install GitBenchmark**:
    - Download the binary from the releases page.
    - Place the binary in a directory included in your system's PATH.
    - You can now use the `gb` or `gitbenchmark` command in your terminal.

## Usage

Here are the main commands available:

- `gb init`: Initializes config files.
- `gb build [scope]`: Build to specific scope.
- `gb scope [add|remove|list|check] [scope]`: Configures scopes.
- `gb type [add|remove|list] [type]`: Configures commit types.
- `gb commit [type]`: Performs a commit.

## How to Contribute

We welcome contributions! Here's how you can contribute:

1. **Fork the GitBenchmark repository on GitHub**.
2. **Create a branch for your contribution**.
3. **Make your changes and test them**.
4. **Submit a pull request to the main branch**.

Feel free to reach out if you have any questions or suggestions!