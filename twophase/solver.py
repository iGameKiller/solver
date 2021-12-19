import numpy as np

np.set_printoptions(suppress=True, precision=2)


def reader(line):  # PATROCINADO

    # índices (posições) de expressões em strings
    ind_fo = line.index('RE')
    ind_re = line.index('SF')

    # substrings
    objet = line[0:2]
    fo = line[3: ind_fo - 2]
    re = line[ind_fo: ind_re]

    # setando função objetivo
    f_obj = []
    fo_split = fo[0:].split()
    for i in fo_split:
        f_obj.append(float(i))

    # setando restrições
    re_split = re[2:].split(',')
    rest_array = []
    for i in re_split:
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.split()
        rest_array.append(i)

    restr_A = []
    restr_b = []
    restr_op = []

    # isso deu trabalho, pqp!
    for i in range(len(rest_array)):
        aux_a = []
        aux_b = []
        for j in range(len(rest_array[i])):
            if rest_array[i][j] == '<=' or rest_array[i][j] == '>=' or rest_array[i][j] == '==':
                restr_op.append(rest_array[i][j])
                aux_b.append(float(rest_array[i][j + 1]))
                break

            aux_a.append(float(rest_array[i][j]))

        restr_A.append(aux_a)
        restr_b.append(aux_b)

    f_obj = np.asarray(f_obj)
    restricoesA = np.asarray(restr_A)
    operadores = np.asarray(restr_op)
    restricoesB = np.asarray(restr_b)

    return objet, f_obj, restricoesA, operadores, restricoesB


def gauss(matrix, minorcolpos, lin, col):
    pivots = []
    for i in range(1, len(matrix)):  # montando array de linhas pivô
        if matrix[i][minorcolpos] > 0:
            newnum = matrix[i][0] / matrix[i][minorcolpos]
            if newnum < 0:
                print("Este modelo não pode ser resolvido, pois existem pivots negativos")
                matrix = np.array([-1])
                return matrix
            pivots.append(newnum)

    pivotMinorValue = pivots[0]
    pivotMinorValuePos = 0

    for i in range(len(pivots)):  # encontrando o menor valor do vetor de pivôs e sua posição
        if pivots[i] < pivotMinorValue:
            pivotMinorValue = pivots[i]
            pivotMinorValuePos = i

    pivotline = matrix[pivotMinorValuePos + 1]  # fazendo uma cópia da linha pivô da matriz
    pivotElement = matrix[pivotMinorValuePos + 1][minorcolpos]

    for i in range(lin):  # setando os novos valores para a linha pivô
        if pivotElement > 0:
            pivotline[i] = matrix[pivotMinorValuePos + 1][i] / pivotElement

    matrix[pivotMinorValuePos + 1] = pivotline  # atualizando os valores na matriz original

    for i in range(lin):  # atualizando todas as outras linhas da matriz, exceto a linha pivô
        if i == pivotMinorValuePos + 1:
            i + 1
        else:
            if i == len(matrix):
                break
            magicNumber = matrix[i][minorcolpos]
            lineCopy = matrix[i]

            for j in range(col):
                if j == len(matrix[i]):
                    break
                else:
                    lineCopy[j] = matrix[i][j] - (magicNumber * pivotline[j])

    return matrix


def readed(objet, f_obj, restr_a, restr_op, restr_b):
    if objet == "MA":
        print("Objetivo: Maximizar")
    elif objet == 'MI':
        print("Objetivo: Minimizar")
    print("Números da função objetivo", f_obj)
    print("Matriz de Restrições A: ")
    print(restricoesA)
    print("Operadores: ", operadores)
    print("Matriz de Restrições B: ")
    print(restricoesB)


