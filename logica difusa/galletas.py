# Programar un controlador difuso que permita calcular la temperatura con la cual se deben hornear unas galletas La temperatura del horno debe estar entre 0 y 30 grados. 

# Para determinar la temperatura del horno se captura mediante una camara el nivel cromático de las galletas, dependiendo del nivel de programa la temperatura. Para la temperatura se tienen 3 etiquetas linguisticas, así: alta, moderada y baja.

# El nivel cromático se mide entre 0 y 10, y tiene 2 etiquetas linguisticas, cruda, semicruda y dorada.También se han definido las siguientes reglas:

# R1: Si las galletas están crudas entonces la temperatura del horno es alta
# R2: Si las galletas están semicrudas entonces la temperatura del horno es moderada.
# R3: Si las galletas están doradas entonces temperatura baja
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Definición de las variables difusas
nivel_cromatico = ctrl.Antecedent(np.arange(0, 11, 0.5), 'nivel_cromatico')
temperatura = ctrl.Consequent(np.arange(0, 31, 0.5), 'temperatura')

# Definición de las funciones de pertenencia para nivel cromático
nivel_cromatico['cruda'] = fuzz.trimf(nivel_cromatico.universe, [0, 0, 4])
nivel_cromatico['semicruda'] = fuzz.trimf(nivel_cromatico.universe, [3, 5, 7])
nivel_cromatico['dorada'] = fuzz.trimf(nivel_cromatico.universe, [6, 10, 10])

# Definición de las funciones de pertenencia para temperatura
temperatura['baja'] = fuzz.trimf(temperatura.universe, [0, 0, 10])
temperatura['moderada'] = fuzz.trimf(temperatura.universe, [8, 15, 20])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [18, 30, 30])


# Definición de las reglas difusas
rule1 = ctrl.Rule(nivel_cromatico['cruda'], temperatura['alta'])
rule2 = ctrl.Rule(nivel_cromatico['semicruda'], temperatura['moderada'])
rule3 = ctrl.Rule(nivel_cromatico['dorada'], temperatura['baja'])

# Creación del sistema de control difuso
controlador_temp = ctrl.ControlSystem([rule1, rule2, rule3])
simulador_temp = ctrl.ControlSystemSimulation(controlador_temp)

# Función que calcula la temperatura basada en el nivel cromático
def calcular_temperatura():
    try:
        nivel = float(nivel_cromatico_entry.get())
        simulador_temp.input['nivel_cromatico'] = nivel
        simulador_temp.compute()
        
        # Obtener la salida
        temp_resultado = simulador_temp.output['temperatura']
        temperatura_resultado.set(f"{temp_resultado:.2f} grados")
        
  
        # Cálculo detallado
        nivel_cromatico_vals = {
            'cruda': fuzz.interp_membership(nivel_cromatico.universe, nivel_cromatico['cruda'].mf, nivel),
            'semicruda': fuzz.interp_membership(nivel_cromatico.universe, nivel_cromatico['semicruda'].mf, nivel),
            'dorada': fuzz.interp_membership(nivel_cromatico.universe, nivel_cromatico['dorada'].mf, nivel)
        }
        
        # Mostrar valores de pertenencia
        pertenencia_texto = (
            f"Nivel Cromático 'cruda': {nivel_cromatico_vals['cruda']:.2f}\n"
            f"Nivel Cromático 'semicruda': {nivel_cromatico_vals['semicruda']:.2f}\n"
            f"Nivel Cromático 'dorada': {nivel_cromatico_vals['dorada']:.2f}"
        )
        pertenencia_resultado.set(pertenencia_texto)
        
        # # Valores de las reglas
        # activeRule1 = np.fmin(nivel_cromatico_vals['cruda'], temperatura['alta'].mf)
        # activeRule2 = np.fmin(nivel_cromatico_vals['semicruda'], temperatura['moderada'].mf)
        # activeRule3 = np.fmin(nivel_cromatico_vals['dorada'], temperatura['baja'].mf)
        
        # # Mostrar valores de las reglas
        # reglas_texto = (
        #     f"Regla 1 (cruda -> alta): {np.max(activeRule1):.2f}\n"
        #     f"Regla 2 (semicruda -> moderada): {np.max(activeRule2):.2f}\n"
        #     f"Regla 3 (dorada -> baja): {np.max(activeRule3):.2f}"
        # )
        # reglas_resultado.set(reglas_texto)

        temperatura.view(sim=simulador_temp)
        plt.show()
        
       
        
        
    except Exception as e:
        temperatura_resultado.set("Error en la entrada")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Controlador Difuso de Temperatura para Hornear Galletas")

# Etiqueta y campo de entrada para el nivel cromático
ttk.Label(root, text="Nivel Cromático (0-10):").grid(column=0, row=0, padx=10, pady=10)
nivel_cromatico_entry = ttk.Entry(root, width=10)
nivel_cromatico_entry.grid(column=1, row=0, padx=10, pady=10)

# Botón para calcular la temperatura
calcular_btn = ttk.Button(root, text="Calcular Temperatura", command=calcular_temperatura)
calcular_btn.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

# Etiqueta para mostrar el resultado
ttk.Label(root, text="Temperatura recomendada:").grid(column=0, row=2, padx=10, pady=10)
temperatura_resultado = tk.StringVar()
temperatura_label = ttk.Label(root, textvariable=temperatura_resultado)
temperatura_label.grid(column=1, row=2, padx=10, pady=10)

# Etiquetas para mostrar los cálculos detallados
ttk.Label(root, text="Pertenencia de las funciones:").grid(column=0, row=3, padx=10, pady=10)
pertenencia_resultado = tk.StringVar()
pertenencia_label = ttk.Label(root, textvariable=pertenencia_resultado)
pertenencia_label.grid(column=1, row=3, padx=10, pady=10)

# ttk.Label(root, text="Valores de las reglas:").grid(column=0, row=4, padx=10, pady=10)
# reglas_resultado = tk.StringVar()
# reglas_label = ttk.Label(root, textvariable=reglas_resultado)
# reglas_label.grid(column=1, row=4, padx=10, pady=10)

# Mostrar las gráficas de las funciones de pertenencia iniciales
nivel_cromatico.view()
temperatura.view()

# Iniciar la interfaz gráfica
root.mainloop()
