import os

from cmder import unit
from cmder.data import pyoptions, pypaths


def test_encode_base64():
    assert unit.encode_base64('hello') == 'aGVsbG8='


def test_decode_base64():
    assert unit.decode_base64('aGVsbG8=') == 'hello'


def test_encode_multi_line_note():
    file_string = 'Note\n# """this is note\nHello"""\n#desc: Note'
    encode_str = unit.encode_multi_line_notes(file_string)
    assert encode_str == 'Note\n# {}:dGhpcyBpcyBub3RlCkhlbGxv\n#desc: Note'.format(
        pyoptions.encode_flag)


def test_decode_multi_line_note():
    encode_str = '{}:dGhpcyBpcyBub3RlCkhlbGxv'.format(pyoptions.encode_flag)
    decode_str = unit.decode_multi_line_notes(encode_str)
    assert decode_str == 'this is note\nHello'


def test_get_db_path_list():
    history = ['a', 'b']
    assert unit.get_db_path_list(history) == [
        os.path.join(pypaths.db_path, 'a', 'b'),
        os.path.join(pypaths.custom_db_path, 'a', 'b')
    ]
