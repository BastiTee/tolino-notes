# -*- coding: utf-8 -*-
"""Tolino note parser."""

import logging as log
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple

SUPPORTED_LANGUAGES = {
    'en': {
        'cdate_prefix': r'^Added on ',
        'marker_prefix': r'Highlight on page ',
        'date_format': r'%m/%d/%Y %H:%M',
    },
    'de': {
        'cdate_prefix': r'^Hinzugefügt am ',
        'marker_prefix': r'^Markierung auf Seite ',
        'date_format': r'%d.%m.%Y %H:%M',
    },
    'es': {
        'cdate_prefix': r'^Agregado el ',
        'marker_prefix': r'^Marcadores en la página ',
        'date_format': r'%d.%m.%Y %H:%M',
    },
}


class NoteType(Enum):
    """Type of Tolino notes."""

    HIGHLIGHT = 1
    NOTE = 2
    BOOKMARK = 3


@dataclass
class TolinoNote:
    """Class for keeping track of a Tolino note."""

    note_type: NoteType
    note_lang: str
    book_title: str
    page: int
    content: str
    created: datetime

    @staticmethod
    def __get_language(hint: str) -> Optional[Tuple[dict, str]]:
        for lang in SUPPORTED_LANGUAGES.keys():
            cdate_prefix = SUPPORTED_LANGUAGES[lang]['cdate_prefix']
            if re.match(cdate_prefix + '.*', hint):
                return SUPPORTED_LANGUAGES[lang], lang
        return None

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

        book_title = cn.pop(0).strip()

        # Detect language by reading the creation date prefix
        cdate_line = cn.pop(len(cn) - 1)
        lang_id = TolinoNote.__get_language(cdate_line)
        if not lang_id:
            log.warn(f'Unsupported language for note: {unparsed_content}')
            return None
        lang_dict = lang_id[0]

        cdate = re.sub(lang_dict['cdate_prefix'], '', cdate_line)
        cdate = re.sub(r'\s\|\s', ' ', cdate)
        cdate_parsed = datetime.strptime(cdate, lang_dict['date_format'])

        full_text = '\n'.join(cn)

        location = re.sub('-[0-9]+$', '', full_text.split(r': ', maxsplit=1)[0])
        if not re.match(lang_dict['marker_prefix'], location):
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

        return TolinoNote(
            NoteType.HIGHLIGHT, lang_id[1], book_title, page, content, cdate_parsed
        )
