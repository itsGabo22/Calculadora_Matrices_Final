import customtkinter as ctk
import numpy as np
from tkinter import messagebox, Toplevel
from fractions import Fraction
from PIL import Image, ImageDraw, ImageTk
import io

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Calculadora de Operaciones con Matrices")
app.geometry("1300x800")

matriz_a_entries = []
matriz_b_entries = []
resultado_labels = []
historial_operaciones = []
entrada_actual = None

# --- Funciones ---
def generar_campos_matrices():
    for widget in matriz_frame.winfo_children():
        widget.destroy()

    try:
        filas_a = int(entry_filas_a.get())
        columnas_a = int(entry_columnas_a.get())
        filas_b = int(entry_filas_b.get())
        columnas_b = int(entry_columnas_b.get())
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar valores enteros en filas y columnas.")
        return

    frame_A = ctk.CTkFrame(matriz_frame)
    frame_A.grid(row=0, column=0, padx=20)
    ctk.CTkLabel(frame_A, text="Matriz A").grid(row=0, column=0, columnspan=columnas_a)

    ctk.CTkButton(frame_A, text="Ver Transpuesta", command=lambda: ver_transpuesta("A")).grid(row=1, column=0, columnspan=columnas_a, pady=(0, 5))
    ctk.CTkButton(frame_A, text="Ver Inversa", command=lambda: ver_inversa("A")).grid(row=2, column=0, columnspan=columnas_a, pady=(0, 5))
    ctk.CTkButton(frame_A, text="Determinante", command=lambda: ver_determinante("A")).grid(row=3, column=0, columnspan=columnas_a, pady=(0, 5))
    ctk.CTkButton(frame_A, text="Multiplicar por escalar", command=lambda: multiplicar_por_escalar("A")).grid(row=4, column=0, columnspan=columnas_a, pady=(0, 5))

    frame_B = ctk.CTkFrame(matriz_frame)
    frame_B.grid(row=0, column=1, padx=20)
    ctk.CTkLabel(frame_B, text="Matriz B").grid(row=0, column=0, columnspan=columnas_b)

    ctk.CTkButton(frame_B, text="Ver Transpuesta", command=lambda: ver_transpuesta("B")).grid(row=1, column=0, columnspan=columnas_b, pady=(0, 5))
    ctk.CTkButton(frame_B, text="Ver Inversa", command=lambda: ver_inversa("B")).grid(row=2, column=0, columnspan=columnas_b, pady=(0, 5))
    ctk.CTkButton(frame_B, text="Determinante", command=lambda: ver_determinante("B")).grid(row=3, column=0, columnspan=columnas_b, pady=(0, 5))
    ctk.CTkButton(frame_B, text="Multiplicar por escalar", command=lambda: multiplicar_por_escalar("B")).grid(row=4, column=0, columnspan=columnas_b, pady=(0, 5))

    matriz_a_entries.clear()
    matriz_b_entries.clear()

    for i in range(filas_a):
        fila_a = []
        for j in range(columnas_a):
            entry_a = ctk.CTkEntry(frame_A, width=50)
            entry_a.grid(row=i+5, column=j, padx=3, pady=3)
            entry_a.bind("<FocusIn>", lambda e, r=i, c=j: set_entrada_actual("A", r, c))
            fila_a.append(entry_a)
        matriz_a_entries.append(fila_a)

    for i in range(filas_b):
        fila_b = []
        for j in range(columnas_b):
            entry_b = ctk.CTkEntry(frame_B, width=50)
            entry_b.grid(row=i+5, column=j, padx=3, pady=3)
            entry_b.bind("<FocusIn>", lambda e, r=i, c=j: set_entrada_actual("B", r, c))
            fila_b.append(entry_b)
        matriz_b_entries.append(fila_b)

# ... (mantén las funciones set_entrada_actual, mover_cursor, obtener_matriz, mostrar_resultado_en_tabla, 
# ver_transpuesta, ver_inversa, ver_determinante, determinante_por_sarrus, intercambiar_matrices, 
# actualizar_historial como están en tu código original)

