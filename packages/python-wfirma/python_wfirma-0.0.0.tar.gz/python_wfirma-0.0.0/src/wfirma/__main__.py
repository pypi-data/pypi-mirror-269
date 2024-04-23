"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """WFirma."""


if __name__ == "__main__":
    main(prog_name="python-wfirma")  # pragma: no cover
