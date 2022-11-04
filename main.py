import copy

import numpy as np
from tables import s_box_map, s_box_map_inv, e_table, l_table
from key_expansion import key_expansion


# Funções


def convert_to_hex(var):
    var_hex = format(ord(var), "02x")
    # print(f"{var}   {var_hex}")
    return var_hex


def transpose(matrix_a, matrix_res):
    for a in range(4):
        for b in range(4):
            matrix_res[a][b] = matrix_a[b][a]


# divide a mensagem em blocos de 16 bytes e guarda-os em uma lista
def message_to_block(string):
    message_block = []
    str_instance = ""
    for i in range(0, len(string), 16):
        for e in range(i, i + 16):
            print(f"i: {i} e: {e}")
            try:
                str_instance = str_instance + string[e]
            except Exception:
                str_instance = str_instance + " "
        message_block.append(str_instance)
        str_instance = ""
    print(message_block)
    return message_block


def to_hex_array(input_string):
    block_array = [["20", "20", "20", "20"], ["20", "20", "20", "20"],
                   ["20", "20", "20", "20"], ["20", "20", "20", "20"]]
    text_array = []
    x = 0
    y = 0
    for i in range(0, 16):
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
            block_array = np.transpose(block_array)
            text_array = copy.deepcopy(block_array)
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
            new_array[i][j] = int(array[i][j], 16) ^ int(key[i][j], 16)
            new_array[i][j] = chr(new_array[i][j])
            new_array[i][j] = format(ord(str(new_array[i][j])), "x")
            # print(f"{array[i][j]} XOR {key[i][j]} = {new_array[i][j]}")
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
            # print(f"({l_table[array[0][i]]} = {array[0][i]}) + ({l_table[mult_matrix[j][0]]} = {mult_matrix[j][0]})")
            # print(f"({l_table[array[1][i]]} = {array[1][i]}) + ({l_table[mult_matrix[j][1]]} = {mult_matrix[j][1]})")
            # print(f"({l_table[array[2][i]]} = {array[2][i]}) + ({l_table[mult_matrix[j][2]]} = {mult_matrix[j][2]})")
            # print(f"({l_table[array[3][i]]} = {array[3][i]}) + ({l_table[mult_matrix[j][3]]} = {mult_matrix[j][3]})")
            if array[0][i] != '00':
                a = int(l_table[array[0][i]], 16) + int(l_table[mult_matrix[j][0]], 16)
                a = verify_table_compatibility(a)
            else:
                a = 0
            if array[1][i] != '00':
                b = int(l_table[array[1][i]], 16) + int(l_table[mult_matrix[j][1]], 16)
                b = verify_table_compatibility(b)
            else:
                b = 0
            if array[2][i] != '00':
                c = int(l_table[array[2][i]], 16) + int(l_table[mult_matrix[j][2]], 16)
                c = verify_table_compatibility(c)
            else:
                c = 0
            if array[3][i] != '00':
                d = int(l_table[array[3][i]], 16) + int(l_table[mult_matrix[j][3]], 16)
                d = verify_table_compatibility(d)
            else:
                d = 0
            mix_state[j][i] = a ^ b ^ c ^ d
            mix_state[j][i] = f"{mix_state[j][i]:x}"
            # print(f"{a} {b} {c} {d} = {mix_state[j][i]}")
    print(f"mix_state: {mix_state}\n")
    return mix_state


def verify_table_compatibility(var):
    # caso o número hexadecimal seja maior do que FF, deve-se subtrair FF de seu valor para que ele possa ser usado na
    # e_table e l_table.
    if len(f"{var:x}") > 2:
        var = var - 0xff
    var = int(e_table[f"{var:02x}"], 16)
    return var


# engloba todas as funções de criptografia
def encrypt(msg_array, key, s_box):
    res = []
    key = to_hex_array(key)
    # guarda uma cópia da chave de criptografia
    key_copy = key.copy()
    # expansão de chave
    key_expanded = key_expansion(key, key_copy)
    for m in range(0, len(msg_array)):
        # Transforma a mensagem em hexadecimal conforme a tabela ASCII
        msg_array[m] = to_hex_array(msg_array[m])
        # Faz um XOR  entre a mensagem e a chave
        new_array = add_round_key(msg_array[m], key_expanded[0])
        state = new_array
        print(f"round 0 key: {state}")
        # loop responsável pelos rounds 1-9. Os rounds 0 e 10 possuem características únicas
        for i in range(1, 10):
            print(f"round: {i}\n")
            # Passa o resultado do passo anterior por uma S_box
            sub_byte(new_array, s_box)
            # Desloca as linhas do array com os passos 0, 1, 2 e 3 para cada linha, respetivamente
            shift_rows(new_array)
            # Realiza cálculos matemáticos para "embaralhar" a lista.
            new_array = mix_columns(new_array)
            # faz um XOR entre o resultado e a chave do round atual
            new_array = add_round_key(new_array, key_expanded[i])
            state = new_array
            print(f"round {i} state: {state}\n")
        # último round
        sub_byte(new_array, s_box)
        shift_rows(new_array)
        new_array = add_round_key(new_array, key_expanded[10])
        state = new_array
        res.append(state)
        print(f"last round state: {state}\n")
    return res


# Execução
# key: 54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
# message: 54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
user_input = "Two One Nine TwoAbbCD Audowsgjfe Uwd f jbNv aowq easUotn  cd wta AoCkw i2 jwsjat ahjtUWEamwduotr kwuQQorubncIvTd"
encryption_key = "Thats my Kung Fu"

message = message_to_block(user_input)

# Criptografia
encrypted_msg = encrypt(message, encryption_key, s_box_map)
print(f"encrypted message: {encrypted_msg}")
