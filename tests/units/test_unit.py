from cmder import unit
from cmder.data import pyoptions


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
