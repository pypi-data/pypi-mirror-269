import subprocess


def test_script_help():
    result = subprocess.run(
        ["coverage", "run", "-m", "cligenius_cli", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Cligenius CLI version:" in result.stdout
