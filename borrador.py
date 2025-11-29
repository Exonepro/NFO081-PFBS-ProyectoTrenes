import tkinter as tk

# el submódulo ttk contiene
# "themed widgets" (más sofisticados)
import tkinter.ttk as ttk


def main():
   root = tk.Tk()
   root.title("Prueba Notebook")

   ntb_tabulador = ttk.Notebook(root)

   # Frames vacíos:
   tab1 = tk.Frame(ntb_tabulador, bg="blue", width=250, height=60)
   tab2 = tk.Frame(ntb_tabulador, bg="red", width=250, height=60)

   ntb_tabulador.add(tab1, text="tab azul")
   ntb_tabulador.add(tab2, text="tab rojo")

   ntb_tabulador.pack(expand=1, fill="y")
   root.mainloop()
if __name__ == "__main__":
   main()