def multiplicar_por_escalar(matriz_id):
    entries = matriz_a_entries if matriz_id == "A" else matriz_b_entries
    matriz = obtener_matriz(entries)
    if matriz is None:
        return
    
    # Ventana emergente para pedir el escalar
    dialogo = ctk.CTkInputDialog(text=f"Ingrese el escalar para multiplicar matriz {matriz_id}:",
                                title="Multiplicación por escalar")
    escalar = dialogo.get_input()
    
    try:
        escalar = float(escalar)
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Debe ingresar un número válido")
        return
    
    resultado = escalar * matriz
    mostrar_resultado_en_tabla(resultado)
    actualizar_historial(f"Matriz {matriz_id} multiplicada por {escalar}")

def ejecutar_operacion(event=None):
    operacion = operacion_var.get()
    
    # Operaciones que solo necesitan una matriz
    operaciones_unarias = [
        "determinante A", "determinante B",
        "inversa A", "inversa B",
        "sarrus A", "sarrus B"
    ]
    
    # Obtener matriz A si es necesaria
    if any(op in operacion for op in ["A", "sumar", "restar", "multiplicar"]):
        A = obtener_matriz(matriz_a_entries)
        if A is None:
            return
    
    # Obtener matriz B si es necesaria
    if any(op in operacion for op in ["B", "sumar", "restar", "multiplicar"]):
        B = obtener_matriz(matriz_b_entries)
        if B is None and operacion not in operaciones_unarias:
            return
    
    try:
        if operacion == "sumar":
            if A.shape != B.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones.")
            resultado = A + B
        elif operacion == "restar":
            if A.shape != B.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones.")
            resultado = A - B
        elif operacion == "multiplicar":
            if A.shape[1] != B.shape[0]:
                raise ValueError("Columnas de A deben coincidir con filas de B.")
            resultado = np.dot(A, B)
        elif operacion == "determinante A":
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz A debe ser cuadrada.")
            resultado = np.linalg.det(A)
        elif operacion == "determinante B":
            if B.shape[0] != B.shape[1]:
                raise ValueError("La matriz B debe ser cuadrada.")
            resultado = np.linalg.det(B)
        elif operacion == "inversa A":
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz A debe ser cuadrada.")
            resultado = np.linalg.inv(A)
        elif operacion == "inversa B":
            if B.shape[0] != B.shape[1]:
                raise ValueError("La matriz B debe ser cuadrada.")
            resultado = np.linalg.inv(B)
        elif operacion == "sarrus A":
            resultado = determinante_por_sarrus(A)
        elif operacion == "sarrus B":
            resultado = determinante_por_sarrus(B)
        else:
            raise ValueError("Operación no válida.")
        
        mostrar_resultado_en_tabla(resultado)
        actualizar_historial(f"Operación: {operacion}")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))
