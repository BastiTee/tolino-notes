# -*- coding: utf-8 -*-
"""Module main-file."""

import argparse
import re
from collections import namedtuple
from datetime import datetime
from os import path
from typing import IO, Optional

TolinoNote = namedtuple('TolinoNote', 'book page content created')


def main(input_file: str, output_dir: str) -> None:  # noqa: D103
    with open(input_file, 'r') as fh:
        raw_notes = [line.strip() for line in fh.readlines() if line.strip()]

    raw_notes = re.split(r'\n\-{10,}\n?', '\n'.join(raw_notes))

    notes: dict = {}
    for raw in raw_notes:
        if not raw:
            continue
        opt_note = __convert_note(raw)
        if opt_note:
            book_notes = notes.get(opt_note.book, [])
            book_notes.append(opt_note)
            notes[opt_note.book] = book_notes

    for book in notes.keys():
        fname = path.join(
            output_dir,
            re.sub(r'[^a-z0-9äöü-]+', ' ', book.lower()).strip().replace(' ', '-')
            + '.md',
        )
        fh = open(fname, 'w+')

        def write_io(note: TolinoNote, fh: IO) -> None:
            line = f'{note.content} (p. {note.page})'
            fh.write(line + '\n\n')

        print(f'Converting "{book}" to {fname}')

        fh.write(f'# {book}\n\n')
        for n in sorted(notes.get(book, []), key=lambda x: x.page):
            write_io(n, fh)

        fh.close()


def __convert_note(raw: str) -> Optional[TolinoNote]:
    n = raw.split('\n')
    book = n.pop(0).strip()
    # Disclaimer: The 'am' part is language dependend de_DE
    created = re.sub(r'.*\sam\s', '', n.pop(len(n) - 1))
    created = re.sub(r'\s\|\s', ' ', created)
    created_parsed = datetime.strptime(created, r'%d.%m.%Y %H:%M')

    full_text = '\n'.join(n)

    location = re.sub('-[0-9]+$', '', full_text.split(': ', maxsplit=1)[0])
    # Disclaimer: The 'Markierung' is language dependend de_DE
    if 'Markierung' not in location:
        return None

    page = int(re.sub(r'\s', ' ', location).split(' ')[-1])

    content = ' '.join(
        [
            re.sub(r'\s', ' ', li.strip()).strip()
            for li in full_text.split(': ', maxsplit=1)[1:]
        ]
    )
    for rep in [
        (r'^"\s*', ''),
        (r'\s*"$', ''),
        (r'[“”«»]', '"'),
        (r'\u2019', '\''),
        (r'\s', ' '),
        (r'…', '...'),
    ]:
        content = re.sub(rep[0], rep[1], content)

    return TolinoNote(book, page, content, created_parsed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file', type=str, help='Input Tolino notes file', required=True
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory for Markdown files',
        required=True,
    )
    args = parser.parse_args()
    if not path.isfile(args.input_file):
        print(f'Input file {args.input_file} is not a file!')
        exit(1)
    if not path.isdir(args.output_dir):
        print(f'Output dir {args.output_dir} is not a directory!')
        exit(1)
    main(args.input_file, args.output_dir)
