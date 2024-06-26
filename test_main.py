import pytest

from main import *
from key_expansion import *
import numpy as np


class TestDataManipulation:
    @staticmethod
    def test_string_to_hex():
        res = string_to_hex('A')
        assert res == '41'

    @staticmethod
    @pytest.mark.parametrize("input_text, expected_output", [
        ("", []),  # input vazio
        ("Thats it", ["Thats it        "]),  # bloco incompleto
        ("Thats itThats it", ["Thats itThats it"]),  # bloco completo
        ("Thats itThats itThats it", ["Thats itThats it", "Thats it        "])  # dois blocos, um incompleto
    ])
    def test_text_to_array(input_text, expected_output):
        expected_output = text_to_array("")
        assert expected_output == []

    @staticmethod
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

    @staticmethod
    @pytest.mark.parametrize("input_string, expected_output", [
        ("B", "0B"),  # número incompleto
        ("10", "10")  # número completo - nenhuma ação necessária
    ])
    def test_force_two_digits(input_string, expected_output):
        output = force_two_digits(input_string)
        assert output == expected_output

    @staticmethod
    @pytest.mark.parametrize("var, expected_output", [
        (0x100, 3),
        (0xA3, 100)  # Valor com mais de 2 índices, deve ter o valor FF subtraído antes da conversão
    ])
    def test_verify_e_table_compatibility(var, expected_output):
        output = verify_e_table_compatibility(var)
        assert output == expected_output


class TestKeyExpansion:
    @staticmethod
    @pytest.mark.parametrize("input_key, expected_output", [
        (
            [
                ['2f', 'a3', 'b1', 'c4'],
                ['5d', '8e', '91', 'f2'],
                ['7c', 'd9', 'e0', '3a'],
                ['4b', '60', 'fc', '19']
            ],
            [
                ['2f', 'a3', 'b1', 'f2'],
                ['5d', '8e', '91', '3a'],
                ['7c', 'd9', 'e0', '19'],
                ['4b', '60', 'fc', 'c4']
            ]
        ),
        (
            [
                ['f6', '8d', '33', 'c'],
                ['5d', 'dd', 'f1', '0'],
                ['90', '82', 'ff', '1'],
                ['14', 'b1', 'b1', '1']
            ],
            [
                ['f6', '8d', '33', '00'],
                ['5d', 'dd', 'f1', '01'],
                ['90', '82', 'ff', '01'],
                ['14', 'b1', 'b1', '0c']
            ])
    ])
    def test_rot_word(input_key, expected_output):

        result = rot_word(input_key)
        # asserção - a última coluna deve ter seus elementos deslocados três casas avante

        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize("input_key, expected_output", [
        (
            [
                ['2f', 'a3', 'b1', '0f'],
                ['5d', '8e', '91', '01'],
                ['7c', 'd9', 'e0', '0a'],
                ['4b', '60', 'fc', '07']
            ],
            [
                ['2f', 'a3', 'b1', '76'],
                ['5d', '8e', '91', '7c'],
                ['7c', 'd9', 'e0', '67'],
                ['4b', '60', 'fc', 'c5']
            ]),

    ])
    def test_sub_word(input_key, expected_output):

        res = sub_word(input_key)

        # asserção - a ultima coluna deve apresentar os valores das substituições de s_box_map em tables.py
        assert res == expected_output

    @staticmethod
    @pytest.mark.parametrize("input_key, expected_output, iterations", [
        (
            [
                ['2f', 'a3', 'b1', '0f'],
                ['5d', '8e', '91', '01'],
                ['7c', 'd9', 'e0', '0a'],
                ['4b', '60', 'fc', '07']
            ],
            [
                ['2f', 'a3', 'b1', 'e'],
                ['5d', '8e', '91', '01'],
                ['7c', 'd9', 'e0', '0a'],
                ['4b', '60', 'fc', '07']
            ],
            1
        ),
        (
            [
                ['2f', 'a3', 'b1', '0f'],
                ['5d', '8e', '91', '01'],
                ['7c', 'd9', 'e0', '0a'],
                ['4b', '60', 'fc', '07']
            ],
            [
             ['2f', 'a3', 'b1', '1f'],
             ['5d', '8e', '91', '01'],
             ['7c', 'd9', 'e0', '0a'],
             ['4b', '60', 'fc', '07']
            ],
            5
        )

    ])
    def test_rcon(input_key, expected_output, iterations):

        res = rcon(input_key, iterations)

        assert res == expected_output

    @staticmethod
    @pytest.mark.parametrize("rcon_key, input_key, expected_output", [
        (
            [
                ['2f', 'a3', 'b1', 'c4'],
                ['5d', '8e', '91', 'f2'],
                ['7c', 'd9', 'e0', '3a'],
                ['4b', '60', 'fc', '19']
            ],
            [
                ['2f', 'a3', 'b1', 'e'],
                ['5d', '8e', '91', '01'],
                ['7c', 'd9', 'e0', '0a'],
                ['4b', '60', 'fc', '07']
            ],
            [
                ['eb', '48', 'f9', 'f7'],
                ['af', '21', 'b0', 'b1'],
                ['46', '9f', '7f', '75'],
                ['52', '32', 'ce', 'c9']
            ]
        ),
    ])
    def test_expansion_xor(rcon_key, input_key, expected_output):

        res = expansion_xor(rcon_key, input_key)

        assert res == expected_output

    @staticmethod
    @pytest.mark.parametrize("key, expected_output", [
        (
            [
                ['2f', 'a3', 'b1', 'c4'],
                ['5d', '8e', '91', 'f2'],
                ['7c', 'd9', 'e0', '3a'],
                ['4b', '60', 'fc', '19']
            ],
            [
                [
                    ['2f', 'a3', 'b1', 'c4'],
                    ['5d', '8e', '91', 'f2'],
                    ['7c', 'd9', 'e0', '3a'],
                    ['4b', '60', 'fc', '19']
                ],
                [
                    ['a7', '4', 'b5', '71'],
                    ['dd', '53', 'c2', '30'],
                    ['a8', '71', '91', 'ab'],
                    ['57', '37', 'cb', 'd2']
                ],
                [
                    ['a1', '2', 'b3', '77'],
                    ['bf', '31', 'a0', '52'],
                    ['1d', 'c4', '24', '1e'],
                    ['f4', '94', '68', '71']
                ],
                [
                    ['a5', '6', 'b7', '73'],
                    ['cd', '43', 'd2', '20'],
                    ['be', '67', '87', 'bd'],
                    ['1', '61', '9d', '84']
                ],
                [
                    ['1a', 'b9', '8', 'cc'],
                    ['b7', '39', 'a8', '5a'],
                    ['e1', '38', 'd8', 'e2'],
                    ['8e', 'ee', '12', 'b']],
                [
                    ['b4', '17', 'a6', '62'],
                    ['2f', 'a1', '30', 'c2'],
                    ['ca', '13', 'f3', 'c9'],
                    ['c5', 'a5', '59', '40']
                ],
                [
                    ['b1', '12', 'a3', '67'],
                    ['f2', '7c', 'ed', '1f'],
                    ['c3', '1a', 'fa', 'c0'],
                    ['6f', 'f', 'f3', 'ea']
                ],
                [
                    ['31', '92', '23', 'e7'],
                    ['48', 'c6', '57', 'a5'],
                    ['44', '9d', '7d', '47'],
                    ['ea', '8a', '76', '6f']
                ],
                [
                    ['b7', '14', 'a5', '61'],
                    ['e8', '66', 'f7', '5'],
                    ['ec', '35', 'd5', 'ef'],
                    ['7e', '1e', 'e2', 'fb']
                ],
                [
                    ['c7', '64', 'd5', '11'],
                    ['37', 'b9', '28', 'da'],
                    ['e3', '3a', 'da', 'e0'],
                    ['91', 'f1', 'd', '14']
                ],
                [
                    ['a6', '5', 'b4', '70'],
                    ['d6', '58', 'c9', '3b'],
                    ['19', 'c0', '20', '1a'],
                    ['13', '73', '8f', '96']
                ]
            ]
        ),
    ])
    def test_key_expansion(key, expected_output):
        result = key_expansion(key)
        assert result == expected_output


