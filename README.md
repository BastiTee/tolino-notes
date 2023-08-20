# Tolino Notes

> Convert Tolino notes into useful formats

Tolino stores your highlights and notes in a `notes.txt` file on your device. However the format of that file is neither human- nor computer-readable. This project tries to close the gap by parsing the file (somehow) and convert it to a structured file – one per book in your `notes.txt`.

How to get the file?

- Connect your Tolino to your computer via USB.
- Use a file manager (Finder or Explorer) and open the root directory of the device.
- Look for the `notes.txt` file.

## Install and use

Install using pip / poetry or similar from PyPi.

```shell
python -m pip install tolino_notes
```

## Status

- Successfully tested with Tolino Shine 3
- Supports extraction and conversion of highlights, bookmarks and notes
- Support for DE, EN and ES language settings
- Supported output formats are Markdown and JSON

## Limitation

Tolino stores all your highlights and notes in a file called notes.txt. That's cool, but they're sorted chronologically. It can be quite puzzling if you read several books in parallel. Notulator pulls the text snippets from each other and moves them to separate files: one per book. To convert your notes.txt:

Connect your tolino with USB to your computer. Navigate with the file manager of your computer (Finder or Explorer) to the root directory of your tolino. Drag the file 'notes' or 'notes.txt' to Notulator.

## Development

- Run `make` to create a new virtual environment

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).
