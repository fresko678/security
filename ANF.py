def ANFform(variables, truthvalues):

    n_vars = len(variables)
    n_values = len(truthvalues)

    if n_values != 2 ** n_vars:
        raise ValueError("The number of truth values must be equal to 2^%d, "
                         "got %d" % (n_vars, n_values))

    coeffs = anf_coeffs(truthvalues)
    terms = anf_terms(variables)

    res = ''
    for i in list(range(len(coeffs))):
        if coeffs[i] == 1:
            res += terms[i] + ' {} '.format(chr(8853))

    if res == '':
        return '1'
    else:
        return res[:-3]


def anf_coeffs(truthvalues) -> list:
    s = '{0:b}'.format(len(truthvalues))
    n = len(s) - 1

    if len(truthvalues) != 2 ** n:
        raise ValueError("The number of truth values must be a power of two, "
                         "got %d" % len(truthvalues))

    coeffs = [[v] for v in truthvalues]

    for i in range(n):
        tmp = []
        for j in range(2 ** (n - i - 1)):
            tmp.append(coeffs[2 * j] +
                       list(map(lambda x, y: x ^ y, coeffs[2 * j], coeffs[2 * j + 1])))
        coeffs = tmp

    return coeffs[0]


def anf_terms(variables) -> list:
    n_vars = len(variables)
    template = '{' + ':0{n}d'.format(n=n_vars) + '}'
    res = []
    for i in list(range(2**n_vars)):
        res.append(template.format(int(bin(i)[2:])))

    for i in list(range(len(res))):
        tmp = ''
        for j in list(range(n_vars)):
            if res[i][j] == '1':
                tmp += variables[j]
        if tmp == '':
            res[i] = '1'
        else:
            res[i] = tmp

    return res
