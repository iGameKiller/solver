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
    print("Matriz de Restrições A:")
    print(restr_a)
    print("Operadores: ", restr_op)
    print("Matriz de Restrições B: ")
    print(restr_b)


def gauss(matrix, mayorColPos, lin, col):
    pivots = []
    phasetwo = False
    for i in range(1, len(matrix)):  # montando array de linhas pivô
        newnum = matrix[i][0] / matrix[i][mayorColPos]
        if newnum < 0:
            phasetwo = True
            return phasetwo, matrix
        pivots.append(newnum)


    pivotMinorValue = pivots[0]
    pivotMinorValuePos = 0

    for i in range(len(pivots)):  # encontrando o menor valor do vetor de pivôs e sua posição
        if pivots[i] < pivotMinorValue:
            pivotMinorValue = pivots[i]
            pivotMinorValuePos = i

    pivotline = matrix[pivotMinorValuePos + 1]  # fazendo uma cópia da linha pivô da matriz
    pivotElement = matrix[pivotMinorValuePos + 1][mayorColPos]

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
            magicNumber = matrix[i][mayorColPos]
            lineCopy = matrix[i]

            for j in range(col):
                if j == len(matrix[i]):
                    break
                else:
                    lineCopy[j] = matrix[i][j] - (magicNumber * pivotline[j])

    return phasetwo, matrix


def constructor(f_obj, restr_a, restr_op, restr_b):

    A_var = []
    S_var = []

    for i in range(len(restr_op)):
        if restr_op[i] == '<=':
            data = (i, 1)
            S_var.append(data)

        elif restr_op[i] == '>=':
            data = (i, -1)
            S_var.append(data)

            data = (i, 1)
            A_var.append(data)

        elif restr_op[i] == '==':
            data = (i, 1)
            A_var.append(data)

    lin = len(restr_op) + 2
    col = len(f_obj) + len(S_var) + len(A_var) + 1

    matrix = np.zeros((lin, col))

    restr_A = np.zeros((len(restr_a), len(f_obj)))  # Transformando restrições sem tipo em numéricas
    for i in range(len(restr_a)):
        for j in range(len(restr_a[i])):
            restr_A[i][j] = float(restr_a[i][j])

    for i in range(len(restr_A)):  # Posicionando a matriz A de restrições
        for j in range(len(restr_A[i])):
            matrix[i + 1][j + 1] = restr_A[i][j]

    for i in range(len(restr_b)):  # Posicionando matriz B de restrições
        matrix[i + 1][0] = restr_b[i]

    if len(S_var) > 0: # Posicionando variáveis de folga
        S_matrix = np.zeros((len(restr_op), len(S_var)))

        aux = 0
        for i in range(len(S_var)):
            S_matrix[S_var[i][0]][aux] = S_var[i][1]
            aux = aux + 1

        for i in range(len(S_matrix)):
            for j in range(len(S_matrix[i])):
                matrix[i + 1][len(f_obj) + 1 + j] = S_matrix[i][j]

    if len(A_var) > 0: # Posicionando variáveis artificiais
        A_matrix = np.zeros((len(restr_op), len(A_var)))

        aux = 0
        for i in range(len(A_var)):
            A_matrix[A_var[i][0]][aux] = A_var[i][1]
            aux = aux + 1

        for i in range(len(A_matrix)):
            for j in range(len(A_matrix[i])):
                matrix[i + 1][len(f_obj) + len(S_var) + 1 + j] = A_matrix[i][j]

    for i in range(len(matrix[0])-len(A_var), len(matrix[0])): # Posicionando função objetivo nova
        matrix[0][i] = 1

    for i in range(len(A_var)): # Posicionando soma das linhas com variáveis artificiais
        for j in range(col-len(A_var)):
            matrix[lin-1][j] += matrix[A_var[i][0]+1][j]

    return matrix,A_var,S_var


def phasetwo():
    print("__________________________FASE 2_________________________")

def simplextwophase(objet, f_obj, restr_a, restr_op, restr_b):

    matrix, A_var, S_var = constructor(f_obj, restr_a, restr_op, restr_b)

    lin = len(restr_op) + 2
    col = len(f_obj) + len(S_var) + len(A_var) + 1
    print("__________________________TABLEAU INICIAL_________________________")
    print(matrix)
    allminorequalzero = False
    phase = False
    itcounter = 0
    print("__________________________FASE 1_________________________")

    while allminorequalzero == False:

        itcounter = itcounter + 1
        mayorvalue = matrix[0][0]  # Procura o maior número na ultima linha
        mayorColPos = 0

        for i in range(1, col - 1):  # encontrando o menor valor na ultima linha

            if matrix[lin-1][i] > mayorvalue:
                mayorvalue = matrix[lin-1][i]
                mayorColPos = i

        print("____________________________ITERAÇÃO", itcounter, "_____________________________")
        phase, matrix = gauss(matrix, mayorColPos, lin, col)

        if phase == True:
            phasetwo()
            return 1
        else:
            print(matrix)

    return matrix


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
        print(answer)


if __name__ == "__main__":

    f = open("twophase.txt", "r")
    lines = f.readlines()

    for l in lines:
        if l == '\n':
            break
        if l[0] != '#':  # Cortesia do Professor: ignorar linhas iniciadas com o caractere '#'

            objet, f_obj, restricoesA, operadores, restricoesB = reader(l)
            solver(objet, f_obj, restricoesA, operadores, restricoesB)
