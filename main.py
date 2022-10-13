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
            block_array_transposed = block_array[:][:]
            transpose(block_array, block_array_transposed)
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
            # transforma '0' em '00' para possibilitar o sub-byte na s-box
            if array[i][j] == '0':
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
    # For aninhado q passa por colunas ao invés de linhas
    for i in range(0, 4):
        for j in range(0, 4):
            print(array[j][i])
            array[j][i] = "{0:08b}".format(int(array[j][i], 16))
            print(array[j][i])


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

    mix_columns(new_array)

# Execução


user_input = "Two One Nine Two"
encryption_key = "Thats my Kung Fu"
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
}
# Criptografia
encrypt(user_input, encryption_key, s_box_map)
