import numpy as np


# Funções


def convert_to_hex(var):
    var = format(ord(var), "02x")
    return var


def transpose(matrix_a, matrix_res):
    for a in range(4):
        for b in range(4):
            matrix_res[a][b] = matrix_a[b][a]


def to_hex_array(input_string):
    block_array = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]
    text_array = []
    x = 0
    y = 0
    for i in range(0, len(input_string)):
        if x < 4:
            block_array[y][x] = convert_to_hex(input_string[i])
            x += 1
        elif y < 3:
            x = 0
            y += 1
            block_array[y][x] = convert_to_hex(input_string[i])
            # Evita que a última letra de cada bloco dentro de block_array seja substituida pela primeira do bloco
            # seguinte
            x += 1
        # Transpõe o block_array e o coloca dentro do input_array.
        if (y == 3 and x == 4) or i == len(input_string) - 1:
            # ***
            block_array = np.transpose(block_array)
            # Atenção! transforma a array em 3D
            text_array.append(block_array.copy())
            x = 0
            y = 0
            block_array = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]
            continue
    print(f"hex: {text_array}")
    return text_array


def add_round_key(array, key):
    new_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(0, 4):
        for j in range(0, 4):
            # Adiciona a round key através de um XOR com o input
            new_array[i][j] = int(array[0][i][j], 16) ^ int(key[0][i][j], 16)
            new_array[i][j] = chr(new_array[i][j])
            new_array[i][j] = format(ord(str(new_array[i][j])), "x")
    print(f"round-key: {new_array}")
    return new_array


def sub_byte(array, s_box):
    for i in range(0, 4):
        for j in range(0, 4):
            # faz com que todos os números tenham duas casas, para possibilitar a comparação com as tabelas (ex: f = 0f)
            if len(array[i][j]) == 1:
                array[i][j] = int(array[i][j], 16)
                array[i][j] = format(array[i][j], "02x")
            # passa a array pela s-box
            array[i][j] = s_box[array[i][j]]
    print(f"sub-byte: {array}")


def sub_byte_inv(array, s_box_inv):
    for i in range(0, 4):
        for j in range(0, 4):
            array[i][j] = s_box_inv[array[i][j]]
    print(f"sub-byte-inv: {array}")


def shift_rows(array):
    offset = 0
    for i in range(1, 4):
        offset += 1
        array[i] = np.roll(array[i], -offset)
    print(f"shift rows: {array}")


def shift_rows_inv(array):
    offset = 0
    for i in range(1, 4):
        offset += 1
        array[i] = np.roll(array[i], offset)
    print(array)


def mix_columns(array):
    mult_matrix = [['02', '03', '01', '01'], ['01', '02', '03', '01'], ['01', '01', '02', '03'],
                   ['03', '01', '01', '02']]
    mix_state = [[0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00]]
    # For aninhado q passa por colunas ao invés de linhas
    for i in range(0, 4):
        for j in range(0, 4):
            a = int(l_table[array[0][i]], 16) + int(l_table[mult_matrix[j][0]], 16)
            a = verify_table_compatibility(a)
            a = int(e_table[f"{a:x}"], 16)
            b = int(l_table[array[1][i]], 16) + int(l_table[mult_matrix[j][1]], 16)
            b = verify_table_compatibility(b)
            b = int(e_table[f"{b:x}"], 16)
            c = int(l_table[array[2][i]], 16) + int(l_table[mult_matrix[j][2]], 16)
            c = verify_table_compatibility(c)
            c = int(e_table[f"{c:x}"], 16)
            d = int(l_table[array[3][i]], 16) + int(l_table[mult_matrix[j][3]], 16)
            d = verify_table_compatibility(d)
            d = int(e_table[f"{d:x}"], 16)
            mix_state[j][i] = a ^ b ^ c ^ d
    print(f"mix_state: {mix_state}")
    return mix_state


def verify_table_compatibility(var):
    # caso o número hexadecimal seja maior do que FF, deve-se subtrair FF de seu valor para que ele possa ser usado na
    # e_table e l_table.
    if len(f"{var:x}") > 2:
        var = var - 0xff
    return var


def encrypt(message, key, s_box):
    # Transforma a mensagem e a chave em hexadecimal de acordo com a tabela ASCII
    message = to_hex_array(message)
    key = to_hex_array(key)

    # Faz um XOR  entre a mensagem e a chave
    new_array = add_round_key(message, key)

    # Passa o resultado do passo anterior por uma S_box
    sub_byte(new_array, s_box)

    # Desloca as linhas do array com os passos 0, 1, 2 e 3 para cada linha, respectivamente
    shift_rows(new_array)

    mixed_state = mix_columns(new_array)


