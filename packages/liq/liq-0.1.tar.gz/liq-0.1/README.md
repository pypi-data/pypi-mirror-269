# Limit Image Quality

```
.-.   .-..---.
| |__ | || O ,
`----'`-'`-'\\
```

Limit the quality of images in your repo via [pre-commit](https://pre-commit.com/).

## Disclaimer

**This tool does not make backups of files it changes.**

This tool uses ImageMagick's quality detection. This method is not flawless and based on internal metrics that may change.
This is why the recommended way to use this tool is via a Docker image with a fixed tag.
It's less likely the same image will get different results if the underlying ImageMagick version does not change.

## Usage

It's recommend to use pre-commit directly via the pre-build docker image we release.

### pre-commit

The intended use is via the provided hook in the repo:

```yaml
repos:
  # This repo <3
  - repo: https://gitlab.com/Qteal/oss/liq
    rev: main
    hooks:
      - id: limit-image-quality
        args: ['-q75']
```

Then run `pre-commit autoupdate` to transform the main rev into the latest release.

### Docker image

It's also possible to use the docker image directly.
The image is published to `registry.gitlab.com/qteal/oss/liq/liq`.

Every release gets a tag, `latest` is always up-to-date with the latest release.
You can also use branch name tags, so `main` is good for those living on the bleeding edge.

### Pip

The Python package is also push to the package registry of this repo (for all builds on main) and pypi (for releases).

Install via pip as `pip install liq`.

Run `liq --help` for more info.

You must install the required system dependencies of [Wand](https://docs.wand-py.org/en/latest/guide/install.html) yourself.

## Local Development

Only supported on Linux or something Linux like enough that I won't notice when you make a merge request.

If you want to work on this project, you need to have ImageMagic installed including the development libraries and headers.
It's recommended to follow the installation instructions in [Wand's documentation](https://docs.wand-py.org/en/latest/guide/install.html).

Use [Hatch](https://hatch.pypa.io/latest/) to set up the project environment.
