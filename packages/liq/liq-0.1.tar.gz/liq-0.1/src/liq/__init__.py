from pathlib import Path

import click

try:
    from wand.image import Image
except ModuleNotFoundError:
    raise
except ImportError as e:
    # Magic: If ImageMagick is not installed, try to use a docker container instead. This helps with running this on Daikin PCs.
    # Converting this hook to a Docker hook was also an option, but that requires Docker-in-Docker on Gitlab.
    click.secho("Cannot import wand. Did you install and configure ImageMagic?", fg="red", bold=True)
    raise SystemExit(2) from e


def run_liq(quality: int, fix: bool, verbose: bool, path: Path) -> bool:
    with Image(filename=path) as img:
        if img.compression_quality <= quality:
            if verbose:
                click.echo(f"{path}: Quality {img.compression_quality} <= {quality}. OK")
            return False
        click.echo(f"{path}: Quality {img.compression_quality} > {quality}. Not OK")
        if fix:
            img.compression_quality = quality
            img.save(filename=path)
        return True