# Execução


user_input = "Two One Nine Two"
encryption_key = "Thats my Kung Fu"

# Rijndael S-box
s_box_map = {
    '00': '63', '01': '7c', '02': '77', '03': '7b', '04': 'f2', '05': '6b', '06': '6f', '07': 'c5', '08': '30',
    '09': '01', '0a': '67', '0b': '2b', '0c': 'fe', '0d': 'd7', '0e': 'ab', '0f': '76',  # linha 0
    '10': 'ca', '11': '82', '12': 'c9', '13': '7d', '14': 'fa', '15': '59', '16': '47', '17': 'f0', '18': 'ad',
    '19': 'd4', '1a': 'a2', '1b': 'af', '1c': '9c', '1d': 'a4', '1e': '72', '1f': 'c0',  # linha 1
    '20': 'b7', '21': 'fd', '22': '93', '23': '26', '24': '36', '25': '3f', '26': 'f7', '27': 'cc', '28': '34',
    '29': 'a5', '2a': 'e5', '2b': 'f1', '2c': '71', '2d': 'd8', '2e': '31', '2f': '15',  # linha 2
    '30': '04', '31': 'c7', '32': '23', '33': 'c3', '34': '18', '35': '96', '36': '05', '37': '9a', '38': '07',
    '39': '12', '3a': '80', '3b': 'e2', '3c': 'eb', '3d': '27', '3e': 'b2', '3f': '75',  # linha 3
    '40': '09', '41': '83', '42': '2c', '43': '1a', '44': '1b', '45': '6e', '46': '5a', '47': 'a0', '48': '52',
    '49': '3b', '4a': 'd6', '4b': 'b3', '4c': '29', '4d': 'e3', '4e': '2f', '4f': '84',  # linha 4
    '50': '53', '51': 'd1', '52': '00', '53': 'ed', '54': '20', '55': 'fc', '56': 'b1', '57': '5b', '58': '6a',
    '59': 'cb', '5a': 'be', '5b': '39', '5c': '4a', '5d': '4c', '5e': '58', '5f': 'cf',  # linha 5
    '60': 'd0', '61': 'ef', '62': 'aa', '63': 'fb', '64': '43', '65': '4d', '66': '33', '67': '85', '68': '45',
    '69': 'f9', '6a': '02', '6b': '7f', '6c': '50', '6d': '3c', '6e': '9f', '6f': 'a8',  # linha 6
    '70': '51', '71': 'a3', '72': '40', '73': '8f', '74': '92', '75': '9d', '76': '38', '77': 'f5', '78': 'bc',
    '79': 'b6', '7a': 'da', '7b': '21', '7c': '10', '7d': 'ff', '7e': 'f3', '7f': 'd2',  # linha 7
    '80': 'cd', '81': '0c', '82': '13', '83': 'ec', '84': '5f', '85': '97', '86': '44', '87': '17', '88': 'c4',
    '89': 'a7', '8a': '7e', '8b': '3d', '8c': '64', '8d': '5d', '8e': '19', '8f': '73',  # linha 8
    '90': '60', '91': '81', '92': '4f', '93': 'dc', '94': '22', '95': '2a', '96': '90', '97': '88', '98': '46',
    '99': 'ee', '9a': 'b8', '9b': '14', '9c': 'de', '9d': '5e', '9e': '0b', '9f': 'db',  # linha 9
    'a0': 'e0', 'a1': '32', 'a2': '3a', 'a3': '0a', 'a4': '49', 'a5': '06', 'a6': '24', 'a7': '5c', 'a8': 'c2',
    'a9': 'd3', 'aa': 'ac', 'ab': '62', 'ac': '91', 'ad': '95', 'ae': 'e4', 'af': '79',  # linha a
    'b0': 'e7', 'b1': 'c8', 'b2': '37', 'b3': '6d', 'b4': '8d', 'b5': 'd5', 'b6': '4e', 'b7': 'a9', 'b8': '6c',
    'b9': '56', 'ba': 'f4', 'bb': 'ea', 'bc': '65', 'bd': '7a', 'be': 'ae', 'bf': '08',  # linha b
    'c0': 'ba', 'c1': '78', 'c2': '25', 'c3': '2e', 'c4': '1c', 'c5': 'a6', 'c6': 'b4', 'c7': 'c6', 'c8': 'e8',
    'c9': 'dd', 'ca': '74', 'cb': '1f', 'cc': '4b', 'cd': 'bd', 'ce': '8b', 'cf': '8a',  # linha c
    'd0': '70', 'd1': '3e', 'd2': 'b5', 'd3': '66', 'd4': '48', 'd5': '03', 'd6': 'f6', 'd7': '0e', 'd8': '61',
    'd9': '35', 'da': '57', 'db': 'b9', 'dc': '86', 'dd': 'c1', 'de': '1d', 'df': '9e',  # linha d
    'e0': 'e1', 'e1': 'f8', 'e2': '98', 'e3': '11', 'e4': '69', 'e5': 'd9', 'e6': '8e', 'e7': '94', 'e8': '9b',
    'e9': '1e', 'ea': '87', 'eb': 'e9', 'ec': 'ce', 'ed': '55', 'ee': '28', 'ef': 'df',  # linha e
    'f0': '8c', 'f1': 'a1', 'f2': '89', 'f3': '0d', 'f4': 'bf', 'f5': 'e6', 'f6': '42', 'f7': '68', 'f8': '41',
    'f9': '99', 'fa': '2d', 'fb': '0f', 'fc': 'b0', 'fd': '54', 'fe': 'bb', 'ff': '16',  # linha f
}

