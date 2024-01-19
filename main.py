import copy
import numpy as np
from tkinter import *
from tkinter import ttk
from tables import s_box_map, s_box_map_inv, e_table, l_table
from key_expansion import key_expansion

BYTE_SIZE = 4


# Funções
def string_to_hex(var):
    var_hex = format(ord(var), "02x")
    return var_hex


# divide a mensagem em blocos de 16 bytes e guarda-os em uma lista
def text_to_array(text):
    text_block = []
    str_instance = ""
    # str_instance recebe 16 caracteres que serão guardados como um vetor na matriz text_block
    for a in range(0, len(text), BYTE_SIZE*4):
        for b in range(a, a + BYTE_SIZE*4):
            try:
                str_instance = str_instance + text[b]
            # insere caracteres vazios no final de uma str_instance com menos de 16 caracteres
            except IndexError:
                str_instance = str_instance + " "
        text_block.append(str_instance)
        str_instance = ""
    # print(f"Blocos: ", text_block, "\n")
    return text_block


def text_to_hex_array(input_string):
    # array preenchido por espaços vazios (valor em hexadecimal)
    block_array = [["20", "20", "20", "20"],
                   ["20", "20", "20", "20"],
                   ["20", "20", "20", "20"],
                   ["20", "20", "20", "20"]]
    hex_array = []
    a = 0
    b = 0
    for e in range(0, BYTE_SIZE*4):
        if a < BYTE_SIZE:
            block_array[b][a] = string_to_hex(input_string[e])
            a += 1
        elif b < BYTE_SIZE-1:
            a = 0
            b += 1
            block_array[b][a] = string_to_hex(input_string[e])
            # Evita que a última letra de cada linha dentro de block_array seja substituida pela primeira do bloco
            # seguinte
            a += 1
        # Transpõe o block_array.
        if (b == BYTE_SIZE-1 and a == BYTE_SIZE) or e == len(input_string) - 1:
            block_array = np.transpose(block_array)
            hex_array = copy.deepcopy(block_array)
            a = 0
            b = 0
            block_array = [["", "", "", ""],
                           ["", "", "", ""],
                           ["", "", "", ""],
                           ["", "", "", ""]]
            continue
    # print(f"Vetor hexadecimal:\n", hex_array, "\n")
    return hex_array


def add_round_key(array, key):
    res_array = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    for e in range(0, BYTE_SIZE):
        for j in range(0, BYTE_SIZE):
            # Adiciona a round key através de um XOR com o input
            result_hex = format(int(array[e][j], 16) ^ int(key[e][j], 16), '02x')
            res_array[e][j] = result_hex
    # print(f"Linha do vetor com round key adicionada: ", res_array, "\n")
    return res_array


def sub_byte(array, s_box):
    for row in array:
        for i, value in enumerate(row):
            # faz com que value sempre tenha dois algarismos para possibilitar a comparação com s_box
            value = value.zfill(2)
            row[i] = s_box[value]
    # print(f"Sub byte: ", array, "\n")


def shift_rows(array):
    offset = 0
    for e in range(1, BYTE_SIZE):
        offset += 1
        array[e] = np.roll(array[e], -offset)
    # print(f"Shift rows:", array, "\n")


def shift_rows_inv(array):
    offset = 0
    for e in range(1, BYTE_SIZE):
        offset += 1
        array[e] = np.roll(array[e], offset)
    # print(f"Shift rows: ", array, "\n")


def mix_columns(array):
    mult_matrix = [['02', '03', '01', '01'],
                   ['01', '02', '03', '01'],
                   ['01', '01', '02', '03'],
                   ['03', '01', '01', '02']]
    mix_state = [[0x00, 0x00, 0x00, 0x00],
                 [0x00, 0x00, 0x00, 0x00],
                 [0x00, 0x00, 0x00, 0x00],
                 [0x00, 0x00, 0x00, 0x00]]
    # For aninhado q passa por colunas ao invés de linhas
    for e in range(0, BYTE_SIZE):
        for j in range(0, BYTE_SIZE):
            if array[0][e] != '00':
                a = int(l_table[array[0][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][0]], BYTE_SIZE*4)
                a = verify_table_compatibility(a)
            else:
                a = 0
            if array[1][e] != '00':
                b = int(l_table[array[1][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][1]], BYTE_SIZE*4)
                b = verify_table_compatibility(b)
            else:
                b = 0
            if array[2][e] != '00':
                c = int(l_table[array[2][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][2]], BYTE_SIZE*4)
                c = verify_table_compatibility(c)
            else:
                c = 0
            if array[3][e] != '00':
                d = int(l_table[array[3][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][3]], BYTE_SIZE*4)
                d = verify_table_compatibility(d)
            else:
                d = 0
            mix_state[j][e] = a ^ b ^ c ^ d
            mix_state[j][e] = f"{mix_state[j][e]:x}"
    # print(f"Mix columns: ", mix_state, "\n")
    return mix_state


