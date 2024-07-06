import os

from click.testing import CliRunner

import munge.cli

this_dir = os.path.dirname(__file__)
data_dir = os.path.join(this_dir, "data")


def test_cli():
    runner = CliRunner()
    rv = runner.invoke(munge.cli.main, [])
    assert 2 == rv.exit_code

    rv = runner.invoke(munge.cli.main, ["--list-codecs"])
    assert 0 == rv.exit_code

    rv = runner.invoke(munge.cli.main, [os.path.join(data_dir, "dict0.toml"), "json:"])
    assert 0 == rv.exit_code
