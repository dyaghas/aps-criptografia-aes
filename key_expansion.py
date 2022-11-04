import copy

from tables import s_box_map, s_box_map_inv, e_table, l_table, rcon_dict


def force_two_digits(hex_string):
    if len(hex_string) < 2:
        hex_string = f"0{hex_string}"
    return hex_string


def rot_word(key):
    # previne que o input seja alterado
    state_array = copy.deepcopy(key)
    for i in range(0, 4):
        state_array[i][3] = key[i - 3][3]
        # verifica se todas as strings hexadecimais possuem dois digitos
        state_array[i][3] = force_two_digits(state_array[i][3])
    return state_array


def sub_word(rot_key):
    # Previne que o input seja alterado
    state_res = copy.deepcopy(rot_key)
    # Substitui os valores através de uma s_box
    for i in range(0, 4):
        state_res[i][3] = s_box_map[state_res[i][3]]
    return state_res


def rcon(sub_key, loop_num):
    # Previne que o input seja alterado
    state_res = copy.deepcopy(sub_key)
    rcon_res = int(sub_key[0][3], 16)
    rcon_res = rcon_res ^ rcon_dict[loop_num]
    rcon_res = f"{rcon_res:x}"
    state_res[0][3] = rcon_res
    return state_res


def expansion_xor(rcon_key, original_key):
    state_res = copy.deepcopy(rcon_key)
    # faz o XOR da primeira coluna da chave retornada na função rcon com a chave original
    for e in range(0, 4):
        element = int(rcon_key[e][0], 16) ^ int(rcon_key[e][3], 16)
        # guarda o elemento do cálculo anterior no índice especificado
        state_res[e][0] = f"{element:x}"
    for x in range(1, 4):
        for y in range(0, 4):
            # faz o XOR das três colunas restantes
            element = int(state_res[y][x - 1], 16) ^ int(original_key[y][x], 16)
            element = f"{element:x}"
            state_res[y][x] = element
    return state_res


# engloba todas as funções da expansão de chave
def key_expansion(key, key_copy):
    key_expanded = []
    first_key = copy.deepcopy(key)
    key_expanded.append(first_key)
    key_fragment = copy.deepcopy(key)
    key_state = copy.deepcopy(key_copy)
    # cria uma chave para cada round de criptografia
    for i in range(1, 11):
        key_fragment = rot_word(key_fragment)
        key_fragment = sub_word(key_fragment)
        key_fragment = rcon(key_fragment, i)
        key_fragment = expansion_xor(key_fragment, key_state)
        key_state = copy.deepcopy(key_fragment)
        key_expanded.append(key_state)
    return key_expanded
