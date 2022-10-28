import numpy as np
from tables import s_box_map, s_box_map_inv, e_table, l_table
from key_expansion import key_expansion


# Funções


def convert_to_hex(var):
    var_hex = format(ord(var), "02x")
    return var_hex


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
    print(f"hex: {text_array}\n")
    return text_array


def add_round_key(array, key):
    new_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(0, 4):
        for j in range(0, 4):
            # Adiciona a round key através de um XOR com o input
            new_array[i][j] = int(array[0][i][j], 16) ^ int(key[0][i][j], 16)
            new_array[i][j] = chr(new_array[i][j])
            new_array[i][j] = format(ord(str(new_array[i][j])), "x")
    print(f"round-key: {new_array}\n")
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
    print(f"sub-byte: {array}\n")


def sub_byte_inv(array, s_box_inv):
    for i in range(0, 4):
        for j in range(0, 4):
            array[i][j] = s_box_inv[array[i][j]]
    print(f"sub-byte-inv: {array}\n")


def shift_rows(array):
    offset = 0
    for i in range(1, 4):
        offset += 1
        array[i] = np.roll(array[i], -offset)
    print(f"shift rows: {array}\n")


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
            mix_state[j][i] = [f"{mix_state[j][i]:x}"]
    print(f"mix_state: {mix_state}\n")
    return mix_state


def verify_table_compatibility(var):
    # caso o número hexadecimal seja maior do que FF, deve-se subtrair FF de seu valor para que ele possa ser usado na
    # e_table e l_table.
    if len(f"{var:x}") > 2:
        var = var - 0xff
    return var


# engloba todas as funções de criptografia
def encrypt(message, key, s_box):
    # Transforma a mensagem e a chave em hexadecimal conforme a tabela ASCII
    message = to_hex_array(message)
    key = to_hex_array(key)
    # guarda uma cópia da chave de criptografia
    key_copy = key.copy()
    # Faz um XOR  entre a mensagem e a chave
    new_array = add_round_key(message, key)
    # Passa o resultado do passo anterior por uma S_box
    sub_byte(new_array, s_box)
    # Desloca as linhas do array com os passos 0, 1, 2 e 3 para cada linha, respetivamente
    shift_rows(new_array)
    # Realiza cálculos matemáticos para "embaralhar" a lista.
    mixed_state = mix_columns(new_array)
    # expansão de chave
    key_expansion(key, key_copy)


# Execução
user_input = "Two One Nine Two"
encryption_key = "Thats my Kung Fu"

# Criptografia
encrypt(user_input, encryption_key, s_box_map)
