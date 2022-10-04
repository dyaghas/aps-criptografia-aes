user_input = "Two One Nine Two"
encryption_key = "Thats my Kung Fu"


def convert_to_hex(var):
    var = format(ord(var), "x")
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
    c = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    for i in range(0, 4):
        for j in range(0, 4):
            # Adiciona a round key através de um XOR com o input
            c[i][j] = int(array[0][i][j], 16) ^ int(key[0][i][j], 16)
            c[i][j] = chr(c[i][j])
            c[i][j] = format(ord(str(c[i][j])), "x")
    print(f"hex: {c}")


user_input = to_hex_array(user_input)

encryption_key = to_hex_array(encryption_key)

add_round_key(user_input, encryption_key)