s_box_map_inv = {
    '00': '52', '01': '09', '02': '6a', '03': 'd5', '04': '30', '05': '36', '06': 'a5', '07': '38', '08': 'bf',
    '09': '40', '0a': 'a3', '0b': '9e', '0c': '81', '0d': 'f3', '0e': 'd7', '0f': 'fb',  # linha 0
    '10': '7c', '11': 'e3', '12': '39', '13': '82', '14': '9b', '15': '2f', '16': 'ff', '17': '87', '18': '34',
    '19': '8e', '1a': '43', '1b': '44', '1c': 'c4', '1d': 'de', '1e': 'e9', '1f': 'cb',  # linha 1
    '20': '54', '21': '7b', '22': '94', '23': '32', '24': 'a6', '25': 'c2', '26': '23', '27': '3d', '28': 'ee',
    '29': '4c', '2a': '95', '2b': '0b', '2c': '42', '2d': 'fa', '2e': 'c3', '2f': '4e',  # linha 2
    '30': '08', '31': '2e', '32': 'a1', '33': '66', '34': '28', '35': 'd9', '36': '24', '37': 'b2', '38': '76',
    '39': '5b', '3a': 'a2', '3b': '49', '3c': '6d', '3d': '8b', '3e': 'd1', '3f': '25',  # linha 3
    '40': '72', '41': 'f8', '42': 'f6', '43': '64', '44': '86', '45': '68', '46': '98', '47': '16', '48': 'd4',
    '49': 'a4', '4a': '5c', '4b': 'cc', '4c': '5d', '4d': '65', '4e': 'b6', '4f': '92',  # linha 4
    '50': '6c', '51': '70', '52': '48', '53': '50', '54': 'fd', '55': 'ed', '56': 'b9', '57': 'da', '58': '5e',
    '59': '15', '5a': '46', '5b': '57', '5c': 'a7', '5d': '8d', '5e': '9d', '5f': '84',  # linha 5
    '60': '90', '61': 'd8', '62': 'ab', '63': '00', '64': '8c', '65': 'bc', '66': 'd3', '67': '0a', '68': 'f7',
    '69': 'e4', '6a': '58', '6b': '05', '6c': 'b8', '6d': 'b3', '6e': '45', '6f': '06',  # linha 6
    '70': 'd0', '71': '2c', '72': '1e', '73': '8f', '74': 'ca', '75': '3f', '76': '0f', '77': '02', '78': 'c1',
    '79': 'af', '7a': 'bd', '7b': '03', '7c': '01', '7d': '13', '7e': '8a', '7f': '6b',  # linha 7
    '80': '3a', '81': '91', '82': '11', '83': '41', '84': '4f', '85': '67', '86': 'dc', '87': 'ea', '88': '97',
    '89': 'f2', '8a': 'cf', '8b': 'ce', '8c': 'f0', '8d': 'b4', '8e': 'e6', '8f': '73',  # linha 8
    '90': '96', '91': 'ac', '92': '74', '93': '22', '94': 'e7', '95': 'ad', '96': '35', '97': '85', '98': 'e2',
    '99': 'f9', '9a': '37', '9b': 'e8', '9c': '1c', '9d': '75', '9e': 'df', '9f': '6e',  # linha 9
    'a0': '47', 'a1': 'f1', 'a2': '1a', 'a3': '71', 'a4': '1d', 'a5': '29', 'a6': 'c5', 'a7': '89', 'a8': '6f',
    'a9': 'b7', 'aa': '62', 'ab': '0e', 'ac': 'aa', 'ad': '18', 'ae': 'be', 'af': '1b',  # linha a
    'b0': 'fc', 'b1': '56', 'b2': '3e', 'b3': '4b', 'b4': 'c6', 'b5': 'd2', 'b6': '79', 'b7': '20', 'b8': '9a',
    'b9': 'db', 'ba': 'c0', 'bb': 'fe', 'bc': '78', 'bd': 'cd', 'be': '5a', 'bf': 'f4',  # linha b
    'c0': '1f', 'c1': 'dd', 'c2': 'a8', 'c3': '33', 'c4': '88', 'c5': '07', 'c6': 'c7', 'c7': '31', 'c8': 'b1',
    'c9': '12', 'ca': '10', 'cb': '59', 'cc': '27', 'cd': '80', 'ce': 'ec', 'cf': '5f',  # linha c
    'd0': '60', 'd1': '51', 'd2': '7f', 'd3': 'a9', 'd4': '19', 'd5': 'b5', 'd6': '4a', 'd7': '0d', 'd8': '2d',
    'd9': 'e5', 'da': '7a', 'db': '9f', 'dc': '93', 'dd': 'c9', 'de': '9c', 'df': 'ef',  # linha d
    'e0': 'a0', 'e1': 'e0', 'e2': '3b', 'e3': '4d', 'e4': 'ae', 'e5': '2a', 'e6': 'f5', 'e7': 'b0', 'e8': 'c8',
    'e9': 'eb', 'ea': 'bb', 'eb': '3c', 'ec': '83', 'ed': '53', 'ee': '99', 'ef': '61',  # linha e
    'f0': '17', 'f1': '2b', 'f2': '04', 'f3': '7e', 'f4': 'ba', 'f5': '77', 'f6': 'd6', 'f7': '26', 'f8': 'e1',
    'f9': '69', 'fa': '14', 'fb': '63', 'fc': '55', 'fd': '21', 'fe': '0c', 'ff': '7d',  # linha f
}

