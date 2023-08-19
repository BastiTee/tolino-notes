# -*- coding: utf-8 -*-
"""Module main-file."""

import json
import re
from collections import namedtuple
from datetime import datetime
from os import path
from typing import IO, Optional

import click

TolinoNote = namedtuple('TolinoNote', 'book page content created')

LANGUAGES = {
    'de': {
        'added_prefix': r'^Hinzugefügt\sam\s',
        'date_format': r'%d.%m.%Y %H:%M',
        'marker_prefix': r'^Markierung\sauf\sSeite\s.*',
    }
}
JSON_DATE_FORMAT = r'%d.%m.%Y %H:%M'


@click.command(help='Convert Tolino notes into useful formats')
@click.option(
    '--input-file',
    '-i',
    help='Original Tolino notes file',
    required=True,
    metavar='PATH',
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
)
@click.option(
    '--output-dir',
    '-o',
    help='Folder for output files',
    required=True,
    metavar='PATH',
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
)
@click.option(
    '--language',
    '-l',
    help='Language setting of your Tolino',
    required=True,
    metavar='LANG',
    type=click.Choice(['de'], case_sensitive=False),
)
@click.option(
    '--format',
    '-f',
    'out_format',
    help='Output format',
    required=True,
    metavar='FORMAT',
    default='md',
    type=click.Choice(['md', 'json'], case_sensitive=False),
)
def main(  # noqa: D103
    input_file: str, output_dir: str, language: str, out_format: str
) -> None:
    # Read content of Tolino notes file
    with open(input_file, 'r') as fh:
        content = [line.strip() for line in fh.readlines() if line.strip()]

    # Individual notes are separated by dashed lines
    raw_notes = re.split(r'\n\-{10,}\n?', '\n'.join(content))
    raw_notes = [raw_note for raw_note in raw_notes if raw_note]

    # Create a note object per raw note
    notes: dict = {}
    for raw in raw_notes:
        opt_note = __raw_to_tolino_note(raw, language)
        if opt_note:
            book_notes = notes.get(opt_note.book, [])
            book_notes.append(opt_note)
            notes[opt_note.book] = book_notes

    # Write output per book
    for book in notes.keys():
        # Generate target filename
        fname = path.join(
            output_dir,
            re.sub(r'[^a-z0-9äöü-]+', ' ', book.lower()).strip().replace(' ', '-')
            + '.'
            + out_format,
        )
        print(f'Writing notes of "{book}" to {fname}')
        fh = open(fname, 'w+')

        # Get notes sorted by page
        notes_sorted = sorted(notes.get(book, []), key=lambda x: x.page)

        # Format output
        if out_format == 'md':

            def write_io(note: TolinoNote, fh: IO) -> None:
                line = f'{note.content} (p. {note.page})'
                fh.write(line + '\n\n')

            fh.write(f'# {book}\n\n')
            for n in notes_sorted:
                write_io(n, fh)
        elif out_format == 'json':
            data = {'book': book, 'notes': []}
            for n in notes_sorted:
                data['notes'].append(
                    {
                        'page': n.page,
                        'created': n.created.strftime(JSON_DATE_FORMAT),
                        'note': n.content,
                    }
                )
            json.dump(data, fh, indent=2)
        else:
            pass  # Prevented by cmd-line parser

        fh.close()


def __raw_to_tolino_note(raw: str, language: str) -> Optional[TolinoNote]:
    lang: dict = LANGUAGES[language]
    n = raw.strip().split('\n')

    book = n.pop(0).strip()

    created = re.sub(lang['added_prefix'], '', n.pop(len(n) - 1))
    created = re.sub(r'\s\|\s', ' ', created)
    created_parsed = datetime.strptime(created, lang['date_format'])

    full_text = '\n'.join(n)

    location = re.sub('-[0-9]+$', '', full_text.split(r': ', maxsplit=1)[0])
    if not re.match(lang['marker_prefix'], location):
        # E.g., ignoring bookmarks
        return None

    page = int(re.sub(r'\s', ' ', location).split(' ')[-1])

    content = ' '.join(
        [
            re.sub(r'\s', ' ', li.strip()).strip()
            for li in full_text.split(': ', maxsplit=1)[1:]
        ]
    )

    # Clean up content
    for rep in [
        (r'[\u2018\u2019\u00b4`]', '\''),  # Special ticks ’‘´`
        (r'[“”«»]+', '"'),  # Unwanted quote types
        (r'\'{2}', '"'),  # Double-quotes made of single-quotes ''
        (r'\s', ' '),  # Whitespace characters
        (r'…', '...'),  # Special dashes
        (r'\s*"\s*$', ''),  # Trailing quotes
        (r'^\s*"\s*', ''),  # Leading quotes
    ]:
        content = re.sub(rep[0], rep[1], content)

    return TolinoNote(book, page, content, created_parsed)


if __name__ == '__main__':
    main()