def determinante_por_sarrus(matriz, matriz_id="A"):
    if matriz.shape != (3, 3):
        raise ValueError("La matriz debe ser 3x3 para aplicar la regla de Sarrus.")
    
    # Extraer elementos
    a = matriz
    a11, a12, a13 = a[0,0], a[0,1], a[0,2]
    a21, a22, a23 = a[1,0], a[1,1], a[1,2]
    a31, a32, a33 = a[2,0], a[2,1], a[2,2]
    
    # Calcular términos
    term_pos1 = a11 * a22 * a33
    term_pos2 = a12 * a23 * a31
    term_pos3 = a13 * a21 * a32
    term_neg1 = a13 * a22 * a31
    term_neg2 = a11 * a23 * a32
    term_neg3 = a12 * a21 * a33
    det = term_pos1 + term_pos2 + term_pos3 - term_neg1 - term_neg2 - term_neg3
    
    # Crear ventana de explicación
    explicacion = ctk.CTkToplevel(app)
    explicacion.title(f"Regla de Sarrus - Matriz {matriz_id}")
    explicacion.geometry("600x650")
    
    # Frame principal con scroll
    main_frame = ctk.CTkFrame(explicacion)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título
    ctk.CTkLabel(main_frame, 
                text=f"Matriz extendida (para Sarrus):",
                font=("Arial", 14, "bold")).pack(pady=(10,5), anchor="w")
    
    # Matriz extendida
    matriz_ext_str = f"{a11:.2f}  {a12:.2f}  {a13:.2f}  {a11:.2f}  {a12:.2f}\n" \
                    f"{a21:.2f}  {a22:.2f}  {a23:.2f}  {a21:.2f}  {a22:.2f}\n" \
                    f"{a31:.2f}  {a32:.2f}  {a33:.2f}  {a31:.2f}  {a32:.2f}"
    
    ctk.CTkLabel(main_frame, 
                text=matriz_ext_str,
                font=("Courier", 14)).pack(anchor="w")
    
    # Separador
    ctk.CTkLabel(main_frame, text="-"*50).pack(pady=10)
    
    # Términos positivos
    ctk.CTkLabel(main_frame, 
                text="Términos positivos (diagonales principales):",
                font=("Arial", 14, "bold")).pack(anchor="w")
    
    term1_str = f"+ {a11:.2f} × {a22:.2f} × {a33:.2f} = {term_pos1:.2f}"
    term2_str = f"+ {a12:.2f} × {a23:.2f} × {a31:.2f} = {term_pos2:.2f}"
    term3_str = f"+ {a13:.2f} × {a21:.2f} × {a32:.2f} = {term_pos3:.2f}"
    
    ctk.CTkLabel(main_frame, text=term1_str, font=("Courier", 14)).pack(anchor="w")
    ctk.CTkLabel(main_frame, text=term2_str, font=("Courier", 14)).pack(anchor="w")
    ctk.CTkLabel(main_frame, text=term3_str, font=("Courier", 14)).pack(anchor="w")
    
    # Separador
    ctk.CTkLabel(main_frame, text="-"*50).pack(pady=10)
    
    # Términos negativos
    ctk.CTkLabel(main_frame, 
                text="Términos negativos (diagonales secundarias):",
                font=("Arial", 14, "bold")).pack(anchor="w")
    
    term4_str = f"- {a13:.2f} × {a22:.2f} × {a31:.2f} = -{term_neg1:.2f}"
    term5_str = f"- {a11:.2f} × {a23:.2f} × {a32:.2f} = -{term_neg2:.2f}"
    term6_str = f"- {a12:.2f} × {a21:.2f} × {a33:.2f} = -{term_neg3:.2f}"
    
    ctk.CTkLabel(main_frame, text=term4_str, font=("Courier", 14)).pack(anchor="w")
    ctk.CTkLabel(main_frame, text=term5_str, font=("Courier", 14)).pack(anchor="w")
    ctk.CTkLabel(main_frame, text=term6_str, font=("Courier", 14)).pack(anchor="w")
    
    # Separador
    ctk.CTkLabel(main_frame, text="-"*50).pack(pady=10)
    
    # Cálculo final
    ctk.CTkLabel(main_frame, 
                text="Cálculo del determinante:",
                font=("Arial", 14, "bold")).pack(anchor="w")
    
    calc_str = f"{term_pos1:.2f} + {term_pos2:.2f} + {term_pos3:.2f} " \
               f"- {term_neg1:.2f} - {term_neg2:.2f} - {term_neg3:.2f} = {det:.2f}"
    
    ctk.CTkLabel(main_frame, 
                text=calc_str,
                font=("Courier", 14, "bold")).pack(anchor="w")
    
    # Resultado final
    ctk.CTkLabel(main_frame, 
                text=f"\nResultado final: {det:.2f}",
                font=("Arial", 16, "bold")).pack(pady=10)
    
    # Botón para cerrar
    ctk.CTkButton(main_frame, 
                 text="Cerrar", 
                 command=explicacion.destroy).pack(pady=10)
    
    return det

def visualizar_sarrus(matriz):
    # Crear una imagen para mostrar las diagonales
    img = Image.new("RGB", (600, 300), "white")
    draw = ImageDraw.Draw(img)
    
    # Extraer elementos
    a = matriz
    elements = [
        [a[0,0], a[0,1], a[0,2], a[0,0], a[0,1]],
        [a[1,0], a[1,1], a[1,2], a[1,0], a[1,1]],
        [a[2,0], a[2,1], a[2,2], a[2,0], a[2,1]]
    ]
    
    # Dibujar la matriz extendida
    for i in range(3):
        for j in range(5):
            x = 100 + j * 80
            y = 50 + i * 80
            draw.rectangle([x-30, y-15, x+30, y+15], outline="black")
            draw.text((x, y), f"{elements[i][j]:.1f}", fill="black", anchor="center")
    
    # Dibujar líneas para diagonales positivas (verde)
    for i in range(3):
        # Diagonal principal 1
        x1 = 100 + i * 80 - 30
        y1 = 50 + i * 80 - 15
        x2 = 100 + i * 80 + 30
        y2 = 50 + i * 80 + 15
        draw.line([x1, y1, x2, y2], fill="green", width=3)
        
        # Otras diagonales positivas
        if i < 2:
            x1 = 100 + (i+1) * 80 - 30
            y1 = 50 + i * 80 - 15
            x2 = 100 + (i+1) * 80 + 30
            y2 = 50 + i * 80 + 15
            draw.line([x1, y1, x2, y2], fill="green", width=3)
    
    # Dibujar líneas para diagonales negativas (rojo)
    for i in range(3):
        # Diagonal secundaria 1
        x1 = 100 + (2-i) * 80 - 30
        y1 = 50 + i * 80 - 15
        x2 = 100 + (2-i) * 80 + 30
        y2 = 50 + i * 80 + 15
        draw.line([x1, y1, x2, y2], fill="red", width=3)
        
        # Otras diagonales negativas
        if i < 2:
            x1 = 100 + (3-i) * 80 - 30
            y1 = 50 + i * 80 - 15
            x2 = 100 + (3-i) * 80 + 30
            y2 = 50 + i * 80 + 15
            draw.line([x1, y1, x2, y2], fill="red", width=3)
    
    # Añadir leyenda
    draw.text((50, 250), "Verde: Términos positivos", fill="green")
    draw.text((300, 250), "Rojo: Términos negativos", fill="red")
    
    return img

