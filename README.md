# Tolino Notes

> Convert Tolino notes into useful formats

Tolino stores your highlights and notes in a `notes.txt` file on your device. However the format of that file is neither human- nor computer-readable. This project tries to close the gap by parsing the file (somehow) and convert it to a structured file – one per book in your `notes.txt`.

How to get the file?

- Connect your Tolino to your computer via USB.
- Use a file manager (Finder or Explorer) and open the root directory of the device.
- Look for the `notes.txt` file.

## Install and use

Install using pip / poetry or similar [from PyPi](https://pypi.org/project/tolino-notes/).

```shell
$ python -m pip install tolino-notes
```

In a new shell run:

```shell
$ tolino-notes --help
Usage: tolino-notes [OPTIONS]

  Convert Tolino notes into useful formats

Options:
  -i, --input-file FILE       Original Tolino notes file  [required]
  -o, --output-dir DIRECTORY  Folder for output files  [required]
  -f, --format [md|json]      Output format  [required]
  -v, --verbose               Verbose output
  --help                      Show this message and exit.
```

For example to convert all your notes to markdown run:

```shell
$ mkdir output-dir
$ tolino-notes -i notes.txt -o output-dir -f md
```

## Status

- Successfully tested with Tolino Shine 3
- Supports extraction and conversion of highlights, bookmarks and notes
- Support for DE, EN and ES language settings
- Supported output formats are Markdown and JSON

## Development

- Run `make` to create a new virtual environment
- Use the [issue tracker](https://github.com/BastiTee/tolino-notes/issues) to let me know about ideas and issues

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).
