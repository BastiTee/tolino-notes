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
        assert note.cdate == datetime(2023, 8, 15, 18, 00)
        assert note.page == 286
        assert note.content
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
        assert note.cdate == datetime(2023, 8, 20, 7, 48)
        assert note.page == 77
        assert note.content
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
        assert note.cdate == datetime(2023, 8, 20, 7, 50)
        assert note.page == 77
        assert note.content
        assert note.content.startswith('got up and walked away ')
        assert note.content.endswith('This was on your bed. You')

    def test_lang_de_noted_note_1(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """

Ender’s Game (Card, Orson Scott)
Nota en la página 78: Note in Spanish.
"On impulse Ender hugged him, tight, almost as if he were Valentine. "
Agregado el 20.08.2023 | 7:50

------
    """
        )
        assert note
        assert note.note_type == NoteType.NOTE
        assert note.note_lang == 'es'
        assert note.book_title == 'Ender\'s Game (Card, Orson Scott)'  # noqa: E501
        assert note.cdate == datetime(2023, 8, 20, 7, 50)
        assert note.page == 78
        assert note.content
        assert note.content.startswith('On impulse Ender hugged him')
        assert note.content.endswith('as if he were Valentine.')
        assert note.user_notes
        assert note.user_notes == 'Note in Spanish.'

    def test_lang_de_noted_note_2(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """
Ender’s Game (Card, Orson Scott)
Notiz auf Seite 99: Let's make a long multi line comment.


And even include quotes like "this"
"“Colonel Graff, Either random distribution of stars, or symmetrical.”
“Fairness is a wonderful attribute, Major Anderson. It has nothing to do with war.”
“The game will be compromised. The comparative standings will become meaningless.”
“Alas.”"
Hinzugefügt am 20.08.2023 | 14:42

    """
        )
        assert note
        assert note.note_type == NoteType.NOTE
        assert note.note_lang == 'de'
        assert note.book_title == 'Ender\'s Game (Card, Orson Scott)'  # noqa: E501
        assert note.cdate == datetime(2023, 8, 20, 14, 42)
        assert note.page == 99
        assert note.content
        assert note.content.startswith('"Colonel Graff, Either random')
        assert note.content.endswith('Alas."')
        assert note.user_notes
        assert note.user_notes.startswith('Let\'s make a long multi')
        assert note.user_notes.endswith('quotes like "this"')

    def test_lang_de_noted_note_3(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """

Ender’s Game (Card, Orson Scott)
Notiz auf Seite 99: Test Note
"Double quotes" at beginning.
"Then run the simulations and see which ones are hardest, which easiest. "
Hinzugefügt am 20.08.2023 | 15:46

-----------------------------------


    """
        )
        assert note
        assert note.note_type == NoteType.NOTE
        assert note.note_lang == 'de'
        assert note.book_title == 'Ender\'s Game (Card, Orson Scott)'  # noqa: E501
        assert note.cdate == datetime(2023, 8, 20, 15, 46)
        assert note.page == 99
        assert note.content
        assert note.content.startswith('Then run the simulations')
        assert note.content.endswith(', which easiest.')
        assert note.user_notes
        assert note.user_notes.startswith('Test Note')
        assert note.user_notes.endswith('quotes" at beginning.')

    def test_issue_dkuester_github_3(self) -> None:  # noqa: D102
        note = TolinoNote.from_unparsed_content(
            """Miss Merkel (Safier, David)
Markierung"In diesem Moment realisierte Angela, dass sie zwar während ihrer ganzen
Regierungszeit...mals das Gefühl, das wirklich zu erleben"
Geändert am 21.08.2022 | 22:55"""
        )
        assert note
        assert note.note_type == NoteType.HIGHLIGHT
        assert note.note_lang == 'de'
        assert note.book_title == 'Miss Merkel (Safier, David)'  # noqa: E501
        assert note.cdate == datetime(2022, 8, 21, 22, 55)
        assert note.page == 0
        assert note.content
        assert note.content.startswith('In diesem Moment')
        assert note.content.endswith('das wirklich zu erleben')
