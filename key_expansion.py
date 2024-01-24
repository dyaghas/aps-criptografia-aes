import copy

from tables import s_box_map, rcon_dict

BYTE_SIZE = 4
ROUNDS = 11


# faz com que um número hexadecimal tenha necessariamente dois caracteres
def force_two_digits(hex_string):
    if len(hex_string) < 2:
        hex_string = f"0{hex_string}"
    return hex_string


# realiza a etapa de rotação na chave de criptografia
def rot_word(key):
    # previne que o input seja alterado acidentalmente
    state_array = copy.deepcopy(key)
    for i in range(0, BYTE_SIZE):
        state_array[i][3] = key[i - 3][3]
        # verifica se todas as strings hexadecimais possuem dois digitos
        state_array[i][3] = force_two_digits(state_array[i][3])
    return state_array


# realiza a etapa de substituição na chave de criptografia
def sub_word(rot_key):
    # Previne que o input seja alterado
    state_res = copy.deepcopy(rot_key)
    # Substitui os valores através de uma s_box
    for i in range(0, BYTE_SIZE):
        state_res[i][3] = s_box_map[state_res[i][3]]
    return state_res


# realiza a etapa de rcon na chave de criptografia
def rcon(sub_key, loop_num):
    # Previne que o input seja alterado
    state_res = copy.deepcopy(sub_key)
    rcon_res = int(sub_key[0][3], BYTE_SIZE*4)
    rcon_res = rcon_res ^ rcon_dict[loop_num]
    rcon_res = f"{rcon_res:x}"
    state_res[0][3] = rcon_res
    return state_res


# realiza a etapa de expansão na chave de criptografia
def expansion_xor(rcon_key, original_key):
    state_res = copy.deepcopy(rcon_key)
    # faz o XOR da primeira coluna da chave retornada na função rcon com a chave original
    for e in range(0, BYTE_SIZE):
        element = int(rcon_key[e][0], BYTE_SIZE*4) ^ int(rcon_key[e][3], BYTE_SIZE*4)
        # guarda o elemento do cálculo anterior no índice especificado
        state_res[e][0] = f"{element:x}"
    for x in range(1, BYTE_SIZE):
        for y in range(0, BYTE_SIZE):
            # faz o XOR das três colunas restantes
            element = int(state_res[y][x - 1], BYTE_SIZE*4) ^ int(original_key[y][x], BYTE_SIZE*4)
            element = f"{element:x}"
            state_res[y][x] = element
    return state_res


# engloba todas as funções da expansão de chave
def key_expansion(key):
    key_expanded = [key]
    key_fragment = copy.deepcopy(key)
    # cria uma chave para cada round de criptografia
    for i in range(1, ROUNDS):
        key_fragment = rot_word(key_fragment)
        key_fragment = sub_word(key_fragment)
        key_fragment = rcon(key_fragment, i)
        key_fragment = expansion_xor(key_fragment, key)
        key_expanded.append(key_fragment)
    return key_expanded
