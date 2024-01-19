from main import *
from tables import *
from key_expansion import key_expansion
import numpy as np


# testes da função string_to_hex
def test_string_to_hex():
    res = string_to_hex('A')
    assert res == '41'


# testes da função text_to_block
def test_text_to_array_empty():
    res = text_to_array("")
    assert res == []


def test_text_to_array_incomplete():
    res = text_to_array("Thats it")
    assert res == ["Thats it        "]


def test_text_to_array_single():
    res = text_to_array("Thats itThats it")
    assert res == ["Thats itThats it"]


def test_text_to_array_multiple():
    res = text_to_array("Thats itThats itThats it")
    assert res == ["Thats itThats it", "Thats it        "]


def test_text_to_hex_array():
    input_string = "TestInputStringg"
    expected_output = [
        ["54", "49", "74", "69"],
        ["65", "6e", "53", "6e"],
        ["73", "70", "74", "67"],
        ["74", "75", "72", "67"]
    ]
    res = text_to_hex_array(input_string)
    assert np.array_equal(res, expected_output)


def test_encryption():
    key = "A key that is used in cryptography"
    hex_key = text_to_hex_array(key)
    expanded_key = key_expansion(hex_key)
    input_string = "This message shouldn't be visible"
    input_array = text_to_array(input_string)
    encrypted_msg = encrypt(input_array, expanded_key, s_box_map)
    res = encrypted_array_to_line(encrypted_msg)
    assert res == "6f7e5999682cb2207dee5ba67dca5429629199e597309d7be8707498930cec823f57af5666f03c4a3d28adfa710d201b"