e_table = {
    '00': '01', '01': '03', '02': '05', '03': '0f', '04': '11', '05': '33', '06': '55', '07': 'ff', '08': '1a',
    '09': '2e', '0a': '72', '0b': '96', '0c': 'a1', '0d': 'f8', '0e': '13', '0f': '35',  # linha 0
    '10': '5f', '11': 'e1', '12': '38', '13': '48', '14': 'd8', '15': '73', '16': '95', '17': 'a4', '18': 'f7',
    '19': '02', '1a': '06', '1b': '0a', '1c': '1e', '1d': '22', '1e': '66', '1f': 'aa',  # linha 1
    '20': 'e5', '21': '34', '22': '5c', '23': 'e4', '24': '37', '25': '59', '26': 'eb', '27': '26', '28': '6a',
    '29': 'be', '2a': 'd9', '2b': '70', '2c': '90', '2d': 'ab', '2e': 'e6', '2f': '31',  # linha 2
    '30': '53', '31': 'f5', '32': '04', '33': '0c', '34': '14', '35': '3c', '36': '44', '37': 'cc', '38': '4f',
    '39': 'd1', '3a': '68', '3b': 'b8', '3c': 'd3', '3d': '6e', '3e': 'b2', '3f': 'cd',  # linha 3
    '40': '4c', '41': 'd4', '42': '67', '43': 'a9', '44': 'e0', '45': '3b', '46': '4d', '47': 'd7', '48': '62',
    '49': 'a6', '4a': 'f1', '4b': '08', '4c': '18', '4d': '28', '4e': '78', '4f': '88',  # linha 4
    '50': '83', '51': '9e', '52': 'b9', '53': 'd0', '54': '6b', '55': 'bd', '56': 'dc', '57': '7f', '58': '81',
    '59': '98', '5a': 'b3', '5b': 'ce', '5c': '49', '5d': 'db', '5e': '76', '5f': '9a',  # linha 5
    '60': 'b5', '61': 'c4', '62': '57', '63': 'f9', '64': '10', '65': '30', '66': '50', '67': 'f0', '68': '0b',
    '69': '1d', '6a': '27', '6b': '69', '6c': 'bb', '6d': 'd6', '6e': '61', '6f': 'a3',  # linha 6
    '70': 'fe', '71': '19', '72': '2b', '73': '7d', '74': '87', '75': '92', '76': 'ad', '77': 'ec', '78': '2f',
    '79': '71', '7a': '93', '7b': 'ae', '7c': 'e9', '7d': '20', '7e': '60', '7f': 'a0',  # linha 7
    '80': 'fb', '81': '16', '82': '3a', '83': '4e', '84': 'd2', '85': '6d', '86': 'b7', '87': 'c2', '88': '5d',
    '89': 'e7', '8a': '32', '8b': '56', '8c': 'fa', '8d': '15', '8e': '3f', '8f': '41',  # linha 8
    '90': 'c3', '91': '5e', '92': 'e2', '93': '3d', '94': '47', '95': 'c9', '96': '40', '97': 'c0', '98': '5b',
    '99': 'ed', '9a': '2c', '9b': '74', '9c': '9c', '9d': 'bf', '9e': 'da', '9f': '75',  # linha 9
    'a0': '9f', 'a1': 'ba', 'a2': 'd5', 'a3': '64', 'a4': 'ac', 'a5': 'ef', 'a6': '2a', 'a7': '7e', 'a8': '82',
    'a9': '9d', 'aa': 'bc', 'ab': 'df', 'ac': '7a', 'ad': '8e', 'ae': '89', 'af': '80',  # linha a
    'b0': '9b', 'b1': 'b6', 'b2': 'c1', 'b3': '58', 'b4': 'e8', 'b5': '23', 'b6': '65', 'b7': 'af', 'b8': 'ea',
    'b9': '25', 'ba': '6f', 'bb': 'b1', 'bc': 'c8', 'bd': '43', 'be': 'c5', 'bf': '54',  # linha b
    'c0': 'fc', 'c1': '1f', 'c2': '21', 'c3': '63', 'c4': 'a5', 'c5': 'f4', 'c6': '07', 'c7': '09', 'c8': '1b',
    'c9': '2d', 'ca': '77', 'cb': '99', 'cc': 'b0', 'cd': 'cb', 'ce': '46', 'cf': 'ca',  # linha c
    'd0': '45', 'd1': 'cf', 'd2': '4a', 'd3': 'de', 'd4': '79', 'd5': '8b', 'd6': '86', 'd7': '91', 'd8': 'ab',
    'd9': 'e3', 'da': '3e', 'db': '42', 'dc': 'c6', 'dd': '51', 'de': 'f3', 'df': '0e',  # linha d
    'e0': '12', 'e1': '36', 'e2': '5a', 'e3': 'ee', 'e4': '29', 'e5': '7b', 'e6': '8d', 'e7': '8c', 'e8': '8f',
    'e9': '8a', 'ea': '85', 'eb': '94', 'ec': 'a7', 'ed': 'f2', 'ee': '0d', 'ef': '17',  # linha e
    'f0': '39', 'f1': '4b', 'f2': 'dd', 'f3': '7c', 'f4': '84', 'f5': '97', 'f6': 'a2', 'f7': 'fd', 'f8': '1c',
    'f9': '24', 'fa': '6c', 'fb': 'b4', 'fc': 'c7', 'fd': '52', 'fe': 'f6', 'ff': '01',  # linha f

}

