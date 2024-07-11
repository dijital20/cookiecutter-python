"""Handle generating the requirements.txt."""

import shlex as sh
import subprocess as sp


def run_cmd(message: str, command: str | list[str]):
    """Run a given command.

    Args:
        command: Command to run.
    """
    match command:
        case str():
            command = sh.split(command)

        case list():
            pass

        case _:
            raise ValueError("command should be a str or list[str].")

    print(f"--> {message}")
    result = sp.run(
        args=command,
        stderr=sp.STDOUT,
        stdout=sp.PIPE,
        check=False,
        text=True,
        encoding="UTF-8",
    )
    print(f"{sh.join(result.args)} returned {result.returncode}:\n{result.stdout}")


if __name__ == "__main__":
    if "{{ cookiecutter.compile_with_uv }}" == "True":
        run_cmd(
            "Compile requirements.txt",
            "uv pip compile pyproject.toml -o requirements.txt",
        )
        run_cmd(
            "Compile requirements-dev.txt",
            "uv pip compile pyproject.toml --extra dev -o requirements-dev.txt",
        )
        run_cmd(
            "Create virtual environment",
            "uv venv",
        )
        run_cmd(
            "Sync dev dependencies",
            "uv pip sync requirements.txt requirements-dev.txt",
        )

    if "{{ cookiecutter.initialize_git }}" == "True":
        run_cmd(
            "Initialize git",
            "git init -b main",
        )
        run_cmd(
            "Stage everything",
            "git add *",
        )
        run_cmd(
            "Create initial commit",
            'git commit -m "Initial cookiecutter"',
        )