class TestCryptographyRounds:
    @staticmethod
    def test_add_round_key():
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

        res = add_round_key(array, key)

        # asserção - resultado após a adição da round key
        assert np.array_equal(res, expected_output)

    @staticmethod
    def test_sub_byte():
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

        expected_output = [
            ['01', '02', '03', '04'],
            ['05', '06', '07', '08'],
            ['09', '0a', '0b', '0c'],
            ['0d', '0e', '0f', '10']
        ]

        sub_byte(input_array, s_box_mock)

        # asserção - resultado após a substituição de bytes através da s_box
        assert input_array == expected_output

    @staticmethod
    def test_shift_rows():
        # arranjo
        input_array = [
            ['ce', 'cc', '9a', '4d'],
            ['8d', 'da', 'b5', '38'],
            ['74', 'c4', '60', 'ea'],
            ['20', 'a4', '2b', 'a9']
        ]

        expected_output = [
            ['ce', 'cc', '9a', '4d'],
            ['da', 'b5', '38', '8d'],
            ['60', 'ea', '74', 'c4'],
            ['a9', '20', 'a4', '2b']
        ]

        # ação
        shift_rows(input_array)

        # asserção - para n linhas, cada elemento é deslocado n-1 para a esquerda
        assert np.array_equal(input_array, expected_output)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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


class TestEncryptionProcess:
    @staticmethod
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

    @staticmethod
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

        # asserção - a mensagem deve permanecer igual no inicio porém com uma quantidade de caracteres múltipla de 16
        assert decrypted_message == "This message shouldn't be visible               "

    @staticmethod
    # teste com chave de criptografia com menos de 16 bytes
    def test_short_key_handling():
        # arranjo
        encryption_key = "fUy7w8DunBVGct1"
        expected_error_message = "string index out of range"

        # execução
        with pytest.raises(IndexError) as excinfo:
            key = text_to_hex_array(encryption_key)

        # asserção - retorna erro pois a chave de criptografia é muito pequena
        assert str(excinfo.value) == expected_error_message

    @staticmethod
    # teste com caracter inválido na mensagem de input
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

        # asserção - erro causado por caracter inválido na mensagem
        assert str(excinfo.value) == expected_error_message


# testes end-to-end
class TestEndToEndEncryption:
    @staticmethod
    @pytest.mark.parametrize("user_input, encryption_key, expected_decrypted_message", [
        ("Encrypt this message", "fUy7w8DunBVGct1q", "Encrypt this message            "),
        # teste com chave de criptografia que não preenche dois blocos de 16 bytes totalmente
        ("Another message", "fUy7w8DunBVGct1qUchVYwaQ2", "Another message "),
    ])
    def test_execute_encryption(user_input, encryption_key, expected_decrypted_message):

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

        # asserção - a mensagem deve permanecer igual no inicio porém com uma quantidade de caracteres múltipla de 16
        assert decrypted_message == expected_decrypted_message
