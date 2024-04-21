import pytest
from click.testing import CliRunner

from mychef import cli


@pytest.fixture
def patch_alembic_migration(monkeypatch: pytest.MonkeyPatch):
    def patch():
        print("patched migrations...")

    monkeypatch.setattr(cli, "upgrade_to_head", patch)


@pytest.fixture
def patch_generate_secret_token(monkeypatch: pytest.MonkeyPatch):
    def patch() -> str:
        return "PATCHED-KEY-123ABC"

    monkeypatch.setattr(cli.hashing, "generate_secret_token", patch)


@pytest.fixture
def patch_uvicorn_server(monkeypatch: pytest.MonkeyPatch):
    def patch(*args, **kwargs):
        print("patched server received the following params:")
        print(f"args: {args}")
        print(f"kwargs: {kwargs}")

    monkeypatch.setattr(cli.uvicorn, "run", patch)


def test_calling_mychef_without_args_launches_help(cli_runner: CliRunner):
    expected_help_text = """\
Usage: mychef [OPTIONS] COMMAND [ARGS]...

  Control panel for managing mychef application.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  init   Instantiate the application environment and secret key.
  run    Migrate database to latest version and launch application server.
  users  Control panel for managing users.
"""
    result = cli_runner.invoke(cli.mychef, [])

    assert result.exit_code == 0
    assert result.output == expected_help_text


def test_init_help(cli_runner: CliRunner):
    expected_help_text = """\
Usage: init [OPTIONS]

  Instantiate the application environment and secret key.

Options:
  --help  Show this message and exit.
"""
    result = cli_runner.invoke(cli.init, ["--help"])

    assert result.exit_code == 0
    assert result.output == expected_help_text


@pytest.mark.usefixtures("patch_alembic_migration")
def test_init_with_secret_key(cli_runner: CliRunner):
    cli_runner.env = {"SECRET_KEY": "ALREADY-HAVE-A-KEY-SET"}
    result = cli_runner.invoke(cli.init, [])
    expected_output = """\
Secret key for application:
Key already found in your environment: `SECRET_KEY`

Migrating database to head:
patched migrations...
Successfully migrated to head.
"""

    assert result.exit_code == 0
    assert result.output == expected_output


@pytest.mark.skip(reason="Need to find a way to patch local dotenv file.")
@pytest.mark.usefixtures("patch_alembic_migration", "patch_generate_secret_token")
def test_init_without_secret_key(cli_runner: CliRunner):
    cli_runner.env = {"SECRET_KEY": None}
    result = cli_runner.invoke(cli.init, [])
    expected_output = """\
Secret key for application:
SECRET_KEY=PATCHED-KEY-123ABC
Copy and paste this into your `.env` file.

Migrating database to head:
patched migrations...
Successfully migrated to head.
"""

    assert result.exit_code == 0
    assert result.output == expected_output


def test_run_help(cli_runner: CliRunner):
    expected_help_text = """\
Usage: run [OPTIONS]

  Migrate database to latest version and launch application server.

Options:
  --host TEXT     Bind socket to this host.  [default: 127.0.0.1]
  --port INTEGER  Bind socket to this port.  [default: 8000]
  --help          Show this message and exit.
"""
    result = cli_runner.invoke(cli.run, ["--help"])

    assert result.exit_code == 0
    assert result.output == expected_help_text


@pytest.mark.usefixtures("patch_alembic_migration", "patch_uvicorn_server")
def test_run_with_defaults(cli_runner: CliRunner):
    result = cli_runner.invoke(cli.run, [])
    expected_output = """\
Migrating database to head:
patched migrations...
Successfully migrated to head.

Starting server...
patched server received the following params:
args: ('mychef.app:app',)
kwargs: {'host': '127.0.0.1', 'port': 8000, 'log_level': 'info'}
"""

    assert result.exit_code == 0
    assert result.output == expected_output
