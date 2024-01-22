import pytest

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


def test_add_round_key():
    # arranjo
    array = [
        ['6f', '7e', '59', '99'],
        ['68', '2c', 'b2', '20'],
        ['7d', 'ee', '5b', 'a6'],
        ['7d', 'ca', '54', '29']
    ]

    key = [
        ['a1', 'b2', 'c3', 'd4'],
        ['e5', 'f6', '07', '18'],
        ['09', '2a', '3b', '4c'],
        ['5d', '6e', '7f', '80']
    ]

    expected_output = [
        ['ce', 'cc', '9a', '4d'],
        ['8d', 'da', 'b5', '38'],
        ['74', 'c4', '60', 'ea'],
        ['20', 'a4', '2b', 'a9']
    ]

    # ação
    res = add_round_key(array, key)

    # asserção
    assert np.array_equal(res, expected_output)


def test_sub_byte():
    # arranjo
    input_array = [
        ['ce', 'cc', '9a', '4d'],
        ['8d', 'da', 'b5', '38'],
        ['74', 'c4', '60', 'ea'],
        ['20', 'a4', '2b', 'a9']
    ]

    s_box_mock = {
        'ce': '01', 'cc': '02', '9a': '03', '4d': '04',
        '8d': '05', 'da': '06', 'b5': '07', '38': '08',
        '74': '09', 'c4': '0a', '60': '0b', 'ea': '0c',
        '20': '0d', 'a4': '0e', '2b': '0f', 'a9': '10'
    }

    # Expected output after applying the sub_byte function
    expected_output = [
        ['01', '02', '03', '04'],
        ['05', '06', '07', '08'],
        ['09', '0a', '0b', '0c'],
        ['0d', '0e', '0f', '10']
    ]

    # ação
    sub_byte(input_array, s_box_mock)

    # asserção
    assert input_array == expected_output


def test_shift_rows():
    # arranjo
    input_array = [
        ['ce', 'cc', '9a', '4d'],
        ['8d', 'da', 'b5', '38'],
        ['74', 'c4', '60', 'ea'],
        ['20', 'a4', '2b', 'a9']
    ]
    # para n linhas, cada elemento é deslocado n-1 para a esquerda
    expected_output = [
        ['ce', 'cc', '9a', '4d'],
        ['da', 'b5', '38', '8d'],
        ['60', 'ea', '74', 'c4'],
        ['a9', '20', 'a4', '2b']
    ]

    # ação
    shift_rows(input_array)

    # asserção
    assert np.array_equal(input_array, expected_output)


def test_shift_rows_inv():
    # arranjo
    input_array = [
        ['ce', 'cc', '9a', '4d'],
        ['da', 'b5', '38', '8d'],
        ['60', 'ea', '74', 'c4'],
        ['a9', '20', 'a4', '2b']
    ]
    # para n linhas, cada elemento é deslocado n-1 para a direita
    expected_output = [
        ['ce', 'cc', '9a', '4d'],
        ['8d', 'da', 'b5', '38'],
        ['74', 'c4', '60', 'ea'],
        ['20', 'a4', '2b', 'a9']
    ]

    # ação
    shift_rows_inv(input_array)

    # asserção
    assert np.array_equal(input_array, expected_output)


def test_mix_columns():

    # arranjo
    array = [
        ['ce', 'cc', '9a', '4d'],
        ['8d', 'da', 'b5', '38'],
        ['74', 'c4', '60', 'ea'],
        ['20', 'a4', '2b', 'a9']
    ]

    expected_output = [
        ['5f', '96', 'a0', '91'],
        ['73', '90', '60', 'b1'],
        ['cb', '72', '92', '5a'],
        ['f0', '2', '36', '4c']
    ]

    # ação
    res = mix_columns(array)

    # asserção
    assert np.array_equal(res, expected_output)


