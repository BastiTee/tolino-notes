# -*- coding: utf-8 -*-
"""Module main-file."""

import json
import logging as log
import re
from os import path
from typing import IO

import click

from tolino_notes.tolino_note import SUPPORTED_LANGUAGES, TolinoNote

JSON_DATE_FORMAT = r'%d.%m.%Y %H:%M'


@click.command(help='Convert Tolino notes into useful formats')
@click.option(
    '--input-file',
    '-i',
    help='Original Tolino notes file',
    required=True,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
)
@click.option(
    '--output-dir',
    '-o',
    help='Folder for output files',
    required=True,
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
)
@click.option(
    '--language',
    '-l',
    help='Language setting of your Tolino',
    required=True,
    type=click.Choice(list(SUPPORTED_LANGUAGES.keys()), case_sensitive=False),
)
@click.option(
    '--format',
    '-f',
    'out_format',
    help='Output format',
    required=True,
    default='md',
    type=click.Choice(['md', 'json'], case_sensitive=False),
)
@click.option('--verbose', '-v', help='Verbose output', is_flag=True)
def main(  # noqa: D103
    input_file: str, output_dir: str, language: str, out_format: str, verbose: bool
) -> None:
    log.basicConfig(
        level=log.DEBUG if verbose else log.WARNING,
        format=r'[%(levelname)s] [%(asctime)s] %(message)s',
    )

    log.info('Read content of Tolino notes file...')
    with open(file=input_file, mode='r', encoding='utf-8') as fh:
        content = [line.strip() for line in fh.readlines() if line.strip()]
    raw_notes = re.split(  # Individual notes are separated by dashed lines
        r'\n\-{10,}\n?', '\n'.join(content)
    )
    raw_notes = [raw_note for raw_note in raw_notes if raw_note]

    log.info('Create a note object per raw note...')
    notes: dict = {}
    for raw in raw_notes:
        opt_note = TolinoNote.from_unparsed_content(raw, language)
        if opt_note:
            book_notes = notes.get(opt_note.book_title, [])
            book_notes.append(opt_note)
            notes[opt_note.book_title] = book_notes

    log.info('Write output per book...')
    for book in notes.keys():
        fname = path.join(
            output_dir,
            re.sub(r'[^a-z0-9äöü-]+', ' ', book.lower()).strip().replace(' ', '-')
            + '.'
            + out_format,
        )
        log.info(f'Writing notes of "{book}" to {fname}')
        fh = open(fname, 'w+')

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


if __name__ == '__main__':
    main()
