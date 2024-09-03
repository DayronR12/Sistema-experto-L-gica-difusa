import tkinter as tk
import clips
from io import StringIO
import sys

# Crear entorno CLIPS
env = clips.Environment()
env.load('rules.clp')

# Función para configurar los hechos en CLIPS
def set_facts(peso, raza, edad, enfermedades):
    env.reset()
    env.assert_string(f"(peso {peso})")
    env.assert_string(f"(raza \"{raza}\")")
    env.assert_string(f"(edad {edad})")
    env.assert_string(f"(enfermedades \"{enfermedades}\")")
    
    # Imprimir los hechos en CLIPS para depuración
    print("Hechos en CLIPS:")
    for fact in env.facts():
        print(fact)

# Capturar la salida de CLIPS en un buffer
class CLIPSRedirector:
    print("Testing CLIPS output redirection")
    def __init__(self):
        self.buffer = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.buffer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout

# Función para ejecutar el sistema experto y obtener recomendaciones
def recommend_diet():
    peso = entry_peso.get()
    raza = entry_raza.get()
    edad = entry_edad.get()
    enfermedades = entry_enfermedades.get()
    
    print(f"Peso: {peso}, Raza: {raza}, Edad: {edad}, Enfermedades: {enfermedades}")
    
    set_facts(peso, raza, edad, enfermedades)
    
    # Ejecutar el entorno CLIPS
    with CLIPSRedirector() as redirector:
        env.run()
    
    # Obtener la recomendación desde el buffer
    result = redirector.buffer.getvalue()
    print("Resultado de la ejecución:")
    print(result)

    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, result)
    text_result.config(state=tk.DISABLED)

# Crear ventana principal
root = tk.Tk()
root.title("Sistema Experto de Alimentación")

# Crear y colocar etiquetas y campos de entrada
tk.Label(root, text="Peso (KG) :").grid(row=0, column=0, padx=10, pady=5)
entry_peso = tk.Entry(root)
entry_peso.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Raza: (Grande/Mediana/Pequeña) ").grid(row=1, column=0, padx=10, pady=5)
entry_raza = tk.Entry(root)
entry_raza.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Edad (Años) :").grid(row=2, column=0, padx=10, pady=5)
entry_edad = tk.Entry(root)
entry_edad.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Enfermedades: (Si/No) ").grid(row=3, column=0, padx=10, pady=5)
entry_enfermedades = tk.Entry(root)
entry_enfermedades.grid(row=3, column=1, padx=10, pady=5)

# Crear botón para obtener recomendaciones
btn_recommend = tk.Button(root, text="Obtener Recomendación", command=recommend_diet)
btn_recommend.grid(row=5, column=0, columnspan=2, pady=10)

# Crear área de texto para mostrar resultados
text_result = tk.Text(root, height=10, width=50, wrap=tk.WORD)
text_result.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
text_result.config(state=tk.DISABLED)

# Ejecutar la ventana principal
root.mainloop()