def test_mix_columns_inv():
    # arranjo
    array = [
        ['ce', 'cc', '9a', '4d'],
        ['8d', 'da', 'b5', '38'],
        ['74', 'c4', '60', 'ea'],
        ['20', 'a4', '2b', 'a9']
    ]

    expected_output = [
        ['39', '2b', '68', '90'],
        ['49', 'ee', '23', '68'],
        ['ad', 'cf', '5a', '5b'],
        ['ca', '7c', '75', '95']
    ]

    # ação
    res = mix_columns_inv(array)

    # asserção
    assert np.array_equal(res, expected_output)


def test_e_verify_table_compatibility_subtraction():
    var = 0x100
    res = verify_e_table_compatibility(var)
    assert res == 3


def test_verify_e_table_compatibility_no_sub():
    var = 0xA3
    res = verify_e_table_compatibility(var)
    assert res == 100


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


def test_execute_encryption():
    # arranjo
    user_input = "Encrypt this message"
    encryption_key = "fUy7w8DunBVGct1q"

    # execução
    message = text_to_array(user_input)
    key = text_to_hex_array(encryption_key)
    key_final = key_expansion(key)

    cypher_txt = encrypt(message, key_final, s_box_map)

    decrypted_message = ''
    decryption_state = decrypt(cypher_txt, key_final, s_box_map_inv)
    for i in range(0, len(decryption_state)):
        for x in range(0, BYTE_SIZE):
            for y in range(0, BYTE_SIZE):
                # transforma os números hexadecimais em seus caracteres utf-8 correspondentes
                decryption_state[i][x][y] = bytes.fromhex(decryption_state[i][x][y]).decode('utf-8')
                decrypted_message = decrypted_message + decryption_state[i][x][y]

    # asserção
    assert decrypted_message == "Encrypt this message            "


def test_execute_encryption_long_key():
    # arranjo
    user_input = "Encrypt this message"
    encryption_key = "fUy7w8DunBVGct1qUchVYwaQ2"

    # execução
    message = text_to_array(user_input)
    key = text_to_hex_array(encryption_key)
    key_final = key_expansion(key)

    cypher_txt = encrypt(message, key_final, s_box_map)

    decrypted_message = ''
    decryption_state = decrypt(cypher_txt, key_final, s_box_map_inv)
    for i in range(0, len(decryption_state)):
        for x in range(0, BYTE_SIZE):
            for y in range(0, BYTE_SIZE):
                # transforma os números hexadecimais em seus caracteres utf-8 correspondentes
                decryption_state[i][x][y] = bytes.fromhex(decryption_state[i][x][y]).decode('utf-8')
                decrypted_message = decrypted_message + decryption_state[i][x][y]

    # asserção
    assert decrypted_message == "Encrypt this message            "


def test_short_key_handling():
    # arranjo
    encryption_key = "fUy7w8DunBVGct1"
    expected_error_message = "string index out of range"

    # execução
    with pytest.raises(IndexError) as excinfo:
        key = text_to_hex_array(encryption_key)

    # asserção
    assert str(excinfo.value) == expected_error_message


def test_invalid_char_input():
    # arranjo
    user_input = "Encrypt this messageÇ"
    encryption_key = "fUy7w8DunBVGct1q"
    expected_error_message = "'utf-8' codec can't decode byte 0xc7 in position 0: unexpected end of data"

    # execução
    message = text_to_array(user_input)
    key = text_to_hex_array(encryption_key)
    key_final = key_expansion(key)

    cypher_txt = encrypt(message, key_final, s_box_map)

    with pytest.raises(UnicodeDecodeError) as excinfo:
        decrypted_message = ''
        decryption_state = decrypt(cypher_txt, key_final, s_box_map_inv)
        for i in range(0, len(decryption_state)):
            for x in range(0, BYTE_SIZE):
                for y in range(0, BYTE_SIZE):
                    # transforma os números hexadecimais em seus caracteres utf-8 correspondentes
                    decryption_state[i][x][y] = bytes.fromhex(decryption_state[i][x][y]).decode('utf-8')
                    decrypted_message = decrypted_message + decryption_state[i][x][y]

    # asserção
    assert str(excinfo.value) == expected_error_message

