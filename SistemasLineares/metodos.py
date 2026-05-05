def gauss(A, b):
    n = len(A)

    for i in range(n):
        if A[i][i] == 0:
            raise Exception("Matriz singular")

        for j in range(i + 1, n):
            fator = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= fator * A[i][k]
            b[j] -= fator * b[i]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - soma) / A[i][i]

    return x


def jacobi(A, b, tol, max_iter):
    n = len(A)
    x = [0] * n

    for it in range(max_iter):
        x_new = x.copy()

        for i in range(n):
            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - soma) / A[i][i]

        erro = max(abs(x_new[i] - x[i]) for i in range(n))
        x = x_new

        if erro < tol:
            return x, it + 1

    raise Exception("Não convergiu")


def gauss_seidel(A, b, tol, max_iter):
    n = len(A)
    x = [0] * n

    for it in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            soma1 = sum(A[i][j] * x[j] for j in range(i))
            soma2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - soma1 - soma2) / A[i][i]

        erro = max(abs(x[i] - x_old[i]) for i in range(n))

        if erro < tol:
            return x, it + 1

    raise Exception("Não convergiu")