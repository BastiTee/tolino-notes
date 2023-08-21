# -*- coding: utf-8 -*-
"""Writing options for notes."""

import json
from typing import IO, List

from tolino_notes.tolino_note import NoteType, TolinoNote


def write_to_markdown(notes: List[TolinoNote], output_file: str) -> None:
    """Write notes to Markdown file."""
    non_bookmarks = len([tn for tn in notes if tn.note_type != NoteType.BOOKMARK.name])
    if non_bookmarks == 0:
        return
    notes_sorted = sorted(notes, key=lambda x: x.page)
    book = notes_sorted[0].book_title

    def write_io(note: TolinoNote, fh: IO) -> None:
        if n.note_type == NoteType.BOOKMARK.name:
            return
        line = f'{note.content} (p. {note.page})'
        if n.note_type == NoteType.NOTE.name:
            fh.write(line + '\n')
            fh.write(f'> {n.user_notes}\n\n')
        else:
            fh.write(f'{line}\n\n')

    with open(output_file, 'w+') as fh:
        fh.write(f'# {book}\n\n')
        for n in notes_sorted:
            write_io(n, fh)


def write_to_json(notes: List[TolinoNote], output_file: str) -> None:
    """Write notes to JSON file."""
    notes_sorted = sorted(notes, key=lambda x: x.page)
    data = []
    for n in notes_sorted:
        data.append(n.__dict__)
    with open(output_file, 'w+') as fh:
        json.dump(data, fh, indent=2)
