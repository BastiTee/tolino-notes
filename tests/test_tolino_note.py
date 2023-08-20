# -*- coding: utf-8 -*-
"""Test suite for tolino_note."""

from datetime import datetime

from tolino_notes.tolino_note import NoteType, TolinoNote


class TestCode:  # noqa: D101
    def test_no_content(self) -> None:  # noqa: D102
        assert not TolinoNote.from_unparsed_content('')
        assert not TolinoNote.from_unparsed_content(r'   ')

    def test_lang_de_marker_note(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """


The Goal: A Process of Ongoing Improvement (Goldratt, Eliyahu M.)
Markierung auf Seite 286: ""So why do you think ... failed?’’ I ask her.

  "Simple,’’ Bob jumps in. "They talked, we did.’’"
Hinzugefügt am 15.08.2023 | 18:00

-----------------------------------

"""
        )
        assert note
        assert note.note_type == NoteType.HIGHLIGHT
        assert note.note_lang == 'de'
        assert (
            note.book_title
            == 'The Goal: A Process of Ongoing Improvement (Goldratt, Eliyahu M.)'
        )  # noqa: E501
        assert note.created == datetime(2023, 8, 15, 18, 00)
        assert note.page == 286
        assert note.content.startswith('"So why do you')
        assert note.content.endswith('"They talked, we did."')

    def test_lang_en_marker_note(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """

Ender's Game (Card, Orson Scott)
Highlight on page 77: "Ender laughed. “I’ll set up a system for you.”
“Now?”
“Can I finish eating?”
“You never finish eating.”"
Added on 08/20/2023 | 7:48

-----------------------------------

"""
        )
        assert note
        assert note.note_type == NoteType.HIGHLIGHT
        assert note.note_lang == 'en'
        assert note.book_title == 'Ender\'s Game (Card, Orson Scott)'  # noqa: E501
        assert note.created == datetime(2023, 8, 20, 7, 48)
        assert note.page == 77
        assert note.content.startswith('Ender laughed.')
        assert note.content.endswith('You never finish eating."')

    def test_lang_es_marker_note(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """


Ender's Game (Card, Orson Scott)
Marcadores en la página 77: "got up and walked away from his bed.
“Ender,” said Alai.
Ender turned around. Alai was holding a little piece of paper.
“What is it?”
Alai looked up at him. “Don’t you know? This was on your bed. You "
Agregado el 20.08.2023 | 7:50

"""
        )
        assert note
        assert note.note_type == NoteType.HIGHLIGHT
        assert note.note_lang == 'es'
        assert note.book_title == 'Ender\'s Game (Card, Orson Scott)'  # noqa: E501
        assert note.created == datetime(2023, 8, 20, 7, 50)
        assert note.page == 77
        assert note.content.startswith('got up and walked away ')
        assert note.content.endswith('This was on your bed. You')
