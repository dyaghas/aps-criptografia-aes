from main import *


# testes da função string_to_hex
def test_string_to_hex():
    res = string_to_hex('A')
    assert res == '41'


# testes da função text_to_block
def test_text_to_block_empty_block():
    res = text_to_block("")
    assert res == []


def test_text_to_block_incomplete_block():
    res = text_to_block("Thats it")
    assert res == ["Thats it        "]


def test_text_to_block_single_block():
    res = text_to_block("Thats itThats it")
    assert res == ["Thats itThats it"]


def test_text_to_block_multiple_blocks():
    res = text_to_block("Thats itThats itThats it")
    assert res == ["Thats itThats it", "Thats it        "]