def verify_table_compatibility(var):
    # caso o número hexadecimal seja maior do que FF, deve-se subtrair FF de seu valor para que ele possa ser usado na
    # e_table e l_table.
    if len(f"{var:x}") > 2:
        var = var - 0xff
    var = int(e_table[f"{var:02x}"], BYTE_SIZE*4)
    return var


def mix_columns_inv(array):
    mult_matrix = [['0e', '0b', '0d', '09'],
                   ['09', '0e', '0b', '0d'],
                   ['0d', '09', '0e', '0b'],
                   ['0b', '0d', '09', '0e']]
    mix_state = [[0x00, 0x00, 0x00, 0x00],
                 [0x00, 0x00, 0x00, 0x00],
                 [0x00, 0x00, 0x00, 0x00],
                 [0x00, 0x00, 0x00, 0x00]]
    for e in range(0, BYTE_SIZE):
        for j in range(0, BYTE_SIZE):
            if array[0][e] != '00':
                a = int(l_table[array[0][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][0]], BYTE_SIZE*4)
                a = verify_table_compatibility(a)
            else:
                a = 0
            if array[1][e] != '00':
                b = int(l_table[array[1][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][1]], BYTE_SIZE*4)
                b = verify_table_compatibility(b)
            else:
                b = 0
            if array[2][e] != '00':
                c = int(l_table[array[2][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][2]], BYTE_SIZE*4)
                c = verify_table_compatibility(c)
            else:
                c = 0
            if array[3][e] != '00':
                d = int(l_table[array[3][e]], BYTE_SIZE*4) + int(l_table[mult_matrix[j][3]], BYTE_SIZE*4)
                d = verify_table_compatibility(d)
            else:
                d = 0
            mix_state[j][e] = a ^ b ^ c ^ d
            mix_state[j][e] = f"{mix_state[j][e]:x}"
    # print(f"Mix columns: ", mix_state, "\n")
    return mix_state


# engloba todas as funções de criptografia
def encrypt(msg_array, key_expanded, s_box):
    encrypt_res = []
    for m in range(0, len(msg_array)):
        # primeiro round
        # Transforma a mensagem em hexadecimal conforme a tabela ASCII
        msg_array[m] = text_to_hex_array(msg_array[m])
        # Faz um XOR  entre a mensagem e a chave
        new_array = add_round_key(msg_array[m], key_expanded[0])

        # loop responsável pelos rounds 1-9. Os rounds 0 e 10 possuem características únicas
        for a in range(1, 10):
            # Passa o resultado do passo anterior por uma S_box
            sub_byte(new_array, s_box)
            # Desloca as linhas do array com os passos 0, 1, 2 e 3 para cada linha, respetivamente
            shift_rows(new_array)
            # Realiza cálculos matemáticos para "embaralhar" a lista.
            new_array = mix_columns(new_array)
            # faz um XOR entre o resultado e a chave do round atual
            new_array = add_round_key(new_array, key_expanded[a])

        # último round
        sub_byte(new_array, s_box)
        shift_rows(new_array)
        new_array = add_round_key(new_array, key_expanded[10])
        encrypt_res.append(new_array)
    return encrypt_res


def decrypt(encrypted_message, key_array, s_box_inv):
    final_message = []
    for a in range(0, len(encrypted_message)):
        # descriptografia de 16 bytes realizadas em 10 rounds
        # round 10 (decrescente)
        decrypt_res = add_round_key(encrypted_message[a], key_array[10])
        shift_rows_inv(decrypt_res)
        sub_byte(decrypt_res, s_box_inv)
        decrypt_res = add_round_key(decrypt_res, key_array[9])
        decrypt_res = mix_columns_inv(decrypt_res)

        # round 9 ao 2
        for b in range(1, 9):
            shift_rows_inv(decrypt_res)
            sub_byte(decrypt_res, s_box_inv)
            decrypt_res = add_round_key(decrypt_res, key_array[10 - b - 1])
            decrypt_res = mix_columns_inv(decrypt_res)

        # round 1
        shift_rows_inv(decrypt_res)
        sub_byte(decrypt_res, s_box_inv)
        decrypt_res = add_round_key(decrypt_res, key_array[0])
        decrypt_res = np.transpose(decrypt_res)
        final_message.append(decrypt_res)
    return final_message


