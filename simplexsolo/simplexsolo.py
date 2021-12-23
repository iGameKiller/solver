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


def readed(objet, f_obj, restr_a, restr_op, restr_b):
    if objet == "MA":
        print("Objetivo: Maximizar")
    elif objet == 'MI':
        print("Objetivo: Minimizar")
    print("Números da função objetivo", f_obj)
    print("Matriz de Restrições A: ")
    print(restr_a)
    print("Operadores: ", restr_op)
    print("Matriz de Restrições B: ")
    print(restr_b)


def gaussonephase(matrix, minorcolpos, lin, col):
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


def tableau(objet, f_obj, restr_a, restr_op, restr_b):
    lin = len(restr_op) + 1
    col = len(f_obj) + len(restr_op) + 1
    matrix = np.zeros([lin, col])
    idmatrix = np.zeros([len(restr_op), len(restr_op)])

    for i in range(len(f_obj)):  # Posicionando a função objetivo
        if objet == 'MA':
            matrix[0, i + 1] = -f_obj[i]
        elif objet == 'MI':
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

    for i in range(len(restr_b)):  # Posicionando a matriz identidade
        for j in range(len(restr_b[i])):
            matrix[i + 1][len(restr_a) + 1 + j] = idmatrix[i][j]

    return matrix


def simplexonephase(objet, f_obj, restr_a, restr_op, restr_b):
    lin = len(f_obj) + 1
    col = (len(f_obj) * 2) + 1

    matrix = tableau(objet, f_obj, restr_a, restr_op, restr_b)

    allpositives = False
    itcounter = 0

    while not allpositives:
        itcounter = itcounter + 1
        ngtvcounter = 0  # Conta a quantidade de valores negativos existentes
        minorvalue = matrix[0][0]  # Procura o menor número na primeira linha
        minorColPos = 0
        for i in range(col - 1):  # encontrando o menor valor na primeira linha, correspondente a função objetivo
            if matrix[0][i] < 0:
                ngtvcounter = ngtvcounter + 1
            if matrix[0][i] < minorvalue:
                minorvalue = matrix[0][i]
                minorColPos = i

        print("____________________________ITERAÇÃO", itcounter, "_____________________________")
        print(matrix)
        matrix = gaussonephase(matrix, minorColPos, lin, col)
        if len(matrix) == 1:
            if matrix[0] == -1:
                allpositives = True
        if ngtvcounter == 0:
            allpositives = True

    if objet == 'MA':
        answer = matrix[0]
    elif objet == 'MI':
        answer = -matrix[0]

    return answer


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

    readed(objet, f_obj, restr_A, restr_op, restr_b)
    print("__________________________MÉTODO SIMPLEX____________________________")

    answer = simplexonephase(objet, f_obj, restr_A, restr_op, restr_b)
    for i in range(len(answer)):
        if i != 0:
            print("X", i, "=", "%.1f" % answer[i])
        else:
            print("A solução ótima da Função Objetivo é", "%.1f" % answer[i])



if __name__ == "__main__":

    f = open("simplexsolo.txt", "r")
    lines = f.readlines()
    i = 0
    for l in lines:
        if l == '\n':
            break
        if l[0] != '#':  # Cortesia do Professor: ignorar linhas iniciadas com o caractere '#'
            i = i + 1
            print("Problema",i)
            objet, f_obj, restricoesA, operadores, restricoesB = reader(l)
            solver(objet, f_obj, restricoesA, operadores, restricoesB)
            print("__________________________________________________________________")
            print("__________________________________________________________________")