# --- Interfaz ---
titulo = ctk.CTkLabel(app, text="Calculadora de Operaciones con Matrices", font=("Arial", 20))
titulo.pack(pady=10)

filas_columnas_frame = ctk.CTkFrame(app)
filas_columnas_frame.pack(pady=10)

ctk.CTkLabel(filas_columnas_frame, text="Filas A").grid(row=0, column=0, padx=5)
entry_filas_a = ctk.CTkEntry(filas_columnas_frame, width=60)
entry_filas_a.grid(row=0, column=1, padx=5)

ctk.CTkLabel(filas_columnas_frame, text="Columnas A").grid(row=0, column=2, padx=5)
entry_columnas_a = ctk.CTkEntry(filas_columnas_frame, width=60)
entry_columnas_a.grid(row=0, column=3, padx=5)

ctk.CTkLabel(filas_columnas_frame, text="Filas B").grid(row=1, column=0, padx=5)
entry_filas_b = ctk.CTkEntry(filas_columnas_frame, width=60)
entry_filas_b.grid(row=1, column=1, padx=5)

ctk.CTkLabel(filas_columnas_frame, text="Columnas B").grid(row=1, column=2, padx=5)
entry_columnas_b = ctk.CTkEntry(filas_columnas_frame, width=60)
entry_columnas_b.grid(row=1, column=3, padx=5)

ctk.CTkButton(app, text="Generar campos de matrices", command=generar_campos_matrices).pack(pady=10)
ctk.CTkButton(app, text="Intercambiar matrices", command=intercambiar_matrices).pack(pady=5)

matriz_frame = ctk.CTkFrame(app, fg_color="transparent")
matriz_frame.pack(pady=10)

opciones_frame = ctk.CTkFrame(app)
opciones_frame.pack(pady=10)

operacion_var = ctk.StringVar(value="sumar")
combo_operacion = ctk.CTkComboBox(opciones_frame, 
                                 values=[
                                     "sumar", 
                                     "restar", 
                                     "multiplicar", 
                                     "sarrus A", 
                                     "sarrus B",
                                 ], 
                                 variable=operacion_var)
combo_operacion.grid(row=0, column=0, padx=5)

formato_var = ctk.StringVar(value="decimal")
combo_formato = ctk.CTkComboBox(opciones_frame, values=["entero", "decimal", "fracción"], variable=formato_var)
combo_formato.grid(row=0, column=1, padx=5)

ctk.CTkButton(app, text="Ejecutar operación", command=ejecutar_operacion).pack(pady=10)
app.bind("<Return>", ejecutar_operacion)
app.bind("<Up>", lambda e: mover_cursor("arriba"))
app.bind("<Down>", lambda e: mover_cursor("abajo"))
app.bind("<Left>", lambda e: mover_cursor("izquierda"))
app.bind("<Right>", lambda e: mover_cursor("derecha"))

resultado_frame = ctk.CTkFrame(app)
resultado_frame.pack(pady=10)

historial_frame = ctk.CTkFrame(app)
historial_frame.pack(pady=10)
ctk.CTkLabel(historial_frame, text="Historial de operaciones").pack()
historial_textbox = ctk.CTkTextbox(historial_frame, height=150, width=600)
historial_textbox.pack()

app.mainloop()