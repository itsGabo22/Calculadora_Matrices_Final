import numpy as np

def pedir_matriz(nombre):
    while True:
        try:
            filas = int(input(f"\nIngrese el número de filas de la matriz {nombre}: "))
            columnas = int(input(f"Ingrese el número de columnas de la matriz {nombre}: "))
            break
        except ValueError:
            print("⚠️ Por favor ingrese números enteros válidos para filas y columnas.")

    print(f"\nIngrese los elementos de la matriz {nombre} **fila por fila**.")
    print(f"Use espacios para separar los números. Ejemplo para 3 columnas: 1.5 2 3.7")

    elementos = []
    for i in range(filas):
        while True:
            fila_input = input(f"Fila {i + 1}: ")
            try:
                fila = list(map(float, fila_input.strip().split()))
                if len(fila) != columnas:
                    print(f"⚠️ Debe ingresar exactamente {columnas} valores. Intente de nuevo.")
                    continue
                elementos.append(fila)
                break
            except ValueError:
                print("⚠️ Asegúrese de ingresar solo números separados por espacios.")
    return np.array(elementos)

def sumar_matrices():
    A = pedir_matriz("A")
    B = pedir_matriz("B")
    if A.shape != B.shape:
        print("❌ Las matrices deben tener las mismas dimensiones.")
    else:
        print("✅ Resultado de A + B:")
        print(A + B)

def escalar_por_matriz():
    A = pedir_matriz("A")
    while True:
        try:
            escalar = float(input("Ingrese el escalar: "))
            break
        except ValueError:
            print("⚠️ Ingrese un número válido.")
    print(f"✅ Resultado de {escalar} * A:")
    print(escalar * A)

def suma_escalar_matrices():
    A = pedir_matriz("A")
    B = pedir_matriz("B")
    if A.shape != B.shape:
        print("❌ Las matrices deben tener las mismas dimensiones.")
        return
    while True:
        try:
            alpha = float(input("Ingrese escalar α para A: "))
            beta = float(input("Ingrese escalar β para B: "))
            break
        except ValueError:
            print("⚠️ Ingrese valores numéricos válidos.")
    resultado = alpha * A + beta * B
    print("✅ Resultado de αA + βB:")
    print(resultado)

def multiplicar_matrices():
    A = pedir_matriz("A")
    B = pedir_matriz("B")
    try:
        resultado = np.dot(A, B)
        print("✅ Resultado de A * B:")
        print(resultado)
    except ValueError:
        print("❌ Dimensiones incompatibles para la multiplicación.")

def determinante():
    A = pedir_matriz("A")
    if A.shape[0] != A.shape[1]:
        print("❌ La matriz debe ser cuadrada.")
    else:
        det = np.linalg.det(A)
        print("✅ Determinante de A:", det)

def inversa():
    A = pedir_matriz("A")
    if A.shape[0] != A.shape[1]:
        print("❌ La matriz debe ser cuadrada.")
    else:
        try:
            inv = np.linalg.inv(A)
            print("✅ Matriz inversa de A:")
            print(inv)
        except np.linalg.LinAlgError:
            print("❌ La matriz no es invertible (determinante = 0).")

def resolver_sistema():
    print("Para resolver AX = B:")
    A = pedir_matriz("A")
    B = pedir_matriz("B")
    if A.shape[0] != A.shape[1] or A.shape[0] != B.shape[0]:
        print("❌ A debe ser cuadrada y tener mismo número de filas que B.")
        return
    try:
        print("✅ Solución por matriz inversa:")
        X_inv = np.linalg.inv(A).dot(B)
        print("X =", X_inv)

        print("\n✅ Solución por método de Cramer:")
        detA = np.linalg.det(A)
        if detA == 0:
            print("❌ No se puede usar Cramer: determinante de A es 0.")
        else:
            n = A.shape[0]
            X_cramer = []
            for i in range(n):
                Ai = A.copy()
                Ai[:, i] = B[:, 0]  # Reemplaza la columna i con B
                Xi = np.linalg.det(Ai) / detA
                X_cramer.append(Xi)
            print("X =", np.array(X_cramer))
    except np.linalg.LinAlgError:
        print("❌ Error al resolver el sistema: matriz no invertible.")

def menu():
    while True:
        print("\n--- MENÚ DE OPERACIONES ---")
        print("1. Sumar matrices")
        print("2. Multiplicar matriz por escalar")
        print("3. Suma ponderada: αA + βB")
        print("4. Multiplicar matrices")
        print("5. Determinante de una matriz")
        print("6. Matriz inversa")
        print("7. Resolver sistema AX = B")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sumar_matrices()
        elif opcion == "2":
            escalar_por_matriz()
        elif opcion == "3":
            suma_escalar_matrices()
        elif opcion == "4":
            multiplicar_matrices()
        elif opcion == "5":
            determinante()
        elif opcion == "6":
            inversa()
        elif opcion == "7":
            resolver_sistema()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

menu()
