# Tolino Notes

> Convert Tolino notes into useful formats

![PyPI](https://img.shields.io/pypi/v/tolino-notes)

![Tolino](GFX-SOCIAL.jpg)

Tolino stores your highlights and notes in a `notes.txt` file on your device. However that file has a strange structure and mixes books when you read multiple ones at a time. And the content depends on the language-setting of your device.

This project tries to close the gap by doing the heavy-lifting of parsing the file, sorting and converting to a commonly used format such as Markdown or JSON. – one file per book found in your `notes.txt`.

Where do I find this file?

- Connect your Tolino to your computer via USB.
- Use a file manager (Explorer, Finder, etc.) and open the root directory of the device.
- Look for the `notes.txt` file.

## Install and use

This is a Python program. Install it using `pip` / `poetry` or similar [from PyPi](https://pypi.org/project/tolino-notes/). If you don't yet have `pip` installed, [go here first](https://pip.pypa.io/en/stable/).

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
$ tolino-notes --input-file notes.txt --output-dir output-dir --format md
```

## Status

- Successfully in use with Tolino Shine 3.
- Supports extraction and conversion of highlights, bookmarks and notes.
- Support for DE, EN, ES, IT, NL, FR device-language settings, which is detected automatically.
- Supported output formats are Markdown and JSON.

Limitations:

Due to the unstructured nature of the `notes.txt`, it is a best-guess approach. The `notes.txt` format writes notes sequentially and it is not always clear in which order notes were taken. Also separating notes and highlights can only be done based on "quotes", which is not the most robust approach. In general, I believe 99% of your notes and highlights should be extracted properly.

Use the [issue tracker](https://github.com/BastiTee/tolino-notes/issues) to let me know about ideas and issues.

## Development

- The project is built based on [this](https://github.com/BastiTee/python-boilerplate) boilerplate.
- Run `make` to create a new virtual environment.

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).
