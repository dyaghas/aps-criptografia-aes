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
    res = text_to_hex_array(input_string)
    expected_output = [
        ["54", "49", "74", "69"],
        ["65", "6e", "53", "6e"],
        ["73", "70", "74", "67"],
        ["74", "75", "72", "67"]
    ]
    assert np.array_equal(res, expected_output)


def test_encryption_functionality():

    # arranjo
    key = "A key that is used in cryptography"
    hex_key = text_to_hex_array(key)
    expanded_key = key_expansion(hex_key)
    input_string = "This message shouldn't be visible"
    input_array = text_to_array(input_string)

    # ação
    encrypted_msg = encrypt(input_array, expanded_key, s_box_map)

    # asserção - a mensagem criptografada é retornada como um vetor de três dimensões
    expected_output = [
        [
            ['6f', '7e', '59', '99'],
            ['68', '2c', 'b2', '20'],
            ['7d', 'ee', '5b', 'a6'],
            ['7d', 'ca', '54', '29']
        ],
        [
            ['62', '91', '99', 'e5'],
            ['97', '30', '9d', '7b'],
            ['e8', '70', '74', '98'],
            ['93', '0c', 'ec', '82']
        ],
        [
            ['3f', '57', 'af', '56'],
            ['66', 'f0', '3c', '4a'],
            ['3d', '28', 'ad', 'fa'],
            ['71', '0d', '20', '1b']
        ]
    ]
    assert np.array_equal(encrypted_msg, expected_output)


def test_decryption_functionality():

    # arranjo
    key = "A key that is used in cryptography"
    hex_key = text_to_hex_array(key)
    expanded_key = key_expansion(hex_key)
    encrypted_msg = [
        [
            ['6f', '7e', '59', '99'],
            ['68', '2c', 'b2', '20'],
            ['7d', 'ee', '5b', 'a6'],
            ['7d', 'ca', '54', '29']
        ],
        [
            ['62', '91', '99', 'e5'],
            ['97', '30', '9d', '7b'],
            ['e8', '70', '74', '98'],
            ['93', '0c', 'ec', '82']
        ],
        [
            ['3f', '57', 'af', '56'],
            ['66', 'f0', '3c', '4a'],
            ['3d', '28', 'ad', 'fa'],
            ['71', '0d', '20', '1b']
        ]
    ]
    decrypted_message = ''

    # ação
    decryption_state = decrypt(encrypted_msg, expanded_key, s_box_map_inv)
    for i in range(0, len(decryption_state)):
        for x in range(0, BYTE_SIZE):
            for y in range(0, BYTE_SIZE):
                # transforma os números hexadecimais em seus caracteres utf-8 correspondentes
                decryption_state[i][x][y] = bytes.fromhex(decryption_state[i][x][y]).decode('utf-8')
                decrypted_message = decrypted_message + decryption_state[i][x][y]

    # asserção
    assert decrypted_message == "This message shouldn't be visible               "

