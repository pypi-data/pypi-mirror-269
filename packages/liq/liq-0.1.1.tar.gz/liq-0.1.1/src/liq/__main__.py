from pathlib import Path

import click

from . import run_liq
from ._version import __version__

QTEAL = click.style("Q", fg="cyan") + click.style("teal", fg="bright_black")
LOGO = f"""
.-.   .-..---.  {QTEAL}
| |__ | || O ,  {click.style('fixing systems, not people', fg='bright_black')}
`----'`-'`-'\\\\  v{__version__}
""".strip()

HELP = f"""\b
Limit the quality of JPG images.
When running with --fix it will overwrite the file(s) in question.
{click.style("No backups are made. This is a potentially destructive operation!", bold=True, blink=True)}
Exits with 1 if any files where/would have been changed.
"""


@click.command(
    context_settings={
        # Help is still wrapped to terminal width, but ignore the 80 char default max.
        "max_content_width": 1000,
    },
    help="\b\n" + LOGO + "\n" + HELP,
)
@click.version_option(__version__)
@click.option("-q", "--quality", type=click.IntRange(min=0, max=100), default=75, show_default=True)
@click.option("--fix/--no-fix", is_flag=True, default=False, show_default=True)
@click.option("-v", "--verbose", is_flag=True, default=False, help="log the detected quality of every image")
@click.argument("paths", type=click.Path(path_type=Path, exists=True, file_okay=True, dir_okay=False), nargs=-1, required=True)
def main(quality: int, fix: bool, verbose: bool, paths: tuple[Path]):
    changes = False
    # can't use any or all builtins because they short circuit
    for path in paths:
        changes = run_liq(quality, fix, verbose, path) or changes
    if changes:
        exit(1)


if __name__ == "__main__":
    main()