def simplextwophase(objet, f_obj, restr_a, restr_op, restr_b):

    if len(restr_a) > len(f_obj) or len(restr_a) == len(f_obj):
        A_pos = []
        A_number = []
        A_count = 0

        X_pos = []
        X_sign = []
        X_number = []
        X_count = 0

        for i in range(len(restr_op)):

            if restr_op[i] == '==':
                A_count = A_count + 1
                A_pos.append(i)
                A_number.append(1)

            elif restr_op[i] == '>=':
                A_count = A_count + 1
                A_pos.append(i)
                A_number.append(1)

                X_sign.append(restr_op[i])
                X_count = X_count + 1
                X_pos.append(i)
                X_number.append(-1)
            elif restr_op[i] == '<=':
                X_count = X_count + 1
                X_pos.append(i)
                X_sign.append(restr_op[i])
                X_number.append(1)

        X_matrix = np.zeros((len(restr_op), X_count))
        A_matrix = np.zeros((len(restr_op), A_count))

        n_length = len(f_obj) + X_count + A_count + 1
        matrix = np.zeros(((len(restr_op)+1), n_length))
        limit = len(matrix[0]) - (len(matrix[0])-A_count)
        limit = n_length - limit

        for i in range(limit, len(matrix[0])):
            matrix[0][i] = 1

        restr_A = np.zeros((len(restr_a), len(restr_a)))

        for i in range(len(restr_A)):
            for j in range(len(restr_a[i])):
                restr_A[i][j] = float(restr_a[i][j])


        for i in range(len(restr_a)):  # Posicionando a matriz A de restrições
            for j in range(len(restr_a[i])):
                matrix[i + 1][j + 1] = restr_a[i][j]

        for i in range(len(restr_b)):  # Posicionando matriz B de restrições
            matrix[i + 1][0] = restr_b[i]

        col = 0
        for i in range(len(X_pos)):
            X_matrix[X_pos[i]][col] = X_number[i]
            col = col + 1

        for i in range(len(X_matrix)):
            for j in range(len(X_matrix[i])):
                matrix[i+1][len(f_obj)+j+1] = X_matrix[i][j]

        col = 0
        for i in range(len(A_pos)):
            A_matrix[A_pos[i]][col] = A_number[i]
            col = col + 1

        for i in range(len(A_matrix)):
            for j in range(len(A_matrix[i])):
                matrix[i+1][len(f_obj)+j+X_count+1] = A_matrix[i][j]

        print(matrix)
        print("___________________________________________________________")

    elif len(restr_a) < len(f_obj):

        extraCol = len(f_obj) - len(restr_a)

        if extraCol == 1:
            A_pos = []
            A_number = []
            A_count = 0

            X_pos = []
            X_sign = []
            X_number = []
            X_count = 0

            for i in range(len(restr_op)):

                if restr_op[i] == '==':
                    A_count = A_count + 1
                    A_pos.append(i)
                    A_number.append(1)

                elif restr_op[i] == '>=':
                    A_count = A_count + 1
                    A_pos.append(i)
                    A_number.append(1)

                    X_sign.append(restr_op[i])
                    X_count = X_count + 1
                    X_pos.append(i)
                    X_number.append(-1)

                elif restr_op[i] == '<=':
                    X_count = X_count + 1
                    X_pos.append(i)
                    X_sign.append(restr_op[i])
                    X_number.append(1)

            X_matrix = np.zeros((len(restr_op), X_count))
            A_matrix = np.zeros((len(restr_op), A_count))

            n_length = len(f_obj) + X_count + A_count + 1
            matrix = np.zeros(((len(restr_op) + 1), n_length+1))
            limit = len(matrix[0]) - (len(matrix[0]) - A_count)
            limit = n_length - limit

            for i in range(limit, len(matrix[0])):
                matrix[0][i] = 1

            col = 0
            for i in range(len(X_pos)):
                X_matrix[X_pos[i]][col] = X_number[i]
                col = col + 1

            for i in range(len(X_matrix)):
                for j in range(len(X_matrix[i])):
                    matrix[i + 1][len(f_obj) + j + 1] = X_matrix[i][j]

            col = 0
            for i in range(len(A_pos)):
                A_matrix[A_pos[i]][col] = A_number[i]
                col = col + 1

            for i in range(len(A_matrix)):
                for j in range(len(A_matrix[i])):
                    matrix[i + 1][len(f_obj) + j + X_count + 1] = A_matrix[i][j]


            print(matrix)


def solver(objet, f_obj, restr_A, restr_op, restr_b, verbose=False):
    if not isinstance(objet, str):
        raise TypeError('Parâmetro "objet" diferente do especificado.')

    if (objet != 'MA' and objet != 'MI'):
        raise TypeError('Tipo de objetivo diferente do especificado.')

    if not isinstance(f_obj, (np.ndarray)):
        raise TypeError('Parâmetro "f_obj" diferente do especificado.')

    if not isinstance(restr_A, (np.ndarray)):
        raise TypeError('Parâmetro "restr_A" diferente do especificado.')

    if not isinstance(restr_op, (np.ndarray)):
        raise TypeError('Parâmetro "restr_op" diferente do especificado.')

    if not isinstance(restr_b, (np.ndarray)):
        raise TypeError('Parâmetro "restr_b" diferente do especificado.')

    flag = 0

    for i in range(len(restr_op)):  # verifica se será usado simplex ou simplex duas fases
        if restr_op[i] == '>=' or restr_op[i] == '==':
            flag = 1

    if flag == 1:

        readed(objet, f_obj, restr_A, restr_op, restr_b)
        print("__________MÉTODO SIMPLEX DUAS FASES SELECIONADO__________")
        answer = simplextwophase(objet, f_obj, restr_A, restr_op, restr_b)


if __name__ == "__main__":

    f = open("twophase.txt", "r")
    lines = f.readlines()

    for l in lines:
        if l == '\n':
            break
        if l[0] != '#':  # Cortesia do Professor: ignorar linhas iniciadas com o caractere '#'

            objet, f_obj, restricoesA, operadores, restricoesB = reader(l)
            solver(objet, f_obj, restricoesA, operadores, restricoesB)
