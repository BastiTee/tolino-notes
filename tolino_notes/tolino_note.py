# -*- coding: utf-8 -*-
"""Tolino note parser."""

import logging as log
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple

LANGS = {
    'en': {
        'cdate_prefix': r'^Added on ',
        'cdate_changed_prefix': r'^Changed on ',
        'highlight_prefix': r'Highlight on page ',
        'note_prefix': r'^Note on page ',
        'bookmark_prefix': r'^Bookmark on page ',
        'date_format': r'%m/%d/%Y %H:%M',
    },
    'de': {
        'cdate_prefix': r'^Hinzugefügt am ',
        'cdate_changed_prefix': r'^Geändert am ',
        'highlight_prefix': r'^Markierung auf Seite ',
        'note_prefix': r'^Notiz auf Seite ',
        'bookmark_prefix': r'^Lesezeichen auf Seite ',
        'date_format': r'%d.%m.%Y %H:%M',
    },
    'es': {
        'cdate_prefix': r'^Agregado el ',
        'cdate_changed_prefix': r'^Modificado el ',
        'highlight_prefix': r'^Marcadores en la página ',
        'note_prefix': r'^Nota en la página ',
        'bookmark_prefix': r'^Selección en la página ',
        'date_format': r'%d.%m.%Y %H:%M',
    },
}
JSON_DATE_FORMAT = r'%d.%m.%Y %H:%M'


class NoteType(Enum):
    """Type of Tolino notes."""

    HIGHLIGHT = 1
    NOTE = 2
    BOOKMARK = 3

    def __str__(self) -> str:  # noqa: D105
        return str(self.name)


@dataclass
class TolinoNote:
    """Class for keeping track of a Tolino note."""

    note_type: str
    note_lang: str
    book_title: str
    page: int
    cdate: str
    content: Optional[str]
    user_notes: Optional[str]

    @staticmethod
    def __get_language(hint: str) -> Optional[Tuple[dict, str]]:
        for lang in LANGS.keys():
            if re.match(LANGS[lang]['cdate_prefix'] + '.*', hint) or re.match(
                LANGS[lang]['cdate_changed_prefix'] + '.*', hint
            ):
                return LANGS[lang], lang
        return None

    @staticmethod
    def __clean_string(string: str) -> str:
        string = string.strip()
        for patt_repl in [
            (r'\s*"\s*$', ''),  # Trailing quotes
            (r'^\s*"\s*', ''),  # Leading quotes
            (r'[\u2018\u2019\u00b4`]', '\''),  # Special ticks ’‘´`
            (r'[“”«»]+', '"'),  # Unwanted quote types
            (r'\'{2}', '"'),  # Double-quotes made of single-quotes ''
            (r'\s', ' '),  # Whitespace characters
            (r'…', '...'),  # Special dashes
        ]:
            string = re.sub(patt_repl[0], patt_repl[1], string)
        return string

    @staticmethod
    def from_unparsed_content(unparsed_content: str) -> Optional['TolinoNote']:
        """Convert a note block from original Tolino file to note object."""
        if not unparsed_content:
            return None
        if not unparsed_content.strip():
            return None

        # Remove a variety of weird whitespaces
        unparsed_content = re.sub(
            r'[^\S\r\n]',  # = whitespace but not carriage return or newline
            ' ',
            unparsed_content,
        )

        # Break down unparsed content
        cn = [line.strip() for line in unparsed_content.strip().split('\n') if line]
        cn = [line for line in cn if not re.match(r'^[\-]+$', line)]

        # First line is the book title
        book_title = TolinoNote.__clean_string(cn.pop(0))

        # Last line is the creation date
        cdate_line = cn.pop(len(cn) - 1)

        # Detect language by reading the creation date prefix
        lang_id = TolinoNote.__get_language(cdate_line)
        if not lang_id:
            log.warn(f'Unsupported language for note: {unparsed_content}')
            return None
        lang_dict = lang_id[0]

        # Format the creation date
        cdate = re.sub(lang_dict['cdate_prefix'], '', cdate_line)
        cdate = re.sub(lang_dict['cdate_changed_prefix'], '', cdate)
        cdate = re.sub(r'\s\|\s', ' ', cdate)
        cdate_parsed = datetime.strftime(
            datetime.strptime(cdate, lang_dict['date_format']), JSON_DATE_FORMAT
        )

        # Remaining content is the note itself
        full_text = '\n'.join(cn)
        full_text_split = full_text.split(r': ', maxsplit=1)

        prefix = re.sub('-[0-9]+$', '', full_text_split[0])
        page = int(re.sub(r'\s', ' ', prefix).split(' ')[-1])

        if re.match(lang_dict['bookmark_prefix'] + r'.*', prefix):
            # Bookmarks only have arbitrary content so we don't provide it.
            return TolinoNote(
                NoteType.BOOKMARK.name,
                lang_id[1],
                book_title,
                page,
                cdate_parsed,
                None,
                None,
            )
        elif re.match(lang_dict['highlight_prefix'] + r'.*', prefix):
            # For highlights the entire content is what the user highlighted
            content = TolinoNote.__clean_string(
                ' '.join(
                    [
                        re.sub(r'\s', ' ', li.strip()).strip()
                        for li in full_text_split[1:]
                    ]
                )
            )
            return TolinoNote(
                NoteType.HIGHLIGHT.name,
                lang_id[1],
                book_title,
                page,
                cdate_parsed,
                content,
                None,
            )
        elif re.match(lang_dict['note_prefix'] + r'.*', prefix):
            # For notes it's really bad as we can only guess what the user
            # wrote and what is marked. Only quotes can guide here.
            fts = ''.join(full_text_split[1:])
            # Best guess: Begin of the book highlight is the last quote
            # preceeded by a line break. ¯\_(ツ)_/¯
            user_notes = '\n"'.join(fts.split('\n"')[:-1])
            user_notes = TolinoNote.__clean_string(re.sub(r'\s', ' ', user_notes))
            # Before that is what the user wrote
            highlight = '\n"'.join(fts.split('\n"')[-1:])
            highlight = TolinoNote.__clean_string(re.sub(r'\s', ' ', highlight))
            return TolinoNote(
                NoteType.NOTE.name,
                lang_id[1],
                book_title,
                page,
                cdate_parsed,
                highlight,
                user_notes,
            )
        else:
            log.warn(f'Unparsable content type: {unparsed_content}')
            return None
