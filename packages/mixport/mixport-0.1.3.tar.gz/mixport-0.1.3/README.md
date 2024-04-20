# Mixport

[![PyPI](https://img.shields.io/pypi/v/mixport)](https://pypi.org/project/mixport)
[![Typecheck](https://github.com/fwcd/mixport/actions/workflows/typecheck.yml/badge.svg)](https://github.com/fwcd/mixport/actions/workflows/typecheck.yml)

CLI tool for transcoding Mixxx recordings.

## Usage

Transcoding the latest recording in `~/Music/Mixxx/Recordings` as Opus to the given directory:

```sh
mixport -o <path/to/outdir>
```

Transcoding a specific recording:

```
mixport -o <path/to/outdir> <path/to/cuefile>
```

For a more detailed overview, see

```sh
mixport --help
```
