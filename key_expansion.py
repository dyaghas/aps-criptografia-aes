import copy

from tables import s_box_map, s_box_map_inv, e_table, l_table


def rot_word(key):
    # previne que o input seja alterado
    state_array = copy.deepcopy(key)
    for i in range(0, 4):
        state_array[0][i][3] = key[0][i - 3][3]
    print(f"\nrotWord key:\n {state_array}\n")
    return state_array


def sub_word(rot_key):
    # Previne que o input seja alterado
    state_res = copy.deepcopy(rot_key)
    # Substitui os valores através de uma s_box
    for i in range(0, 4):
        state_res[0][i][3] = s_box_map[state_res[0][i][3]]
    print(f"\nsubWord key:\n {state_res}\n")
    return state_res


def rcon(sub_key):
    # Previne que o input seja alterado
    state_res = copy.deepcopy(sub_key)
    rcon_res = int(sub_key[0][0][3], 16)
    rcon_res += 1
    rcon_res = f"{rcon_res:x}"
    state_res[0][0][3] = rcon_res
    print(f"rcon:\n{state_res}\n")
    return state_res


def expansion_xor(rcon_key, original_key):
    state_res = copy.deepcopy(rcon_key)
    # faz o XOR da primeira coluna da chave retornada na função rcon com a chave original
    for e in range(0, 4):
        print(f"{rcon_key[0][e][0]} xor {rcon_key[0][e][3]}")
        element = int(rcon_key[0][e][0], 16) ^ int(rcon_key[0][e][3], 16)
        # guarda o elemento do cálculo anterior no índice especificado
        state_res[0][e][0] = f"{element:x}"
    for x in range(1, 4):
        for y in range(0, 4):
            # faz o XOR das três colunas restantes
            element = int(state_res[0][y][x - 1], 16) ^ int(original_key[0][y][x], 16)
            element = f"{element:x}"
            state_res[0][y][x] = element
    print(f"next round key:\n{state_res}")
    return state_res