def encrypted_array_to_line(encrypted_input):
    encrypted_output = ""
    for a in range(0, len(encrypted_input)):
        for b in range(0, BYTE_SIZE):
            for c in range(0, BYTE_SIZE):
                encrypted_output = encrypted_output + encrypted_input[a][b][c]
    return encrypted_output


# Execução
def execute_encryption(*args):
    user_input = str(original_text.get())
    encryption_key = str(encrypt_key.get())

    # print(f"\nmensagem original: {user_input}\n")

    message = text_to_array(user_input)

    # Criptografia
    try:
        key = text_to_hex_array(encryption_key)
        key_final = key_expansion(key)
    except IndexError:
        result_label.set("A chave de criptografia precisa ter pelomenos 16 caracteres")
        result_text.set("")
        raise Exception("A chave de criptografia precisa ter pelomenos 16 caracteres")
    encrypted_msg = encrypt(message, key_final, s_box_map)

    # Descriptografia
    try:
        decrypted_message = ''
        decryption_state = decrypt(encrypted_msg, key_final, s_box_map_inv)
        for i in range(0, len(decryption_state)):
            for x in range(0, BYTE_SIZE):
                for y in range(0, BYTE_SIZE):
                    # transforma os números hexadecimais em seus caracteres utf-8 correspondentes
                    decryption_state[i][x][y] = bytes.fromhex(decryption_state[i][x][y]).decode('utf-8')
                    decrypted_message = decrypted_message + decryption_state[i][x][y]
    except UnicodeDecodeError:
        # print("Caracter inválido - Insira apenas caracteres presentes na tabela ASCII")
        result_label.set("Caracter inválido - Insira apenas caracteres presentes na tabela ASCII")
        result_text.set("")
    else:
        print(f"Mensagem criptografada: {encrypted_array_to_line(encrypted_msg)}\n")
        if encrypted_array_to_line(encrypted_msg) != "":
            result_label.set("Texto criptografado: ")
            result_text.set(encrypted_array_to_line(encrypted_msg))
        else:
            result_label.set("Campo não preenchido")
            result_text.set("")
        print(f"Texto descriptografado: {decrypted_message}\n")


# Interface
root = Tk()
root.title("AES-128")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe = ttk.Frame(root, padding="15 30 15 30")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(1, minsize=40, weight=1, pad=20)
mainframe.columnconfigure(2, minsize=400, weight=40)
mainframe.columnconfigure(3, minsize=20, weight=4, pad=20)
mainframe.rowconfigure(1, minsize=30, pad=10)
mainframe.rowconfigure(2, minsize=30, pad=10)
mainframe.rowconfigure(3, minsize=30, pad=20)
mainframe.rowconfigure(4, weight=1, pad=20)

# Input da chave de criptografia
ttk.Label(mainframe, text="Chave").grid(column=1, row=1)
encrypt_key = StringVar()
encrypt_key_entry = ttk.Entry(mainframe, width=60, textvariable=encrypt_key)
encrypt_key_entry.grid(column=2, row=1, sticky=(W, E))
# Input do texto que será criptografado
ttk.Label(mainframe, text="Texto").grid(column=1, row=2)
original_text = StringVar()
original_text_entry = ttk.Entry(mainframe, width=60, textvariable=original_text)
original_text_entry.grid(column=2, row=2, sticky=(W, E))

# Botão "criptografar"
ttk.Button(mainframe, text="Criptografar", command=execute_encryption).grid(column=2, row=3)

encrypt_key_entry.focus()
original_text_entry.focus()
root.bind("<Return>", execute_encryption)

# Texto criptografado
result_label = StringVar()
ttk.Label(mainframe, textvariable=result_label).grid(column=2, row=4)
result_text = StringVar()
ttk.Label(mainframe, textvariable=result_text).grid(column=2, row=5)

root.mainloop()