l_table = {
    '00': '', '01': '00', '02': '19', '03': '01', '04': '32', '05': '02', '06': '1a', '07': 'c6', '08': '4b',
    '09': 'c7', '0a': '1b', '0b': '68', '0c': '33', '0d': 'ee', '0e': 'df', '0f': '03',  # linha 0 (00 não tem valor)
    '10': '64', '11': '04', '12': 'e0', '13': '0e', '14': '34', '15': '8d', '16': '81', '17': 'ef', '18': '4c',
    '19': '71', '1a': '08', '1b': 'c8', '1c': 'f8', '1d': '69', '1e': '1c', '1f': 'c1',  # linha 1
    '20': '7d', '21': 'c2', '22': '1d', '23': 'b5', '24': 'f9', '25': 'b9', '26': '27', '27': '6a', '28': '4d',
    '29': 'e4', '2a': 'a6', '2b': '72', '2c': '9a', '2d': 'c9', '2e': '09', '2f': '78',  # linha 2
    '30': '65', '31': '2f', '32': '8a', '33': '05', '34': '21', '35': '0f', '36': 'e1', '37': '24', '38': '12',
    '39': 'f0', '3a': '82', '3b': '45', '3c': '35', '3d': '93', '3e': 'da', '3f': '8e',  # linha 3
    '40': '96', '41': '8f', '42': 'db', '43': 'bd', '44': '36', '45': 'd0', '46': 'ce', '47': '94', '48': '13',
    '49': '5c', '4a': 'd2', '4b': 'f1', '4c': '40', '4d': '46', '4e': '83', '4f': '38',  # linha 4
    '50': '66', '51': 'dd', '52': 'fd', '53': '30', '54': 'bf', '55': '06', '56': '8b', '57': '62', '58': 'b3',
    '59': '25', '5a': 'e2', '5b': '98', '5c': '22', '5d': '88', '5e': '91', '5f': '10',  # linha 5
    '60': '7e', '61': '6e', '62': '48', '63': 'c3', '64': 'a3', '65': 'b6', '66': '1e', '67': '42', '68': '3a',
    '69': '6b', '6a': '28', '6b': '54', '6c': 'fa', '6d': '85', '6e': '3d', '6f': 'ba',  # linha 6
    '70': '2b', '71': '79', '72': '0a', '73': '15', '74': '9b', '75': '9f', '76': '5e', '77': 'ca', '78': '4e',
    '79': 'd4', '7a': 'ac', '7b': 'e5', '7c': 'f3', '7d': '73', '7e': 'a7', '7f': '57',  # linha 7
    '80': 'af', '81': '58', '82': 'a8', '83': '50', '84': 'f4', '85': 'ea', '86': 'd6', '87': '74', '88': '4f',
    '89': 'ae', '8a': 'e9', '8b': 'd5', '8c': 'e7', '8d': 'e6', '8e': 'ad', '8f': 'e8',  # linha 8
    '90': '2c', '91': 'd7', '92': '75', '93': '7a', '94': 'eb', '95': '16', '96': '0b', '97': 'f5', '98': '59',
    '99': 'cb', '9a': '5f', '9b': 'b0', '9c': '9c', '9d': 'a9', '9e': '51', '9f': 'a0',  # linha 9
    'a0': '7f', 'a1': '0c', 'a2': 'f6', 'a3': '6f', 'a4': '17', 'a5': 'c4', 'a6': '49', 'a7': 'ec', 'a8': 'd8',
    'a9': '43', 'aa': '1f', 'ab': '2d', 'ac': 'a4', 'ad': '76', 'ae': '7b', 'af': 'b7',  # linha a
    'b0': 'cc', 'b1': 'bb', 'b2': '3e', 'b3': '5a', 'b4': 'fb', 'b5': '60', 'b6': 'b1', 'b7': '86', 'b8': '3b',
    'b9': '52', 'ba': 'a1', 'bb': '6c', 'bc': 'aa', 'bd': '55', 'be': '29', 'bf': '9d',  # linha b
    'c0': '97', 'c1': 'b2', 'c2': '87', 'c3': '90', 'c4': '61', 'c5': 'be', 'c6': 'dc', 'c7': 'fc', 'c8': 'bc',
    'c9': '95', 'ca': 'cf', 'cb': 'cd', 'cc': '37', 'cd': '3f', 'ce': '5b', 'cf': 'd1',  # linha c
    'd0': '53', 'd1': '39', 'd2': '84', 'd3': '3c', 'd4': '41', 'd5': 'a2', 'd6': '6d', 'd7': '47', 'd8': '14',
    'd9': '2a', 'da': '9e', 'db': '5d', 'dc': '56', 'dd': 'f2', 'de': 'd3', 'df': 'ab',  # linha d
    'e0': '44', 'e1': '11', 'e2': '92', 'e3': 'd9', 'e4': '23', 'e5': '20', 'e6': '2e', 'e7': '89', 'e8': 'b4',
    'e9': '7c', 'ea': 'b8', 'eb': '26', 'ec': '77', 'ed': '99', 'ee': 'e3', 'ef': 'a5',  # linha e
    'f0': '67', 'f1': '4a', 'f2': 'ed', 'f3': 'de', 'f4': 'c5', 'f5': '31', 'f6': 'fe', 'f7': '18', 'f8': '0d',
    'f9': '63', 'fa': '8c', 'fb': '80', 'fc': 'c0', 'fd': 'f7', 'fe': '70', 'ff': '07',  # linha f

}

# Criptografia
encrypt(user_input, encryption_key, s_box_map)
