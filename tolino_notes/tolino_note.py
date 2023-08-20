# -*- coding: utf-8 -*-
"""Tolino note parser."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

SUPPORTED_LANGUAGES = {
    'de': {
        'added_prefix': r'^Hinzugefügt\sam\s',
        'marker_prefix': r'^Markierung\sauf\sSeite\s.*',
        'date_format': r'%d.%m.%Y %H:%M',
    }
}


@dataclass
class TolinoNote:
    """Class for keeping track of a Tolino note."""

    book_title: str
    page: int
    content: str
    created: datetime

    @staticmethod
    def from_unparsed_content(
        unparsed_content: str, language: str
    ) -> Optional['TolinoNote']:
        """Convert a note block from original Tolino file to note object."""
        lang: dict = SUPPORTED_LANGUAGES[language]
        cn = unparsed_content.strip().split('\n')

        book_title = cn.pop(0).strip()

        created = re.sub(lang['added_prefix'], '', cn.pop(len(cn) - 1))
        created = re.sub(r'\s\|\s', ' ', created)
        created_parsed = datetime.strptime(created, lang['date_format'])

        full_text = '\n'.join(cn)

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

        return TolinoNote(book_title, page, content, created_parsed)
