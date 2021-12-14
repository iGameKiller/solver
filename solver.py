import numpy as np

np.set_printoptions(suppress=True, precision=2)


def construct(objet, f_obj, restr_a, restr_b):
    if (len(f_obj) == len(restr_a)):
        lin = len(f_obj) + 1
        col = (len(f_obj) * 2) + 1
        matrix = np.zeros([lin, col])
        idmatrix = np.zeros([len(restr_a), len(restr_a)])

        for i in range(len(f_obj)):  # Posicionando a função objetivo
            if objet == 'MA':
                matrix[0, i + 1] = -f_obj[i]
            elif objet == 'MI':
                matrix[0, i + 1] = f_obj[i]

        for i in range(len(restr_b)):  # Posicionando a matriz A de restrições
            for j in range(len(restr_b)):
                matrix[i + 1][j + 1] = restr_a[i][j]
                if i == j:
                    idmatrix[i][j] = 1

        for i in range(len(restr_b)):  # Posicionando matriz B de restrições
            matrix[i + 1][0] = restr_b[i]

        for i in range(len(restr_b)):  # Posicionando a matriz identidade
            for j in range(len(restr_b)):
                matrix[i + 1][lin + j] = idmatrix[i][j]

        return matrix

    elif len(restr_a) > len(f_obj):

        extraCol = len(restr_a) - len(f_obj)
        lin = len(f_obj)
        col = (len(restr_a)+extraCol)
        matrix = np.zeros([len(restr_a) + 1, (col + extraCol + 1)])
        idmatrix = np.zeros([len(restr_a), len(restr_a)])

        for i in range(len(f_obj)):  # Posicionando a função objetivo
            if (objet == 'MA'):
                matrix[0, i + 1] = -f_obj[i]
            elif (objet == 'MI'):
                matrix[0, i + 1] = f_obj[i]

        for i in range(len(restr_a)):  # Posicionando a matriz A de restrições
            for j in range(len(restr_a[i])):
                matrix[i + 1][j + 1] = restr_a[i][j]

        for i in range(len(restr_b)):  # Posicionando matriz B de restrições
            matrix[i + 1][0] = restr_b[i]

        for i in range(len(idmatrix)):  # Setando a Matriz Identidade
            for j in range(len(idmatrix[i])):
                if i == j:
                    idmatrix[i][j] = 1

        for i in range(len(idmatrix)): # Posicionando a Matriz Identidade
            for j in range(len(idmatrix[i])):
                matrix[(lin-1)+i][(col-1)+j] = idmatrix[i][j]

        return matrix

    elif len(restr_a) < len(f_obj):

        extraCol = len(f_obj) - len(restr_a)
        lin = len(f_obj)
        col = (len(restr_a))
        matrix = np.zeros([len(restr_a) + 1, (col + lin + extraCol)])
        idmatrix = np.zeros([col, col])

        for i in range(len(f_obj)):  # Posicionando a função objetivo
            if (objet == 'MA'):
                matrix[0, i + 1] = -f_obj[i]
            elif (objet == 'MI'):
                matrix[0, i + 1] = f_obj[i]

        for i in range(col):  # Posicionando a matriz A de restrições
            steps = len(restr_a[i])
            for j in range(steps):
                matrix[i + 1][j + 1] = restr_a[i][j]

        for i in range(col):  # Posicionando matriz B de restrições
            matrix[i + 1][0] = restr_b[i]

        for i in range(col):  # Setando a Matriz Identidade
            for j in range(len(idmatrix[i])):
                if i == j:
                    idmatrix[i][j] = 1

        for i in range(len(idmatrix)): # Posicionando a Matriz Identidade
            for j in range(len(idmatrix[i])):
                matrix[(col-2) + i][(lin+1)+j] = idmatrix[i][j]

        return matrix


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


def twophase(objet, f_obj, restr_A, restr_op, restr_b):
    print("Two phase here")
    matrix = np.array([-1])
    return matrix


def simplex(objet, f_obj, restr_A, restr_b):
    lin = len(f_obj) + 1
    col = (len(f_obj) * 2) + 1
    matrix = construct(objet, f_obj, restr_A, restr_b)
    allpositives = False

    while not allpositives:
        ngtvcounter = 0  # Conta a quantidade de valores negativos existentes
        minorvalue = matrix[0][0]  # Procura o menor número na primeira linha
        minorColPos = 0
        for i in range(col-1):  # encontrando o menor valor na primeira linha, correspondente a função objetivo
            if matrix[0][i] < 0:
                ngtvcounter = ngtvcounter + 1
            if matrix[0][i] < minorvalue:
                minorvalue = matrix[0][i]
                minorColPos = i

        print("___________________________________________")
        print(matrix)
        matrix = gauss(matrix, minorColPos, lin, col)
        if len(matrix) == 1:
            if matrix[0] == -1:
                allpositives = True
        if ngtvcounter == 0:
            allpositives = True

    if(objet == 'MA'):
        answer = matrix[0]
    elif(objet == 'MI'):
        answer = -matrix[0]

    return answer


def filter(line):
    #PATROCINADO
    # índices (posições) de expressões em strings
    ind_fo = line.index('RE')
    ind_re = line.index('SF')

    # substrings
    objet = line[0:2]
    fo = line[3: ind_fo - 2]
    re = line[ind_fo: ind_re]

    f_obj = []
    fo_split = fo[0:].split()
    for i in fo_split:
        f_obj.append(float(i))

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

    for i in range(len(rest_array)):
        aux_a = []
        aux_b = []
        for j in range(len(rest_array[i])):
            if rest_array[i][j] == '<=' or rest_array[i][j] == '>=' or rest_array[i][j] == '==':
                restr_op.append(rest_array[i][j])
                aux_b.append(float(rest_array[i][j+1]))
                break

            aux_a.append(float(rest_array[i][j]))

        restr_A.append(aux_a)
        restr_b.append(aux_b)

    f_obj = np.asarray(f_obj)
    restricoesA = np.asarray(restr_A)
    operadores = np.asarray(restr_op)
    restricoesB = np.asarray(restr_b)

    return objet, f_obj, restricoesA, operadores, restricoesB


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

    answer = []
    if flag == 0:
        answer = simplex(objet, f_obj, restr_A, restr_b)
        for i in range(len(answer)):
            if i != 0:
                print("X",i, "=", "%.1f" % answer[i])
            else:
                print("A solução ótima da Função Objetivo vale", "%.1f" % answer[i])
    elif flag == 1:
        answer = twophase(objet, f_obj, restr_A, restr_op, restr_b)


if __name__ == "__main__":

    f = open("tests.txt", "r")
    lines = f.readlines()

    for l in lines:
        if l == '\n':
            break
        elif l[0] != '#':  # ignorar linhas iniciadas com o caractere '#'

            objet, f_obj, restricoesA, operadores, restricoesB = filter(l)
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

            solver(objet, f_obj, restricoesA, operadores, restricoesB)
            print("___________________________________________")
            print("___________________________________________")