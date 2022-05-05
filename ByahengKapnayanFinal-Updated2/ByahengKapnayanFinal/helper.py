# needs SymPy installation to run.

from sympy import Matrix, lcm

def getCoeffs(N, factors, elements):
    "Constructs a matrix and gets the matrix nullspace. the nullspace corresponds to the coefficients of a balanced chem equation."
    
    # construct initial matrix
    eN = len(elements)
    matrix = [[0 for i in range(N)] for j in range(eN)]
    elemIndex = {}
    for i in range(eN):
        elemIndex[elements[i]] = i
    for col, elem, val in factors:
        matrix[elemIndex[elem]][col] = val
    #print(*matrix)

    # use sympy to get nullspace of matrix
    symMatrix = Matrix(matrix)
    coeffs = symMatrix.nullspace()[0]
    #print(*coeffs)

    # convert coefficients to its lowest integer form by using lcm
    multi = lcm([val.q for val in coeffs])
    coeffs = multi*coeffs
    
    return list(coeffs)

def processInput(s):
    "processes inputted chem equation."
    factors = []
    elements = []
    
    Sreactant, Sproduct = s.split("->")
    reactants = Sreactant.split("+")
    products = Sproduct.split("+")

    leftN = len(reactants)
    rightN = len(products)

    for i in range(leftN):
        addend = reactants[i]
        lst = addend.split("*")
        for factor in lst:
            elem, moles = factor.split("_")
            factors.append((i, elem, int(moles)))
            elements.append(elem)
    
    for i in range(rightN):
        addend = products[i]
        lst = addend.split("*")
        for factor in lst:
            elem, moles = factor.split("_")
            factors.append((i+leftN, elem, -int(moles)))
    
    return (leftN, rightN, factors, elements, reactants, products)
    
if __name__ == '__main__':
    # S_1+H_1*N_1*O_3->H_2*S_1*O_4+N_1*O_2+H_2*O_1
    nums = set([str(i) for i in range(9)])
    forb = set(['+', '-', '>', ' '])
    letters = [chr(i) for i in range(65, 91)]
    smallet = [chr(i) for i in range(97, 123)]

    f = open("unblnced_equations.txt", "r")
    pref = []
    formatted = []

    for nline in f.readlines():
        s = ''
        line = nline.strip() + ' '
        for i in range(len(line) - 1):
            if line[i] == ' ':
                continue
            s += line[i]
            if line[i] not in nums and line[i+1] in nums and line[i] not in forb and line[i+1] not in forb:
                s += '_'
            elif line[i] in nums and line[i+1] not in nums and line[i] not in forb and line[i+1] not in forb:
                s += '*'
            elif (line[i] in letters or line[i] in smallet) and line[i+1] in letters:
                s += '_1*'
            elif (line[i] in letters or line[i] in smallet) and line[i+1] == ' ':
                s += '_1'

        s += line[-1]

        pref.append(nline.strip())
        formatted.append(s)
    
    file = open("answerkey.txt", "w")

    c = 0 # for debugging
    for i in range(len(formatted)):
        print(c)
        leftN, rightN, factors, elements, reactants, products = processInput(formatted[i])
        coeff = getCoeffs(leftN + rightN, factors, elements)
        coefstr = ''
        for x in coeff:
            coefstr += str(x) + ' '

        file.write(pref[i] + ':' + coefstr.strip() + '\n')
        c += 1

    f.close()
    file.close()
    
