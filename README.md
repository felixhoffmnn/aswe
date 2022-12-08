<h1 align="center">
 HiBuddy
</h1>

<h4 align="center">
 A speech bot for your daily needs build during advanced software engineering at DHBW Stuttgart.
</h4>

<div align="center">
    <a href="https://github.com/felixhoffmnn/python_template">
        <img src="https://img.shields.io/github/license/felixhoffmnn/python_template"
        alt="License: MIT" />
    </a>
    <a href="https://www.python.org/downloads/release/python-3100/">
        <img src="https://img.shields.io/badge/python-3.10-blue.svg"
        alt="Python 3.10" />
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://github.com/prettier/prettier">
        <img src="https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat&logo=appveyor"
        alt="Codestyle: Prettier" />
    </a>
    <a href="https://results.pre-commit.ci/latest/github/felixhoffmnn/aswe/main">
        <img src="https://results.pre-commit.ci/badge/github/felixhoffmnn/aswe/main.svg"
        alt="pre-commit" />
    </a>
    <a href="https://codecov.io/gh/felixhoffmnn/aswe" >
        <img src="https://codecov.io/gh/felixhoffmnn/aswe/branch/main/graph/badge.svg?token=AO8OYDJNDN" alt="Code coverage"/>
    </a>
</div>
<br>

<div align="center">
    <a href="https://github.com/felixhoffmnn/aswe">GitHub</a>
    ·
    <a href="https://github.com/felixhoffmnn/aswe/actions">CI/CD</a>
    ·
    <a href="https://felixhoffmnn.github.io/aswe/">Dokumentation</a>
</div>
<br>

<!-- TODO: Review paragraph -->

This project was built by a team of 5 students during the advanced software engineering course at [DHBW Stuttgart](https://www.dhbw-stuttgart.de/). The goal was to create a bot that can interact using speech-to-text and text-to-speech with the user and perform tasks like a morning briefing, a helper for planning trips and events, and also to provide information about current sports events.

## :rocket: Requirements & Usage

> :arrow_up: Python 3.10 is required

Following dependencies are listed which are required to either run or contribute to this project.

1. Install `portaudio` for speech recognition:
    - On _Windows_: Everything should be installed by default
    - On _macOS_: `brew install portaudio`
    - On _Linux_: `sudo apt install python3-pyaudio`
2. Install python dependencies:

    - Using _Poetry_
        1. Install [Poetry](https://python-poetry.org/docs/#installation)
            - Poetry is a dependency manager for Python used in this project
            - (Optional) Setup poetry to use the local `.venv` folder by running `poetry config virtualenvs.in-project true`
        2. Run `poetry install` to install all dependencies
            - Afterwards, run `poetry shell` to activate the virtual environment
    - Using _Pip_ (not recommended)

        ```bash
        pip install -r requirements.txt -r requirements_dev.txt -r docs/requirements_docs.txt
        ```

3. Install the pre-commit hooks with `pre-commit install`

> :warning: **Note:** If you are using _Poetry_ it is recommended to use `poetry run <command>` to run commands. When using _Pip_ it is possible that the `env` variables are not loading correctly.

<br>

After the setup is complete, use the **following commands** to run the agent. Note that you need to be in the **root directory** of the project.

```bash
# If want to run the agent with the default settings
python aswe/core/agent.py main

# With this you can trigger a specific proactivity
python aswe/core/agent.py main --test_proactivity 4

# If you want to get the microphone input
python aswe/core/agent.py main -- --get_mic

# If you want to trigger a specific proactivity and get the microphone input
python aswe/core/agent.py main --test_proactivity 3 --get_mic
```

## :speech_balloon: Concept

In the following section we will go into detail about the concept of the agent. The agent is divided into three main parts: the **speech** and **text conversion**, the **agent**, the **use cases**, and the **API layer**.

<!-- TODO: Fix link to diagram -->

![Concept](https://github.com/felixhoffmnn/aswe/blob/main/data/flowcharts/layerd_architecture_2.png)

## :repeat: CI/CD

This project uses [pre-commit](https://pre-commit.com) to ensure a consistent code style before committing. This pipeline runs primarily before committing, but will also be triggered as CI/CD pipeline on GitHub using [pre-commit.ci](https://pre-commit.ci/). The related files is named `.pre-commit-config.yaml`. This includes the following checks:

1.  Lock project dependencies and export `requirements.txt`
2.  Check common hooks (e.g., yaml, merge conflicts, case conflicts)
3.  Sort imports with [isort](https://github.com/PyCQA/isort)
4.  Format code with [black](https://github.com/psf/black) and [flake8](https://github.com/PyCQA/flake8)
5.  Check typing with [mypy](https://github.com/python/mypy)
6.  Format markdown and yaml files with [prettier](https://github.com/prettier/prettier)
7.  Check for correct and new python styling with [pyupgrade](

After committing, the GitHub actions CI/CD pipeline will be triggered. The related files can be found in the `.github/workflows` folder. This includes the following checks:

1. Run tests with [pytest](https://github.com/pytest-dev/pytest)
2. Calculates code coverage with [pytest-cov](https://github.com/pytest-dev/pytest-cov) and uploads it to [Codecov](https://codecov.io/gh/felixhoffmnn/aswe)
3. Builds and deploys the [MkDocs](https://www.mkdocs.org/) documentation (see [here](https://felixhoffmnn.github.io/aswe/))
4. Checks code quality and security with [CodeQL](https://github.com/github/codeql)

## :memo: License

This project is licensed under [MIT](https://github.com/felixhoffmnn/aswe/blob/main/LICENSE).
